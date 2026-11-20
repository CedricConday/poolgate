"""One-page Markdown report comparing matchers on the same pool."""

from __future__ import annotations

from .pool import MUST_LABEL, VACANCY_BY_KEY

SYNONYM_LABEL = {"variant": "spelling variant", "abbrev": "abbreviation",
                 "predecessor": "predecessor name"}
CASE_LABEL = {
    "plain": "plain (official title, facts in fields)",
    "synonym": "synonym (Beruf field: another spelling, an abbreviation or a predecessor name)",
    "buried": "buried (a must-have fact only in the notes)",
}


def pct(r: dict | None, counts: bool = True) -> str:
    if not r or r.get("rate") is None:
        return "n/a"
    lo, hi = r["ci95"]
    core = f"{r['rate'] * 100:.0f}%"
    if counts:
        core += f" ({r['k']}/{r['n']})"
    return f"{core} [{lo * 100:.0f}–{hi * 100:.0f}]"


def _row(label: str, cells: list[str]) -> str:
    return f"| {label} | " + " | ".join(cells) + " |"


def render(result: dict, config: dict) -> str:
    runs = result["runs"]
    names = [r["matcher"] for r in runs]
    ms = [r["metrics"] for r in runs]
    pool = result["pool_summary"]
    out = [
        "# poolgate report",
        "",
        f"Pool: {config['n']} synthetic profiles, seed {config['seed']}, "
        f"{len(pool)} vacancies. Matchers: {', '.join(f'`{n}`' for n in names)}."
        + (f" {config['note']}" if config.get("note") else ""),
        "",
        "| Vacancy | True fits | of which plain / synonym / buried | Near-misses |",
        "|---|---|---|---|",
    ]
    for key, s in pool.items():
        out.append(f"| {VACANCY_BY_KEY[key].title} ({VACANCY_BY_KEY[key].site}, "
                   f"{VACANCY_BY_KEY[key].radius_km} km) | {s['fits']} | "
                   f"{s['plain']} / {s['synonym']} / {s['buried']} | {s['near']} |")
    errs = [(r["matcher"], e) for r in runs for e in r["errors"]]
    if errs:
        out += ["", (f"**{len(errs)} error(s); affected candidates are ranked after the scored "
                "ones and the run is otherwise complete. See `errors` in `run.json`.**")]
    out += ["", "## Headline", "",
            ("Brackets are 95% Wilson intervals. The shortlist is the matcher's own yes-list "
            "where it gives one, else its top 10."), "",
            "| Measure | " + " | ".join(f"`{n}`" for n in names) + " |",
            "|---|" + "---|" * len(names)]
    ceil = ms[0]["recall@10"]["ceiling"] if ms and ms[0] else 0
    out.append(_row(f"Recall@10 (ceiling {ceil * 100:.0f}%: more fits than places)",
                    [pct(m.get("recall@10")) for m in ms]))
    out.append(_row("Recall@20", [pct(m.get("recall@20")) for m in ms]))
    out.append(_row("Precision@10", [pct(m.get("precision@10")) for m in ms]))
    out.append(_row("Shortlist precision", [pct(m["shortlist"]["precision"]) for m in ms]))
    out.append(_row("Shortlist recall", [pct(m["shortlist"]["recall"]) for m in ms]))
    out.append(_row("Shortlist size (all vacancies)",
                    [str(m["shortlist"]["size"]) + ("" if m["shortlist"]["own"] else " (top 10)")
                     for m in ms]))
    out.append(_row("Near-misses in top 10", [pct(m.get("near_miss@10")) for m in ms]))
    out.append(_row("Near-misses in shortlist",
                    [str(m["shortlist"]["near_misses_in"]) for m in ms]))
    if any("reached_rerank" in m for m in ms):
        out.append(_row("True fits that reached the model",
                        [pct(m.get("reached_rerank")) if "reached_rerank" in m else "–"
                         for m in ms]))
        out.append(_row("Near-misses that reached the model",
                        [pct(m.get("near_reached_rerank")) if "near_reached_rerank" in m
                         else "–" for m in ms]))

    out += ["", "## Which fits are found", "",
            "Recall@20 and shortlist recall by how the fit is presented.", "",
            "| Case | " + " | ".join(f"`{n}` @20 / shortlist" for n in names) + " |",
            "|---|" + "---|" * len(names)]
    fams = sorted({c for m in ms for c in m.get("by_case", {})},
                  key=lambda c: list(CASE_LABEL).index(c))
    for c in fams:
        out.append(_row(CASE_LABEL[c], [
            (pct(m["by_case"][c]["recall@20"], False) + " / "
             + pct(m["by_case"][c]["in_shortlist"]))
            if c in m.get("by_case", {}) else "–" for m in ms]))
    details = sorted({c for m in ms for c in m.get("by_case_detail", {}) if ":" in c},
                     key=lambda c: (list(CASE_LABEL).index(c.split(":")[0]), c))
    for c in details:
        fam, sub = c.split(":")
        label = SYNONYM_LABEL[sub] if fam == "synonym" else MUST_LABEL[sub]
        out.append(_row(f"· {fam}: {label}", [
            (pct(m["by_case_detail"][c]["recall@20"], False) + " / "
             + pct(m["by_case_detail"][c]["in_shortlist"]))
            if c in m.get("by_case_detail", {}) else "–" for m in ms]))

    out += ["", "## Near-misses let in", "",
            ("Profiles that fail exactly one must-have and look right otherwise, by the "
            "must-have they fail: share that reached the top 10. "
            f"{ms[0].get('near_planted', 0)} of {sum(s['near'] for s in pool.values())} "
            "were planted as look-alikes; the rest are background profiles that happen to "
            "fail exactly one must-have."), "",
            "| Fails | " + " | ".join(f"`{n}`" for n in names) + " |",
            "|---|" + "---|" * len(names)]
    musts = sorted({k for m in ms for k in m.get("near_miss_by_must", {})},
                   key=lambda k: list(MUST_LABEL).index(k))
    for k in musts:
        out.append(_row(MUST_LABEL[k], [pct(m["near_miss_by_must"][k]["in_top10"])
                                        if k in m.get("near_miss_by_must", {}) else "–"
                                        for m in ms]))

    for r in runs:
        mr = r["metrics"].get("must_reading")
        if not mr:
            continue
        out += ["", f"## How `{r['matcher']}` read the must-haves", "",
                ("Every judgement the matcher returned, against the rule applied to the hidden "
                "facts. \"unklar\" counts as not right."), "",
                "| Must-have | right | wrong | unklar |", "|---|---|---|---|"]
        for k, c in mr.items():
            out.append(f"| {MUST_LABEL[k]} | {pct(c['right'])} | {c['wrong']} | {c['unklar']} |")

    for r in runs:
        missed = [x for e in r["per_vacancy"] for x in e["missed"]]
        if not missed:
            continue
        out += ["", f"## Fits `{r['matcher']}` left off the shortlist ({len(missed)})", "",
                ("| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; "
                "misread must-haves) |"), "|---|---|---|---|---|---|"]
        for x in missed[:20]:
            mis = ", ".join(MUST_LABEL[m] for m in x["misread"])
            why = (x["matcher_note"] or "–").replace("|", "/")
            out.append(f"| {x['vacancy']} | {x['id']} | {x['case']} | {x['title']} | "
                       f"{x['rank']} | {why[:160]}{'; misread: ' + mis if mis else ''} |")
        if len(missed) > 20:
            out.append(f"| … | {len(missed) - 20} more in `run.json` | | | | |")

    for r in runs:
        fps = [x for e in r["per_vacancy"] for x in e["false_positives"]
               if x["near_miss"]]
        if not fps or not r["metrics"]["shortlist"]["own"]:
            continue
        out += ["", f"## Near-misses `{r['matcher']}` put on its shortlist ({len(fps)})", "",
                "| Vacancy | Profile | Fails | Rank | Matcher's words |", "|---|---|---|---|---|"]
        for x in fps[:12]:
            note = (x["matcher_note"] or "–").replace("|", "/")
            out.append(f"| {x['vacancy']} | {x['id']} | {MUST_LABEL[x['near_miss']]} | "
                       f"{x['rank']} | {note[:160]} |")

    fair = [(r["matcher"], r["fairness"]) for r in runs if r["fairness"]]
    if fair:
        out += ["", "## Does the name move the ranking?", "",
                ("The pool is ranked again unchanged (repeat) and with every name swapped to "
                 "another origin, same gender, the surname in the notes included (swap). "
                 "Graded: the base run's top 50 per vacancy, and whether each stays in or out "
                 "of the top 10 and, where the matcher gives one, of its own yes-list. A swap "
                 "flip rate above the repeat rate points at the name. Matchers that never read "
                 "the name (bm25, keyword, field-filter) are at 0 by construction."), "",
                ("| Matcher | Top-10 flips on swap | on repeat | Own-list flips on swap | "
                 "on repeat | Mean rank shift swap / repeat |"),
                "|---|---|---|---|---|---|"]
        for name, f in fair:
            own_s, own_r = f.get("own_list_flips_on_swap"), f.get("own_list_flips_on_repeat")
            out.append(f"| `{name}` | {pct(f['top10_flips_on_swap'])} | "
                       f"{pct(f['top10_flips_on_repeat'])} | "
                       f"{pct(own_s) if own_s else '–'} | {pct(own_r) if own_r else '–'} | "
                       f"{f['mean_rank_shift_on_swap']} / {f['mean_rank_shift_on_repeat']} |")
        origins = sorted({g for _, f in fair for g in f["lost_top10_place"]})
        out += ["", ("Lost a top-10 place, by origin: every base/swap pair tests both "
                     "origins involved and counts against the side left out while the other "
                     "got in. Without a name effect every origin sits near the repeat rate."), "",
                "| Origin | " + " | ".join(f"`{n}`" for n, _ in fair) + " |",
                "|---|" + "---|" * len(fair)]
        for g in origins:
            out.append(_row(g, [pct(f["lost_top10_place"].get(g)) for _, f in fair]))

    if result.get("usage"):
        u = result["usage"]
        out += ["", "## Cost", "",
                (f"{u['calls']} model calls ({u['attempts']} attempts incl. retries), "
                 f"{u['input_tokens']:,} input and {u['output_tokens']:,} output tokens, "
                 f"served by " + ", ".join(f"{k} ({v})" for k, v in u["served_by"].items())
                 + f". List-price equivalent reported by the CLI: ${u['list_price_usd']:.2f}.")]
    out += [
        "", "## How this was measured", "",
        ("Every profile is synthetic: hidden facts (trade, years, certificates, licence, town, "
         "shift and on-call willingness) and a presentation of those facts as an ATS record, "
         "with some fields left empty and the fact stated only in messy recruiter notes, and "
         "the trade shown by its official name or an old name, synonym or abbreviation. The "
         "true fits of each vacancy follow from its must-have rules applied to the hidden facts. "
         "Planted per vacancy: 4 plain, 4 synonym and 4 buried fits, and 2 near-misses per "
         "must-have; background profiles that would fit are redrawn. A profile planted for "
         "one vacancy (as fit or near-miss) can be a true fit for another and is counted "
         "there too. Certificate lists are complete: a certificate not named is absent. "
         "Distances are computed and shown to the model, so its Entfernung judgements are "
         "not a reading test. No real candidate data is involved."),
        "",
    ]
    return "\n".join(out)
