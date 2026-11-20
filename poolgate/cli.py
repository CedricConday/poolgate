"""poolgate command line."""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

from . import __version__
from .gate import run_matcher, truth_for
from .pool import case_family, make_pool
from .report import render


def _parse_bias(spec: str | None) -> dict:
    out = {}
    for part in filter(None, (spec or "").split(",")):
        k, _, v = part.partition("=")
        out[k.strip()] = int(v or 1)
    return out


def pool_summary(pool) -> dict:
    out = {}
    for v in pool.vacancies:
        t = truth_for(pool, v)
        fams = Counter(case_family(c) for c in t["fits"].values())
        out[v.key] = {"fits": len(t["fits"]), "near": len(t["near"]),
                      **{f: fams.get(f, 0) for f in ("plain", "synonym", "buried")},
                      "fit_ids": t["fits"], "near_ids": t["near"]}
    return out


def pool_dump(pool) -> dict:
    """Every profile as the matcher sees it, plus the hidden truth, for inspection."""
    return {"seed": pool.seed, "vacancies": [v.public() for v in pool.vacancies],
            "profiles": [{**p.public(), "_truth": {
                "trade": p.facts.trade, "years": p.facts.years,
                "certs": sorted(p.facts.certs), "licence": p.facts.licence,
                "town": p.facts.town, "shift": p.facts.shift, "on_call": p.facts.on_call,
                "origin": p.identity.origin, "gender": p.identity.gender,
                "title_shown_as": p.pres.title, "only_in_notes": sorted(p.pres.hidden),
                "planted": p.planted}} for p in pool.profiles]}


def _matchers(args, pool, log):
    from .keyword import FieldFilterMatcher, KeywordMatcher

    usage = None
    out = []
    for name in args.matchers.split(","):
        name = name.strip()
        if name in ("keyword", "keyword+syn"):
            out.append(KeywordMatcher(synonyms=name.endswith("+syn")))
        elif name == "bm25":
            out.append(KeywordMatcher(soft_filter=False))
        elif name in FieldFilterMatcher.NAMES.values():
            mode = next(k for k, v in FieldFilterMatcher.NAMES.items() if v == name)
            out.append(FieldFilterMatcher(mode))
        elif name == "offline":
            from .offline import OfflineMatcher

            out.append(OfflineMatcher(pool.by_id(), miss_synonym=args.miss_synonym,
                                      miss_buried=args.miss_buried, near_miss=args.near_miss,
                                      bias=_parse_bias(args.bias), noise=args.noise))
        elif name == "claude":
            from .claude import ClaudeRerank, Usage
            from .subscription import CliClient

            usage = usage or Usage()
            out.append(ClaudeRerank(CliClient(log=log), model=args.model, effort=args.effort,
                                    top_n=args.top_n, batch=args.batch, workers=args.workers,
                                    usage=usage))
        else:
            raise SystemExit(f"unknown matcher {name!r}")
    if args.matcher_url:
        from .http import HttpMatcher

        out.append(HttpMatcher(args.matcher_url))
    return out, usage


def cmd_run(args) -> int:
    def log(msg: str) -> None:
        print(f"[poolgate] {msg}", file=sys.stderr, flush=True)

    pool = make_pool(args.n, args.seed)
    matchers, usage = _matchers(args, pool, log)
    out = args.out or Path("results") / f"run-{time.strftime('%Y%m%d-%H%M%S')}"
    out.mkdir(parents=True, exist_ok=True)
    runs = []
    for m in matchers:
        runs.append(run_matcher(m, pool, fairness=not args.no_fairness, swaps=args.swaps,
                                repeats=args.repeats, seed=args.seed, progress=log))
        if hasattr(m, "answers"):
            runs[-1]["model_answers"] = m.answers
        if usage:
            log(f"usage so far: {usage.as_dict()}")
    config = {"n": args.n, "seed": args.seed, "matchers": [m.name for m in matchers],
              "model": args.model if usage else None, "effort": args.effort if usage else None,
              "top_n": args.top_n, "batch": args.batch, "swaps": args.swaps,
              "repeats": args.repeats, "note": args.note, "version": __version__,
              "faults": {"miss_synonym": args.miss_synonym, "miss_buried": args.miss_buried,
                         "near_miss": args.near_miss, "bias": args.bias, "noise": args.noise}}
    result = {"config": config, "pool_summary": pool_summary(pool),
              "usage": usage.as_dict() if usage else None, "runs": runs}
    (out / "run.json").write_text(json.dumps(result, ensure_ascii=False, indent=1))
    (out / "report.md").write_text(render(result, config))
    if args.dump_pool:
        (out / "pool.json").write_text(json.dumps(pool_dump(pool), ensure_ascii=False, indent=1))
    log(f"wrote {out}/report.md")
    return 0


PROOF = [
    ("none", {}),
    ("misses synonym fits (p=0.5)", {"miss_synonym": 0.5}),
    ("misses buried facts (p=0.5)", {"miss_buried": 0.5}),
    ("takes near-misses for fits (p=0.5)", {"near_miss": 0.5}),
    ("downgrades Turkish and Arabic names", {"bias": {"tr": 1, "ar": 1}}),
    ("random score noise (±25)", {"noise": 25.0}),
]


def cmd_proof(args) -> int:
    """The offline stand-in with one planted fault at a time: does the gate see it?"""
    from .offline import OfflineMatcher
    from .report import pct

    pool = make_pool(args.n, args.seed)
    out = args.out or Path("results") / "offline-proof"
    out.mkdir(parents=True, exist_ok=True)
    rows, runs = [], []
    for label, knobs in PROOF:
        m = OfflineMatcher(pool.by_id(), name=f"offline: {label}", **knobs)
        r = run_matcher(m, pool, seed=args.seed)
        runs.append(r)
        mm, f = r["metrics"], r["fairness"]
        lost = {g: x for g, x in f["lost_top10_place"].items() if x["k"]}
        rows.append(
            f"| {label} | {pct(mm['recall@20'], False)} | "
            f"{pct(mm['by_case']['synonym']['in_shortlist'], False)} | "
            f"{pct(mm['by_case']['buried']['in_shortlist'], False)} | "
            f"{pct(mm['near_miss@10'], False)} | "
            f"{pct(f['top10_flips_on_swap'], False)} | "
            f"{pct(f['top10_flips_on_repeat'], False)} | "
            + (", ".join(f"{g} {x['k']}/{x['n']}" for g, x in lost.items()) or "nobody")
            + " |")
    table = "\n".join([
        f"Offline stand-in, pool of {args.n}, seed {args.seed}. One fault at a time.",
        "",
        ("| Planted fault | Recall@20 | Synonym fits shortlisted | Buried fits shortlisted | "
        "Near-misses in top 10 | Top-10 flips on swap | on repeat | Lost a top-10 place |"),
        "|---|---|---|---|---|---|---|---|",
        *rows, ""])
    (out / "report.md").write_text("# poolgate offline proof\n\n" + table)
    (out / "run.json").write_text(json.dumps(
        {"config": {"n": args.n, "seed": args.seed, "version": __version__},
         "pool_summary": pool_summary(pool), "runs": runs}, ensure_ascii=False, indent=1))
    print(table)
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        prog="poolgate",
        description="Plant known fits and near-misses in a synthetic talent pool, run a "
                    "matcher, and score who reaches the shortlist, who is missed and why.")
    p.add_argument("--version", action="version", version=f"poolgate {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("run", "proof"):
        s = sub.add_parser(name)
        s.add_argument("--n", type=int, default=400, help="profiles in the pool")
        s.add_argument("--seed", type=int, default=7)
        s.add_argument("--out", type=Path, default=None)
    r = sub.choices["run"]
    r.add_argument("--matchers", default="keyword,field-filter",
                   help="comma list of bm25, keyword, keyword+syn, field-filter-exact, "
                        "field-filter, field-filter+syn, offline, claude")
    r.add_argument("--matcher-url", default=None, help="also run an HTTP matcher")
    r.add_argument("--model", default="claude-opus-5-5")
    r.add_argument("--effort", default="medium")
    r.add_argument("--top-n", type=int, default=50, help="keyword prefilter depth for claude")
    r.add_argument("--batch", type=int, default=10, help="profiles per model call")
    r.add_argument("--workers", type=int, default=3, help="parallel model calls")
    r.add_argument("--swaps", type=int, default=2)
    r.add_argument("--repeats", type=int, default=1)
    r.add_argument("--no-fairness", action="store_true")
    r.add_argument("--dump-pool", action="store_true", help="also write pool.json")
    r.add_argument("--note", default=None)
    r.add_argument("--miss-synonym", type=float, default=0.0)
    r.add_argument("--miss-buried", type=float, default=0.0)
    r.add_argument("--near-miss", type=float, default=0.0)
    r.add_argument("--bias", default=None, help='offline only, e.g. "tr=1,ar=1"')
    r.add_argument("--noise", type=float, default=0.0)
    args = p.parse_args(argv)
    return cmd_run(args) if args.cmd == "run" else cmd_proof(args)


if __name__ == "__main__":
    raise SystemExit(main())
