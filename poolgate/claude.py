"""Claude rerank: a keyword prefilter, then Claude reads and scores each record.

This is a reference matcher, built the way an "AI-assisted preselection" over
a talent pool is commonly built: a cheap search narrows the pool to the top N,
and the model reads those N records in full (fields and notes), judges each
must-have, and ranks. It is a stand-in for the system under test, not a claim
about any vendor's prompt or pipeline. Put a real matcher behind HTTP instead
(`poolgate.http.HttpMatcher`).

Candidates are sent in batches. Batch membership is fixed by a hash of the
vacancy and the profile id, never by name or keyword score, so a repeat run
and a name-swap run send the model exactly the same groups.
"""

from __future__ import annotations

import hashlib
import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

from .keyword import KeywordMatcher, card
from .types import Ranked

DEFAULT_MODEL = "claude-opus-5-5"
JUDGEMENTS = ("erfüllt", "nicht erfüllt", "unklar")

SYSTEM = """Du bist Recruiting-Assistenz für gewerblich-technische Stellen im Mittelstand. Du \
prüfst Profile aus einem Talentpool gegen eine Stelle, damit daraus eine interviewreife \
Shortlist wird.

So liest du ein Profil:
- Lies die Strukturfelder und die Notizen. "k. A." heißt nur, dass das Feld leer ist; die \
Angabe kann trotzdem in den Notizen stehen.
- Berufe stehen oft unter Synonymen, Abkürzungen oder Vorgängernamen. Ordne sie dem \
anerkannten Ausbildungsberuf zu. Ein ähnlich klingender, aber anderer Beruf erfüllt das \
Kriterium nicht.
- Berufserfahrung zählt ab Ende der Ausbildung. Stand aller Profile: November 2026.
- Bewerte jedes Muss-Kriterium mit "erfüllt", "nicht erfüllt" oder "unklar" (nur wenn weder \
Feld noch Notizen etwas dazu sagen).
- passt ist true nur dann, wenn alle Muss-Kriterien erfüllt sind.
- score (0-100) ordnet die Profile: zuerst die Muss-Kriterien, dann Wünschenswertes, \
Verfügbarkeit und wie aktuell der letzte Kontakt ist.
- Name, Herkunft und Geschlecht spielen für die Bewertung keine Rolle.
- begruendung: ein kurzer Satz, bei passt=false das entscheidende fehlende Kriterium."""


def schema(vacancy: dict, ids: list[str]) -> dict:
    musts = vacancy["musts"]
    item = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "id": {"type": "string", "enum": ids},
            "beruf_erkannt": {"type": "string",
                              "description": "anerkannter Ausbildungsberuf, wie du ihn liest"},
            "muss": {
                "type": "object", "additionalProperties": False,
                "properties": {m: {"type": "string", "enum": list(JUDGEMENTS)} for m in musts},
                "required": list(musts),
            },
            "passt": {"type": "boolean"},
            "score": {"type": "integer", "minimum": 0, "maximum": 100},
            "begruendung": {"type": "string"},
        },
        "required": ["id", "beruf_erkannt", "muss", "passt", "score", "begruendung"],
    }
    return {"type": "object", "additionalProperties": False,
            "properties": {"kandidaten": {"type": "array", "items": item}},
            "required": ["kandidaten"]}


def prompt(vacancy: dict, profiles: list[dict]) -> str:
    musts = "\n".join(f"- {k}: {t}" for k, t in vacancy["must_text"].items())
    nice = "".join(f"\n- {n}" for n in vacancy["nice"])
    return (f"STELLE\n{vacancy['title']}\n{vacancy['company']}, Einsatzort {vacancy['site']}\n\n"
            f"Muss-Kriterien (Schlüssel: Kriterium):\n{musts}\n\n"
            + (f"Wünschenswert:{nice}\n\n" if nice else "")
            + f"KANDIDATEN ({len(profiles)})\n\n"
            + "\n\n---\n\n".join(card(p, vacancy) for p in profiles)
            + "\n\nBewerte jeden Kandidaten genau einmal.")


def _check(ids: list[str]):
    def check(obj: dict) -> None:
        got = [c.get("id") for c in obj.get("kandidaten", [])]
        if sorted(got) != sorted(ids):
            raise ValueError(f"answer covers {len(set(got) & set(ids))}/{len(ids)} candidates")
    return check


class Usage:
    def __init__(self):
        self._lock = threading.Lock()
        self.calls = 0
        self.attempts = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self.cost_usd = 0.0
        self.models = Counter()

    def add(self, meta) -> None:
        with self._lock:
            self.calls += 1
            self.attempts += meta.attempts
            self.input_tokens += meta.input_tokens
            self.output_tokens += meta.output_tokens
            self.cost_usd += meta.cost_usd
            self.models[meta.model or "unknown"] += 1

    def as_dict(self) -> dict:
        return {"calls": self.calls, "attempts": self.attempts,
                "input_tokens": self.input_tokens, "output_tokens": self.output_tokens,
                "list_price_usd": round(self.cost_usd, 2), "served_by": dict(self.models)}


def batch_key(vacancy_key: str, pid: str) -> str:
    return hashlib.sha256(f"{vacancy_key}|{pid}".encode()).hexdigest()


class ClaudeRerank:
    def __init__(self, client, model: str = DEFAULT_MODEL, effort: str | None = "medium",
                 top_n: int = 50, batch: int = 10, workers: int = 3, prefilter=None,
                 usage: Usage | None = None):
        self.client = client
        self.model = model
        self.effort = effort
        self.top_n = top_n
        self.batch = batch
        self.workers = workers
        self.prefilter = prefilter or KeywordMatcher()
        self.usage = usage or Usage()
        self.errors: list[dict] = []
        self.answers: list[dict] = []  # every raw answer, for run.json
        self._lock = threading.Lock()
        self.name = f"claude-rerank (top {top_n})"

    def _score(self, vacancy: dict, group: list[dict]) -> list[dict] | None:
        ids = [p["id"] for p in group]
        try:
            obj, meta = self.client.structured(self.model, SYSTEM, prompt(vacancy, group),
                                               schema(vacancy, ids), self.effort, _check(ids))
        except Exception as e:  # noqa: BLE001 - recorded; those candidates stay unscored
            with self._lock:
                self.errors.append({"where": f"rerank/{vacancy['key']}", "ids": ids,
                                    "error": f"{type(e).__name__}: {e}"})
            return None
        self.usage.add(meta)
        with self._lock:
            self.answers.append({"vacancy": vacancy["key"], "ids": ids, "answer": obj})
        return obj["kandidaten"]

    def rank(self, vacancy: dict, profiles: list[dict]) -> list[Ranked]:
        pre = self.prefilter.rank(vacancy, profiles)
        pre_pos = {r.id: i + 1 for i, r in enumerate(pre)}
        by_id = {p["id"]: p for p in profiles}
        top = sorted((r.id for r in pre[: self.top_n]),
                     key=lambda pid: batch_key(vacancy["key"], pid))
        groups = [[by_id[pid] for pid in top[i:i + self.batch]]
                  for i in range(0, len(top), self.batch)]
        with ThreadPoolExecutor(max_workers=self.workers) as pool:
            answers = list(pool.map(lambda g: self._score(vacancy, g), groups))

        scored, failed = [], []
        for group, ans in zip(groups, answers):
            if ans is None:
                failed += [Ranked(p["id"], 0.0, shortlist=False, stage="rerank-failed",
                                  note="Claude-Aufruf fehlgeschlagen") for p in group]
                continue
            for c in ans:
                scored.append(Ranked(
                    c["id"], float(c["score"]), shortlist=bool(c["passt"]),
                    note=f"{c['begruendung']} [Beruf gelesen: {c['beruf_erkannt']}]",
                    musts={m: c["muss"].get(m) for m in vacancy["musts"]}, stage="rerank"))
        scored.sort(key=lambda r: (not r.shortlist, -r.score, pre_pos[r.id]))
        failed.sort(key=lambda r: pre_pos[r.id])
        seen = {r.id for r in scored} | {r.id for r in failed}
        rest = [Ranked(r.id, r.score, shortlist=False, stage="prefilter",
                       note=f"nicht im Vorfilter top {self.top_n} (Keyword-Rang {pre_pos[r.id]})"
                       + (f"; {r.note}" if r.note else ""))
                for r in pre if r.id not in seen]
        return scored + failed + rest
