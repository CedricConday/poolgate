"""Matchers without a model: BM25 keyword search, and a structured-field filter.

BM25 is what a pool search box does: it ranks records by the vacancy's words.
The field filter is what an ATS filter panel does: keep the records whose
structured fields meet every must-have, rank those first. Neither needs a
network or a dependency; both are baselines a model-based matcher must beat.
"""

from __future__ import annotations

import math
import re
from collections import Counter

from . import geo
from .types import Ranked

_TOKEN = re.compile(r"[^\W_]+", re.UNICODE)
STOP = {"für", "und", "oder", "m", "w", "d", "im", "der", "die", "das", "mit", "von", "zu",
        "in", "auf", "ca", "nach", "bei", "auch"}
_SHIFT_RANK = {"3-Schicht": 0, "2-Schicht": 1, "nur Tagschicht": 2}


def tokens(text: str) -> list[str]:
    return [t for t in _TOKEN.findall(text.lower()) if t not in STOP]


def card(p: dict, vacancy: dict | None = None) -> str:
    """The record as one text block, the way a recruiter or a model reads it."""
    def ka(v):
        return "k. A." if v is None else v
    certs = p["zertifikate"]
    lines = [
        f"Profil {p['id']} | {p['name']}",
        f"Beruf: {ka(p['beruf'])}",
        f"Wohnort: {p['plz']} {p['ort']}",
    ]
    if vacancy is not None:
        d = geo.km(p["ort"], vacancy["site"])
        lines.append(f"Entfernung zum Einsatzort {vacancy['site']}: ca. {d:.0f} km Luftlinie")
    lines += [
        f"Berufserfahrung (Jahre): {ka(p['erfahrung_jahre'])}",
        ("Zertifikate/Kenntnisse: k. A." if certs is None else
         "Zertifikate/Kenntnisse (vollständige Liste): " + (", ".join(certs) or "keine")),
        f"Führerschein: {ka(p['fuehrerschein'])}",
        f"Schichtbereitschaft: {ka(p['schicht'])}",
        f"Rufbereitschaft: {ka(p['rufbereitschaft'])}",
        f"Gehaltswunsch: {p['gehaltswunsch_eur']} EUR/Jahr",
        f"Verfügbar: {p['verfuegbar']}",
        f"Letzter Kontakt: {p['letzter_kontakt']}",
        f"Notizen: {p['notizen']}",
    ]
    return "\n".join(lines)


def query(vacancy: dict) -> list[str]:
    words = [vacancy["title"], *vacancy["trades"], *vacancy["certs_any"], vacancy["site"]]
    if vacancy["licence"]:
        words.append("Führerschein")
    if vacancy["shift"]:
        words.append("Schicht")
    if vacancy["on_call"]:
        words.append("Rufbereitschaft")
    return tokens(" ".join(words))


def bm25(q: list[str], docs: list[list[str]], k1: float = 1.2, b: float = 0.75) -> list[float]:
    n = len(docs)
    avg = sum(map(len, docs)) / n if n else 0.0
    df = Counter(t for d in docs for t in set(d))
    idf = {t: math.log(1 + (n - df[t] + 0.5) / (df[t] + 0.5)) for t in set(q)}
    scores = []
    for d in docs:
        tf = Counter(d)
        s = 0.0
        for t in q:
            if tf[t]:
                s += idf[t] * tf[t] * (k1 + 1) / (tf[t] + k1 * (1 - b + b * len(d) / avg))
        scores.append(s)
    return scores


class KeywordMatcher:
    """BM25 over the whole record, structured fields and notes alike.

    With `soft_filter` (the default), records whose structured fields
    explicitly contradict a must-have (a filled field that fails it: too far,
    too few years, "Führerschein: keiner") are moved behind the rest, as an ATS
    radius and field search would. Empty fields (k. A.) never exclude, and the
    free-text Beruf field is left to the keywords.
    """

    def __init__(self, soft_filter: bool = True):
        self.soft_filter = soft_filter
        self.name = "keyword" if soft_filter else "bm25"

    def rank(self, vacancy: dict, profiles: list[dict]) -> list[Ranked]:
        docs = [tokens(card(p)) for p in profiles]
        scores = bm25(query(vacancy), docs)
        order = sorted(range(len(profiles)), key=lambda i: (-scores[i], profiles[i]["id"]))
        out_in, out_rest = [], []
        for i in order:
            p = profiles[i]
            bad = contradicted(vacancy, p) if self.soft_filter else []
            r = Ranked(p["id"], scores[i], stage="bm25",
                       note=("Feld widerspricht: " + ", ".join(bad)) if bad else "")
            (out_rest if bad else out_in).append(r)
        return out_in + out_rest


_FIELD = {"erfahrung": "erfahrung_jahre", "zertifikate": "zertifikate",
          "fuehrerschein": "fuehrerschein", "entfernung": "ort", "schicht": "schicht",
          "rufbereitschaft": "rufbereitschaft"}


def contradicted(vacancy: dict, p: dict) -> list[str]:
    """Must-haves a filled structured field fails. Beruf is free text and never counts."""
    return [m for m, ok in field_check(vacancy, p).items()
            if not ok and m in _FIELD and p[_FIELD[m]] is not None]


def field_check(vacancy: dict, p: dict) -> dict[str, bool]:
    """The must-haves as a filter panel sees them: structured fields only."""
    out = {}
    for m in vacancy["musts"]:
        if m == "beruf":
            out[m] = p["beruf"] in vacancy["trades"]
        elif m == "erfahrung":
            out[m] = p["erfahrung_jahre"] is not None and p["erfahrung_jahre"] >= vacancy[
                "min_years"]
        elif m == "zertifikate":
            out[m] = bool(set(p["zertifikate"] or ()) & set(vacancy["certs_any"]))
        elif m == "fuehrerschein":
            out[m] = p["fuehrerschein"] == "B"
        elif m == "entfernung":
            out[m] = geo.km(p["ort"], vacancy["site"]) <= vacancy["radius_km"]
        elif m == "schicht":
            want = {"3": 0, "2": 1}[vacancy["shift"]]
            out[m] = p["schicht"] is not None and _SHIFT_RANK[p["schicht"]] <= want
        elif m == "rufbereitschaft":
            out[m] = p["rufbereitschaft"] == "ja"
    return out


class FieldFilterMatcher:
    """Filter on the structured fields, then BM25 within and after the filter."""

    name = "field-filter"

    def rank(self, vacancy: dict, profiles: list[dict]) -> list[Ranked]:
        ranked = KeywordMatcher(soft_filter=False).rank(vacancy, profiles)
        by_id = {p["id"]: p for p in profiles}
        out_in, out_rest = [], []
        for r in ranked:
            checks = field_check(vacancy, by_id[r.id])
            ok = all(checks.values())
            failed = [m for m, v in checks.items() if not v]
            r = Ranked(r.id, r.score, shortlist=ok, stage="filter",
                       note="" if ok else "Feld leer oder unpassend: " + ", ".join(failed))
            (out_in if ok else out_rest).append(r)
        return out_in + out_rest
