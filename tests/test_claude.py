"""The Claude path and the HTTP adapter, offline: fake clients, a fake CLI, a local server."""

import json
import os
import stat
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from poolgate.claude import ClaudeRerank, schema
from poolgate.gate import run_matcher
from poolgate.http import HttpMatcher
from poolgate.pool import VACANCY_BY_KEY, check, make_pool, swap_names
from poolgate.subscription import CallMeta, CliClient, CliError


@pytest.fixture(scope="module")
def pool():
    return make_pool(400, 7)


class OracleClient:
    """Answers like a model that reads every record correctly."""

    def __init__(self, pool, fail_vacancy=None):
        self.truth = pool.by_id()
        self.fail_vacancy = fail_vacancy
        self.batches = []
        self.lock = threading.Lock()

    def structured(self, model, system, prompt, schema, effort=None, check_fn=None):
        ids = schema["properties"]["kandidaten"]["items"]["properties"]["id"]["enum"]
        key = next(k for k in VACANCY_BY_KEY if VACANCY_BY_KEY[k].title in prompt)
        with self.lock:
            self.batches.append((key, tuple(ids)))
        if key == self.fail_vacancy:
            raise CliError("rate limited")
        v = VACANCY_BY_KEY[key]
        out = []
        for pid in ids:
            c = check(v, self.truth[pid].facts)
            out.append({"id": pid, "beruf_erkannt": self.truth[pid].facts.trade,
                        "muss": {m: "erfüllt" if ok else "nicht erfüllt" for m, ok in c.items()},
                        "passt": all(c.values()), "score": 90 if all(c.values()) else 30,
                        "begruendung": "ok"})
        obj = {"kandidaten": out}
        if check_fn:
            check_fn(obj)
        return obj, CallMeta("claude-opus-5-5", 1000, 200, 0.01, 1)


def test_rerank_with_a_perfect_reader_is_limited_only_by_the_prefilter(pool):
    client = OracleClient(pool)
    r = run_matcher(ClaudeRerank(client, top_n=50, batch=10, workers=2), pool, fairness=False)
    m = r["metrics"]
    reached = m["reached_rerank"]
    # Every fit that reached the model is shortlisted, and nothing else is.
    assert m["shortlist"]["precision"]["rate"] == 1.0
    assert m["shortlist"]["recall"]["k"] == reached["k"]
    for e in r["per_vacancy"]:
        for x in e["missed"]:
            assert x["stage"] == "prefilter" and "nicht im Vorfilter" in x["matcher_note"]


def test_prefilter_choice_names_the_matcher_and_sets_what_reaches_the_model(pool):
    from poolgate.keyword import KeywordMatcher

    plain = ClaudeRerank(OracleClient(pool), top_n=50, batch=10, workers=2)
    wide = ClaudeRerank(OracleClient(pool), top_n=50, batch=10, workers=2,
                        prefilter=KeywordMatcher(synonyms=True))
    assert plain.name == "claude-rerank (top 50)"
    assert wide.name == "claude-rerank@keyword+syn (top 50)"
    a = run_matcher(plain, pool, fairness=False)["metrics"]["reached_rerank"]["k"]
    b = run_matcher(wide, pool, fairness=False)["metrics"]["reached_rerank"]["k"]
    assert a != b  # the prefilter, not the reader, decides which fits get read


def test_batches_are_identical_on_repeat_and_on_name_swap(pool):
    client = OracleClient(pool)
    m = ClaudeRerank(client, top_n=50, batch=10, workers=1)
    v = pool.vacancies[0].public()
    m.rank(v, pool.public())
    first = sorted(client.batches)
    client.batches.clear()
    m.rank(v, [p.public() for p in swap_names(pool, 1234)])
    assert sorted(client.batches) == first


def test_a_failing_call_leaves_candidates_unscored_not_the_run_dead(pool):
    client = OracleClient(pool, fail_vacancy="cnc-guetersloh")
    matcher = ClaudeRerank(client, top_n=20, batch=10, workers=1)
    r = run_matcher(matcher, pool, fairness=False)
    assert r["metrics"]["vacancies"] == 3
    assert any(e["where"] == "rerank/cnc-guetersloh" for e in r["errors"])
    cnc = r["rankings"]["cnc-guetersloh"]
    assert cnc[0]["stage"] == "rerank-failed"


def test_schema_names_exactly_the_vacancy_musts(pool):
    for v in pool.vacancies:
        s = schema(v.public(), ["p0001"])
        props = s["properties"]["kandidaten"]["items"]["properties"]["muss"]
        assert props["required"] == list(v.musts())


FAKE_CLI = r'''#!{python}
import json, os, sys
log = os.environ["FAKE_LOG"]
n = len(open(log).readlines()) if os.path.exists(log) else 0
with open(log, "a") as f:
    f.write(json.dumps(sys.argv[1:]) + "\n")
sys.stdin.read()
if n == 0:
    print(json.dumps({{"is_error": True, "result": "API Error: 429 rate_limit_error"}}))
else:
    print(json.dumps({{"is_error": False, "structured_output": {{"kandidaten": []}},
                      "usage": {{"input_tokens": 10, "cache_read_input_tokens": 5,
                                "output_tokens": 7}},
                      "modelUsage": {{"claude-opus-5-5": {{}}}}, "total_cost_usd": 0.02}}))
'''


def test_cli_client_retries_and_passes_the_isolation_flags(tmp_path, monkeypatch):
    fake = tmp_path / "claude"
    fake.write_text(FAKE_CLI.format(python=sys.executable))
    fake.chmod(fake.stat().st_mode | stat.S_IEXEC)
    log = tmp_path / "calls.log"
    monkeypatch.setenv("FAKE_LOG", str(log))
    waits = []
    client = CliClient(binary=str(fake), backoff=1, log=lambda m: None, sleep=waits.append)
    obj, meta = client.structured("claude-opus-5-5", "SYS", "PROMPT", {"type": "object"}, "medium")
    assert obj == {"kandidaten": []}
    assert meta.attempts == 2 and waits == [1]
    assert meta.input_tokens == 15 and meta.output_tokens == 7 and meta.cost_usd == 0.02
    argv = json.loads(log.read_text().splitlines()[-1])
    for flag in ("-p", "--strict-mcp-config", "--no-session-persistence", "--json-schema"):
        assert flag in argv
    assert argv[argv.index("--tools") + 1] == ""
    assert argv[argv.index("--setting-sources") + 1] == ""
    assert argv[argv.index("--system-prompt") + 1] == "SYS"
    assert argv[argv.index("--output-format") + 1] == "json"
    assert argv[argv.index("--model") + 1] == "claude-opus-5-5"
    assert os.listdir(client.cwd) == []


def test_cli_client_gives_up_after_its_attempts(tmp_path, monkeypatch):
    fake = tmp_path / "claude"
    fake.write_text(f"#!{sys.executable}\nprint('not json')\n")
    fake.chmod(fake.stat().st_mode | stat.S_IEXEC)
    client = CliClient(binary=str(fake), attempts=3, backoff=1, log=lambda m: None,
                       sleep=lambda s: None)
    with pytest.raises(CliError, match="gave up after 3"):
        client.structured("m", "s", "p", {"type": "object"})


def test_http_matcher_round_trip(pool):
    seen = {}

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            seen["n"] = len(body["profiles"])
            seen["vacancy"] = body["vacancy"]["key"]
            ids = [p["id"] for p in body["profiles"]][:3]
            data = {"ranking": [{"id": ids[1], "score": 2, "shortlist": True},
                                {"id": "nope", "score": 9},
                                {"id": ids[0], "score": 1, "musts": {"beruf": "erfüllt"}}]}
            raw = json.dumps(data).encode()
            self.send_response(200)
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def log_message(self, *a):
            pass

    srv = HTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        m = HttpMatcher(f"http://127.0.0.1:{srv.server_port}")
        v = pool.vacancies[1].public()
        out = m.rank(v, pool.public())
    finally:
        srv.shutdown()
    assert seen == {"n": 400, "vacancy": "cnc-guetersloh"}
    assert [r.id for r in out] == ["p0002", "p0001"]
    assert out[0].shortlist is True and out[1].musts == {"beruf": "erfüllt"}
