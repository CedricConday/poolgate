"""Matchers without a model: BM25 keyword search, and a structured-field filter.

BM25 is what a pool search box does: it ranks records by the vacancy's words.
The field filter is what an ATS filter panel does: keep the records whose
structured fields meet every must-have, rank those first. Neither needs a
network or a dependency; both are baselines a model-based matcher must beat.

Each comes in a literal form and a "+syn" form that gets the same synonym
table the pool generator uses (every official, variant, abbreviated and
predecessor name of each accepted trade): keyword search adds those names to
its query, the field filter accepts them in the Beruf field. The literal forms
show what that knowledge is worth.
"""

from __future__ import annotations

import math
import re
from collections import Counter

from . import geo
from .pool import NAMES
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


def query(vacancy: dict, synonyms: bool = False) -> list[str]:
    words = [vacancy["title"], *vacancy["trades"], *vacancy["certs_any"], vacancy["site"]]
    if vacancy["licence"]:
        words.append("Führerschein")
    if vacancy["shift"]:
        words.append("Schicht")
    if vacancy["on_call"]:
        words.append("Rufbereitschaft")
    q = tokens(" ".join(words))
    if synonyms:
        # Each word of the other names once, so expansion widens the query
        # without re-weighting the words it already has.
        q += [t for t in dict.fromkeys(tokens(" ".join(trade_names(vacancy["trades"]))))
              if t not in q]
    return q


def trade_names(trades) -> list[str]:
    """Every name in the synonym table for the given trades."""
    return [n for t in trades for n, *_ in NAMES.get(t, ((t,),))]


def norm_trade(name: str) -> str:
    """One spelling per trade name. Case, spacing, punctuation, the gender suffix
    ("/-in"), a chamber tag ("(IHK)") and the Fachrichtung form ("Elektroniker,
    Fachrichtung X" = "Elektroniker für X") do not change the qualification."""
    s = name.lower()
    s = re.sub(r"\((?:ihk|hwk)\)", " ", s)
    s = re.sub(r"\s*(?:/-?\s*in|\(in\)|/innen)\b", "", s)
    s = re.sub(r",?\s*\bfachrichtung\b\s*", " für ", s)
    return re.sub(r"[\s,]+", " ", s).strip(" .")


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

    def __init__(self, soft_filter: bool = True, synonyms: bool = False):
        self.soft_filter = soft_filter
        self.synonyms = synonyms
        self.name = ("keyword" if soft_filter else "bm25") + ("+syn" if synonyms else "")

    def rank(self, vacancy: dict, profiles: list[dict]) -> list[Ranked]:
        docs = [tokens(card(p)) for p in profiles]
        scores = bm25(query(vacancy, self.synonyms), docs)
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


def accepted_names(vacancy: dict, mode: str = "normalised") -> set[str]:
    """The Beruf field values a filter accepts. exact: the vacancy's trade names
    as written; normalised: the same, spelling normalised; synonyms: every name
    in the synonym table, normalised."""
    if mode == "exact":
        return set(vacancy["trades"])
    names = trade_names(vacancy["trades"]) if mode == "synonyms" else vacancy["trades"]
    return {norm_trade(n) for n in names}


def field_check(vacancy: dict, p: dict, mode: str = "normalised") -> dict[str, bool]:
    """The must-haves as a filter panel sees them: structured fields only."""
    out = {}
    for m in vacancy["musts"]:
        if m == "beruf":
            beruf = p["beruf"]
            out[m] = beruf is not None and (
                (beruf if mode == "exact" else norm_trade(beruf)) in accepted_names(vacancy, mode))
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


FIELD_FILTERS = {"exact": "field-filter-exact", "normalised": "field-filter",
                 "synonyms": "field-filter+syn"}  # mode -> matcher name


class FieldFilterMatcher:
    """Filter on the structured fields, then BM25 within and after the filter.

    mode: "exact" compares the Beruf field with the vacancy's trade names as
    strings; "normalised" (the default) first normalises spelling (`norm_trade`);
    "synonyms" also accepts every name in the synonym table.
    """

    def __init__(self, mode: str = "normalised"):
        if mode not in FIELD_FILTERS:
            raise ValueError(f"unknown mode {mode!r}")
        self.mode = mode
        self.name = FIELD_FILTERS[mode]

    def rank(self, vacancy: dict, profiles: list[dict]) -> list[Ranked]:
        ranked = KeywordMatcher(soft_filter=False, synonyms=self.mode == "synonyms").rank(
            vacancy, profiles)
        by_id = {p["id"]: p for p in profiles}
        out_in, out_rest = [], []
        for r in ranked:
            checks = field_check(vacancy, by_id[r.id], self.mode)
            ok = all(checks.values())
            failed = [m for m, v in checks.items() if not v]
            r = Ranked(r.id, r.score, shortlist=ok, stage="filter",
                       note="" if ok else "Feld leer oder unpassend: " + ", ".join(failed))
            (out_in if ok else out_rest).append(r)
        return out_in + out_rest
