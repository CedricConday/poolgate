"""Run matchers over the pool and grade the rankings against the planted truth.

For every vacancy the truth is computed from the hidden facts: which profiles
fit (every must-have met), how hard each fit is to see (plain, synonym,
buried in the notes), and which profiles are near-misses (fail exactly one
must-have while looking right). A ranking is then graded on

  recall@k       of the true fits, how many are in the top k
  precision@k    of the top k, how many are true fits
  shortlist      the matcher's own yes-list, when it has one
  near-miss@k    of the near-misses, how many got into the top k

and, separately, on whether the ranking moves when only names change
(the swap runs) beyond how much it moves on an unchanged re-run (the repeat
runs). Every rate carries a 95% Wilson interval.
"""

from __future__ import annotations

import math
import traceback
from collections import Counter, defaultdict

from .pool import (
    MUSTS,
    Pool,
    Vacancy,
    case_family,
    case_type,
    check,
    near_miss,
    swap_names,
)
from .types import Ranked

KS = (10, 20)
SHORTLIST_K = 10  # an interview-ready shortlist; also the matcher's list when it gives none


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def _rate(k: int, n: int) -> dict:
    lo, hi = wilson(k, n)
    return {"k": k, "n": n, "rate": (k / n) if n else None, "ci95": [lo, hi]}


def truth_for(pool: Pool, v: Vacancy) -> dict:
    fits, near = {}, {}
    for p in pool.profiles:
        checks = check(v, p.facts)
        if all(checks.values()):
            fits[p.id] = case_type(v, p)
        elif (m := near_miss(v, p.facts)) is not None:
            near[p.id] = m
    return {"fits": fits, "near": near}


def _positions(ranking: list[Ranked], all_ids: list[str]) -> dict[str, int]:
    pos = {r.id: i + 1 for i, r in enumerate(ranking)}
    tail = len(pos)
    for pid in all_ids:
        if pid not in pos:
            tail += 1
            pos[pid] = tail
    return pos


def _wrong_musts(r: Ranked | None, truth_checks: dict[str, bool]) -> list[str]:
    """Must-haves the matcher read differently from the truth (unklar counts as wrong)."""
    if r is None or not r.musts:
        return []
    out = []
    for m, ok in truth_checks.items():
        said = r.musts.get(m)
        if said is None:
            continue
        if (said == "erfüllt") != ok:
            out.append(m)
    return out


def evaluate_vacancy(pool: Pool, v: Vacancy, ranking: list[Ranked],
                     ks=KS, shortlist_k: int = SHORTLIST_K) -> dict:
    t = truth_for(pool, v)
    by_id = pool.by_id()
    pos = _positions(ranking, [p.id for p in pool.profiles])
    by_rank = {r.id: r for r in ranking}
    own = [r.id for r in ranking if r.shortlist]
    has_own = any(r.shortlist is not None for r in ranking)
    shortlist = set(own) if has_own else {r.id for r in ranking[:shortlist_k]}

    reading = defaultdict(Counter)  # must -> right / wrong / unklar
    for r in ranking:
        if not r.musts:
            continue
        truth_checks = check(v, by_id[r.id].facts)
        for m, ok in truth_checks.items():
            said = r.musts.get(m)
            if said is None:
                continue
            reading[m]["unklar" if said == "unklar" else
                       ("right" if (said == "erfüllt") == ok else "wrong")] += 1

    missed, false_pos = [], []
    for pid, case in sorted(t["fits"].items(), key=lambda kv: pos[kv[0]]):
        if pid in shortlist:
            continue
        r = by_rank.get(pid)
        missed.append({"vacancy": v.key, "id": pid, "rank": pos[pid], "case": case,
                       "title": by_id[pid].pres.title_text or "k. A.",
                       "stage": r.stage if r else "",
                       "matcher_note": r.note if r else "nicht zurückgegeben",
                       "misread": _wrong_musts(r, check(v, by_id[pid].facts))})
    # The shortlist's wrong entries: the matcher's own yes-list, or its top k.
    for r in ranking:
        if r.id not in shortlist or r.id in t["fits"]:
            continue
        checks = check(v, by_id[r.id].facts)
        false_pos.append({"vacancy": v.key, "id": r.id, "rank": pos[r.id],
                          "near_miss": t["near"].get(r.id),
                          "fails": [m for m, ok in checks.items() if not ok],
                          "matcher_note": r.note, "misread": _wrong_musts(r, checks)})

    return {
        "vacancy": v.key,
        "fits": t["fits"],
        "near": t["near"],
        "pos": {pid: pos[pid] for pid in (*t["fits"], *t["near"])},
        "shortlist": sorted(shortlist),
        "has_own_shortlist": has_own,
        "stages": {pid: (by_rank[pid].stage if pid in by_rank else "") for pid in t["fits"]},
        "reading": {m: dict(c) for m, c in reading.items()},
        "missed": missed,
        "false_positives": false_pos,
        "top": [pid for pid in (r.id for r in ranking[:max(ks)])],
    }


def metrics(per_vacancy: list[dict], ks=KS, rerank_stage: str = "rerank") -> dict:
    out: dict = {"vacancies": len(per_vacancy)}
    n_fits = sum(len(e["fits"]) for e in per_vacancy)
    for k in ks:
        hits = sum(1 for e in per_vacancy for pid in e["fits"] if e["pos"][pid] <= k)
        ceiling = sum(min(k, len(e["fits"])) for e in per_vacancy)
        out[f"recall@{k}"] = {**_rate(hits, n_fits), "ceiling": ceiling / n_fits if n_fits else 0}
        out[f"precision@{k}"] = _rate(hits, k * len(per_vacancy))
        nm = sum(1 for e in per_vacancy for pid in e["near"] if e["pos"][pid] <= k)
        out[f"near_miss@{k}"] = _rate(nm, sum(len(e["near"]) for e in per_vacancy))

    sl_hits = sum(1 for e in per_vacancy for pid in e["shortlist"] if pid in e["fits"])
    sl_n = sum(len(e["shortlist"]) for e in per_vacancy)
    out["shortlist"] = {"own": all(e["has_own_shortlist"] for e in per_vacancy),
                        "size": sl_n, "precision": _rate(sl_hits, sl_n),
                        "recall": _rate(sl_hits, n_fits),
                        "near_misses_in": sum(1 for e in per_vacancy for pid in e["shortlist"]
                                              if pid in e["near"])}

    for label, key in (("by_case", case_family), ("by_case_detail", lambda c: c)):
        groups = defaultdict(lambda: Counter())
        for e in per_vacancy:
            sl = set(e["shortlist"])
            for pid, case in e["fits"].items():
                g = groups[key(case)]
                g["n"] += 1
                g["sl"] += pid in sl
                for k in ks:
                    g[k] += e["pos"][pid] <= k
        out[label] = {g: {**{f"recall@{k}": _rate(c[k], c["n"]) for k in ks},
                          "in_shortlist": _rate(c["sl"], c["n"])}
                      for g, c in sorted(groups.items())}

    by_near = defaultdict(Counter)
    for e in per_vacancy:
        for pid, m in e["near"].items():
            by_near[m]["n"] += 1
            for k in ks:
                by_near[m][k] += e["pos"][pid] <= k
    out["near_miss_by_must"] = {m: {f"in_top{k}": _rate(c[k], c["n"]) for k in ks}
                                for m, c in sorted(by_near.items(), key=lambda x: MUSTS.index(x[0]))}

    out["per_vacancy"] = {
        e["vacancy"]: {"fits": len(e["fits"]), "near_misses": len(e["near"]),
                       **{f"recall@{k}": _rate(sum(1 for p in e["fits"] if e["pos"][p] <= k),
                                               len(e["fits"])) for k in ks}}
        for e in per_vacancy}

    staged = [s for e in per_vacancy for s in e["stages"].values()]
    if any(s == rerank_stage for s in staged):
        out["reached_rerank"] = _rate(sum(s == rerank_stage for s in staged), len(staged))

    reading = defaultdict(Counter)
    for e in per_vacancy:
        for m, c in e["reading"].items():
            reading[m].update(c)
    if reading:
        out["must_reading"] = {
            m: {"right": _rate(c["right"], sum(c.values())), "wrong": c["wrong"],
                "unklar": c["unklar"]}
            for m, c in sorted(reading.items(), key=lambda x: MUSTS.index(x[0]))}
    return out


# ---------------------------------------------------------------- fairness

def _ranks(ranking: list[Ranked], ids: list[str], cap: int) -> dict[str, int]:
    pos = {r.id: i + 1 for i, r in enumerate(ranking)}
    return {pid: min(pos.get(pid, cap), cap) for pid in ids}


def fairness_vacancy(matcher, pool: Pool, v: Vacancy, base: list[Ranked], swaps: int,
                     repeats: int, seed: int, top: int) -> dict:
    """Rank the same pool again unchanged, and again with every name swapped.

    Only names change in a swap (same gender, other origin; the surname in the
    notes too). The decision graded is shortlist inclusion (top SHORTLIST_K) for
    the profiles in the base run's top `top`.
    """
    ids = [r.id for r in base[:top]]
    cap = top + 1
    rec = {"vacancy": v.key, "ids": ids, "base": _ranks(base, ids, cap),
           "base_origin": {p.id: p.identity.origin for p in pool.profiles if p.id in ids},
           "repeats": [], "swaps": []}
    for _ in range(repeats):
        rec["repeats"].append(_ranks(matcher.rank(v.public(), pool.public()), ids, cap))
    for s in range(swaps):
        swapped = swap_names(pool, seed + 1000 * (s + 1))
        ranking = matcher.rank(v.public(), [p.public() for p in swapped])
        rec["swaps"].append({"ranks": _ranks(ranking, ids, cap),
                             "origin": {p.id: p.identity.origin for p in swapped if p.id in ids},
                             "names": {p.id: p.identity.name for p in swapped if p.id in ids}})
    return rec


def fairness_metrics(recs: list[dict], k: int = SHORTLIST_K) -> dict:
    def flips(pairs):
        n = f = 0
        shift = 0
        for a, b in pairs:
            for pid in a:
                n += 1
                f += (a[pid] <= k) != (b[pid] <= k)
                shift += abs(a[pid] - b[pid])
        return _rate(f, n), (shift / n if n else 0.0)

    rep, rep_shift = flips((r["base"], x) for r in recs for x in r["repeats"])
    swp, swp_shift = flips((r["base"], s["ranks"]) for r in recs for s in r["swaps"])

    # Per origin: every base/swap pair is a test of both origins it involves; it
    # counts against the side that is outside the shortlist while the other is in.
    tests, worse = Counter(), Counter()
    moved = defaultdict(list)  # target origin -> rank gains (positive = moved up)
    for r in recs:
        for s in r["swaps"]:
            for pid in r["ids"]:
                ob, os_ = r["base_origin"][pid], s["origin"][pid]
                in_b, in_s = r["base"][pid] <= k, s["ranks"][pid] <= k
                for g, mine, theirs in ((ob, in_b, in_s), (os_, in_s, in_b)):
                    tests[g] += 1
                    worse[g] += theirs and not mine
                moved[os_].append(r["base"][pid] - s["ranks"][pid])
    return {
        "profiles_tested": sum(len(r["ids"]) for r in recs),
        "shortlist_flips_on_swap": swp,
        "shortlist_flips_on_repeat": rep,
        "mean_rank_shift_on_swap": round(swp_shift, 2),
        "mean_rank_shift_on_repeat": round(rep_shift, 2),
        "lost_shortlist_place": {g: _rate(worse[g], tests[g]) for g in sorted(tests)},
        "mean_rank_gain_when_renamed_to": {g: round(sum(v) / len(v), 2)
                                           for g, v in sorted(moved.items())},
    }


# ---------------------------------------------------------------- run

def _guarded(fn, label: str):
    try:
        return fn(), None
    except Exception as e:  # noqa: BLE001 - one failed vacancy must not discard the run
        return None, {"where": label, "error": f"{type(e).__name__}: {e}",
                      "trace": traceback.format_exc(limit=4)}


def _compact(ranking: list[Ranked], n: int = 60) -> list[dict]:
    return [{"id": r.id, "score": round(r.score, 3), "shortlist": r.shortlist, "stage": r.stage,
             "note": r.note, "musts": r.musts} for r in ranking[:n]]


def run_matcher(matcher, pool: Pool, ks=KS, fairness: bool = True, swaps: int = 2,
                repeats: int = 1, fair_top: int = 50, seed: int = 7, progress=None) -> dict:
    progress = progress or (lambda msg: None)
    errors, per_v, rankings, fair = [], [], {}, []
    for v in pool.vacancies:
        ranking, err = _guarded(lambda v=v: matcher.rank(v.public(), pool.public()),
                                f"{matcher.name}/{v.key}")
        if err:
            errors.append(err)
            progress(f"{matcher.name} {v.key}: FAILED {err['error']}")
            continue
        rankings[v.key] = ranking
        per_v.append(evaluate_vacancy(pool, v, ranking, ks))
        progress(f"{matcher.name} {v.key}: ranked {len(ranking)}")
        if fairness:
            rec, err = _guarded(lambda v=v: fairness_vacancy(matcher, pool, v, ranking, swaps,
                                                             repeats, seed, fair_top),
                                f"{matcher.name}/{v.key}/fairness")
            if err:
                errors.append(err)
                progress(f"{matcher.name} {v.key} fairness: FAILED {err['error']}")
            else:
                fair.append(rec)
                progress(f"{matcher.name} {v.key}: fairness done")
    errors += list(getattr(matcher, "errors", []))
    return {
        "matcher": matcher.name,
        "metrics": metrics(per_v, ks) if per_v else {},
        "fairness": fairness_metrics(fair) if fair else None,
        "per_vacancy": per_v,
        "fairness_runs": fair,
        "rankings": {k: _compact(r) for k, r in rankings.items()},
        "errors": errors,
    }
