# poolgate

A recovery gate for talent-pool matching. It plants known fits and near-misses
in a synthetic candidate pool, matches a vacancy against the pool, and scores
how many of the true fits reach the shortlist, which near-misses get in, who is
missed and why, and whether the ranking moves when only the names change.

Talent-pool products sell a large maintained pool plus an AI preselection that
turns a vacancy into an interview-ready shortlist, often for
gewerblich-technische roles in the Mittelstand, with pools in the tens of
thousands of profiles. The pool is
only worth its size if matching finds the people in it. The candidates that
are hard to find are the ones that cost a hire: a fit whose CV says
"Energieelektroniker Fachrichtung Betriebstechnik" instead of
"Elektroniker für Betriebstechnik", a fit whose shift willingness is in a phone note and not in
the field, and the candidate who looks right but has no licence or lives 80 km
away. None of this shows in a demo search. It shows in rates, over a pool whose
true fits are known in advance. poolgate does not test any vendor's product; it
is the harness one would use to.

## How it works

1. **Plant.** A pool of 400 synthetic profiles in OWL (Elektroniker,
   Mechatroniker, Industriemechaniker, Zerspanungsmechaniker and others), each a
   set of hidden facts: trade, years after the apprenticeship, certificates,
   licence, town, shift and on-call willingness, salary, availability, last
   contact. Per vacancy, 12 true fits are planted:
   - 4 **plain**: the official title of the Ausbildungsordnung in the Beruf
     field ("Elektroniker für Betriebstechnik", "Elektroniker, Fachrichtung
     Energie- und Gebäudetechnik"), every fact in its field;
   - 4 **synonym**: the Beruf field shows another name for the same
     qualification, one of three kinds, graded separately:
     a *spelling variant* ("Industriemechaniker/-in", "Mechatroniker (IHK)",
     "Elektroniker für Energie- und Gebäudetechnik" for the Fachrichtung
     title), an *abbreviation* ("Elektroniker BT", "Industriemech.") or a
     *predecessor name* ("Energieelektroniker Fachrichtung Betriebstechnik",
     "Elektroinstallateur", "Betriebsschlosser"). The four slots cycle through
     the kinds. Job titles and unofficial names are not used;
   - 4 **buried**: one must-have fact is "k. A." in its field and stated only in
     the notes, one fit for each must-have other than distance (trade, years,
     and per vacancy certificate, shift, licence or on-call);

   and 2 **near-misses** per must-have: profiles that meet every must-have but
   one (no licence, 80 km away, a Kfz-Mechatroniker for the Bielefeld service job,
   S7 never used, nights refused), with the failing fact usually in the notes.
   Background profiles that would fit are redrawn, so every true fit is known.

   Every trade name, in the field and in the notes, was in use when the
   candidate's training started: today's name from its reform year on (2003 for
   the Elektroniker trades, 1998 for Mechatroniker, 1987 for the metal trades
   ...), the predecessor before. Reform years are checked against BIBB's
   yearly lists of new and modernised occupations; the sources are cited in
   `poolgate/pool.py`. Careers run up to 41 years, and are capped where a trade
   has no sourced predecessor, so no training predates its name. Notes name the
   exam the way the trade takes it: Gesellenprüfung at the Handwerkskammer for
   Elektroniker E+G, Informationselektroniker, Anlagenmechaniker SHK and most
   Kfz-Mechatroniker, Abschluss IHK for the industry trades.

   **Dates.** The structured fields and the truth describe the career on the
   pool's Stand, 15.11.2026. Each note is dated (the last contact) and describes
   the career on that day. Trainings end in summer, and experience counts in
   whole years from 1 July of the final year. So no note is dated before the
   training ended; a duration in a note ("BE: 1 Jahr" on 12.09.25) is the
   experience on the note's date and has grown since; and where the experience
   field is empty, the note names the season and year the training ended
   ("seit Sommer 2024 im Beruf"), which fixes today's value exactly. A test
   checks every duration and every year in the notes of five pool seeds against
   this rule. Certificate lists, in the field and in the notes, are declared
   complete: a certificate not named is absent, not unknown.
2. **Present.** Each profile is rendered as an ATS record: structured fields,
   some empty, and free-text notes in the way recruiters write them (call
   shorthand, CV snippets, abbreviations, typos in filler words).
3. **Truth.** The fits of a vacancy follow from its must-have rules applied to
   the hidden facts, never from the text. Tests check that every fact left
   empty in a field is stated in the notes.
4. **Match and grade.** Every matcher ranks the whole pool for each vacancy. The
   gate reports recall at k = the number of true fits (every matcher gets a list
   as long as the answer, so the ceiling is 100% for all), recall@20 and @10,
   precision@10, the matcher's own shortlist (precision and recall), near-misses
   in the top 10, and recall per hard case, each with a 95% Wilson interval.
   When the matcher reports its reading of each must-have, every missed fit is
   listed with the must-have it misread.
5. **Swap.** The pool is ranked again unchanged (the chance baseline) and twice
   with every name swapped to another origin, same gender, the surname in the
   notes included. Names are one token each, so the text keeps its token count.
   For the base run's top 50, the gate counts how often top-10 membership flips,
   and, where the matcher gives one, membership of its own yes-list. A flip rate
   above the repeat rate points at the name; per origin, the gate counts who lost
   a top-10 place. Matchers that never read the name (the keyword and filter
   baselines) score 0 here by construction.

The three vacancies: Elektroniker für Betriebstechnik in Paderborn (3-Schicht,
S7/TIA, 35 km), CNC-Fräser in Gütersloh (2-Schicht, Heidenhain, 30 km),
Servicetechniker Sicherheitstechnik in Bielefeld (licence, on-call, 50 km).
A profile planted for one vacancy, as a fit or as a near-miss, sometimes fits
another and counts there too. With seed 7 that gives 12, 12 and 15 true fits,
39 in all, on 37 distinct profiles; with seed 8, 12 each, 36 on 36 profiles.
The fits are therefore not fully independent. With more fits than places,
recall@10 cannot exceed 77% on seed 7 (30 of 39) and 83% on seed 8 (30 of 36).

## Matchers

| Matcher | What it does |
|---|---|
| `bm25` | BM25 keyword search over the whole record |
| `keyword` | the same, behind a soft field filter: a record whose filled field contradicts a must-have (too far, too few years, "Führerschein: keiner") moves behind the rest; empty fields never exclude |
| `keyword+syn` | `keyword` with query expansion: every word of every name of the accepted trades in the generator's synonym table, each once |
| `field-filter-exact` | strict filter on structured fields, as an ATS filter panel would, Beruf compared as an exact string; its shortlist is the records that pass |
| `field-filter` | the same, Beruf spelling normalised first (case, spacing, "/-in", "(IHK)", the "Fachrichtung" form) |
| `field-filter+syn` | the same, accepting every name in the synonym table (variants, abbreviations, predecessor names) |
| `claude` | the `keyword` top 50, read in full by Claude Opus 5.5 in batches of 10; Claude judges each must-have per candidate (structured output), the shortlist is the candidates it judges as meeting all of them |
| `claude@keyword+syn` | the same reader behind the `keyword+syn` top 50 (`--prefilter keyword+syn`) |
| HTTP | any matcher behind one endpoint, see below |

The `+syn` baselines get the generator's own table, which is more than a real
search has: they are an upper bound for synonym handling by lookup, not a
typical system. The Claude reranker is a reference built the way such a
preselection is commonly built (cheap search, then a model reads the top N).
It runs behind either prefilter; the two are reported as separate columns. It is not a claim
about any vendor's pipeline or prompt.

## Proof the gate sees each failure

An offline stand-in reads the hidden facts and has one knob per failure, so the
gate can be shown to catch each one before it is pointed at a real matcher.
Same pool, seed 7 ([report](results/offline-proof/report.md)):

| Planted fault | Recall@20 | Synonym fits shortlisted | Buried fits shortlisted | Near-misses in top 10 | Top-10 flips on swap | on repeat | Lost a top-10 place |
|---|---|---|---|---|---|---|---|
| none | 100% | 100% | 100% | 0% | 0% | 0% | nobody |
| misses synonym fits (p=0.5) | 82% | 38% | 100% | 1% | 0% | 0% | nobody |
| misses buried facts (p=0.5) | 87% | 100% | 58% | 0% | 0% | 0% | nobody |
| takes near-misses for fits (p=0.5) | 49% | 100% | 100% | 16% | 0% | 0% | nobody |
| downgrades Turkish and Arabic names | 95% | 77% | 83% | 0% | 12% | 0% | tr 25/100, ar 9/71, de 2/207 |
| random score noise (±25) | 97% | 92% | 100% | 0% | 10% | 11% | spread over all origins |

Each fault lands in its own column. Noise raises swap and repeat flips alike and
spreads the losses over every origin; a name bias raises only the swap flips
and puts the losses on the penalised origins. These are numbers about the gate,
not about any real matcher.

## Results

Claude Opus 5.5, effort medium, through the claude CLI; top 50 per vacancy,
10 candidates per call; every baseline on the same pool. Two pools: seed 7
([report](results/claude-opus-5-5/report.md),
[pool with hidden truth](results/claude-opus-5-5/pool.json)) and seed 8
([report](results/claude-opus-5-5-seed8/report.md),
[pool](results/claude-opus-5-5-seed8/pool.json)). Run 5 is the reranker behind
the literal keyword prefilter; run 6 is the same reader behind the
synonym-aware prefilter, on the same two pools
([seed 7](results/claude-opus-5-5-presyn/report.md),
[seed 8](results/claude-opus-5-5-seed8-presyn/report.md)).

Equal footing first: recall at k = the number of true fits per vacancy, so
every matcher gets a list exactly as long as the answer and the ceiling is
100%. Brackets are 95% Wilson intervals.

| Recall at k = fits | seed 7 (39 fits) | seed 8 (36 fits) | both (75) |
|---|---|---|---|
| `keyword` | 59% (23/39) [43–73] | 50% (18/36) [34–66] | 55% [43–65] |
| `keyword+syn` | 56% (22/39) [41–71] | 67% (24/36) [50–80] | 61% [50–72] |
| `field-filter-exact` | 41% (16/39) [27–57] | 42% (15/36) [27–58] | 41% [31–53] |
| `field-filter` | 54% (21/39) [39–68] | 53% (19/36) [37–68] | 53% [42–64] |
| `field-filter+syn` | 72% (28/39) [56–83] | 72% (26/36) [56–84] | 72% [61–81] |
| `claude` | 92% (36/39) [80–97] | 92% (33/36) [78–97] | 92% [84–96] |
| `claude@keyword+syn` | 100% (39/39) [91–100] | 100% (36/36) [90–100] | 100% [95–100] |

The "both" column pools the two seeds; fits within a seed are not fully
independent, so read its interval as slightly too narrow.

| Measure, seed 7 / seed 8 | `keyword` | `keyword+syn` | `field-filter` | `field-filter+syn` | `claude` | `claude@keyword+syn` |
|---|---|---|---|---|---|---|
| Recall@20 (ceiling 100%) | 74% / 78% | 77% / 83% | 62% / 64% | 74% / 75% | 92% / 92% | 100% / 100% |
| Shortlist precision | 57% / 57% (top 10) | 57% / 67% (top 10) | 100% / 100% | 100% / 100% | 100% / 100% (36/36, 33/33) | 100% / 100% (39/39, 36/36) |
| Shortlist recall | 44% / 47% (top 10; ceiling 77% / 83%) | 44% / 56% (top 10) | 49% / 44% | 69% / 67% | 92% / 92% | 100% / 100% |
| Near-misses in top 10 | 13 of 145 / 10 of 143 | 13 / 8 | 8 / 9 | 1 / 2 | 0 / 1 | 0 / 0 |
| Synonym fits shortlisted | 5/13 / 3/12 | 6/13 / 8/12 | 5/13 / 4/12 | 13/13 / 12/12 | 11/13 / 10/12 | 13/13 / 12/12 |
| · spelling variant | 3/5 / 1/4 | 2/5 / 0/4 | 5/5 / 4/4 | 5/5 / 4/4 | 5/5 / 4/4 | 5/5 / 4/4 |
| · abbreviation | 1/3 / 0/1 | 1/3 / 1/1 | 0/3 / 0/1 | 3/3 / 1/1 | 3/3 / 1/1 | 3/3 / 1/1 |
| · predecessor name | 1/5 / 2/7 | 3/5 / 7/7 | 0/5 / 0/7 | 5/5 / 7/7 | 3/5 / 5/7 | 5/5 / 7/7 |
| Buried fits shortlisted | 3/12 / 7/12 | 4/12 / 6/12 | 0/12 / 0/12 | 0/12 / 0/12 | 11/12 / 11/12 | 12/12 / 12/12 |
| Top-10 flips on name swap / on repeat | 0 (by construction) | 0 | 0 | 0 | 3% (8/300) / 3% (4/150); 2% (6/300) / 3% (4/150) | 3% (8/300) / 3% (4/150); 2% (6/300) / 3% (4/150) |
| Own-list flips on name swap / on repeat | – | – | 0 | 0 | 0/300 / 0/150 on both seeds | 0/300 / 0/150 on both seeds |

`bm25` alone: 26% / 22% at k = fits. `field-filter-exact` shortlists no
synonym fit on either seed, and misses the plain Elektroniker E+G fit on seed 7
because the official title differs from the name in the posting; normalising
the spelling adds 5 and 4 synonym fits (all the spelling variants), the
synonym table another 8 and 8.

What the numbers say, within their intervals:

- Behind the literal keyword prefilter (run 5) the reranker found 92% of the
  fits on both pools, against 72% for the best baseline, a field filter that
  knows every name in the generator's table. The intervals do not overlap on
  the pooled seeds (84–96 against 61–81); on each seed alone they overlap
  slightly (80–97 against 56–83, 78–97 against 56–84).
- Its weak point was the prefilter. All six of its misses never reached the
  model: Bielefeld fits whose Beruf field shows a predecessor name
  (Elektroinstallateur, Radio- und Fernsehtechniker), at keyword ranks 69 to
  112. Every fit the prefilter passed was shortlisted (36 of 36, 33 of 33).
- With the synonym-aware prefilter (run 6) every fit reached the model on both
  pools, and the model shortlisted all of them: 39 of 39 and 36 of 36, 100%
  [95–100] pooled, with 100% shortlist precision. More near-misses reached it
  (53 and 50, against 54 and 45 before); it admitted none. Its top 10 held no
  near-miss on either seed.
- That 100% has a ceiling built in: `keyword+syn` expands the query with the
  generator's own table, so on these pools its top 50 holds every fit (39 of
  39, 36 of 36, against 36 and 33 for the literal prefilter). A real prefilter's
  table is incomplete, and the reader can only be as good as what it is given.
  On its own, `keyword+syn` is a mediocre ranker (56% and 67% at k = fits); as
  a wide net for a model it was enough here.
- The field filters are exact and blind to the notes: 100% precision, no buried
  fit. Given the synonym table, the filter shortlists every synonym fit (25/25);
  the reranker behind the literal prefilter got 21/25, behind the expanded one
  25/25. Keyword search finds some buried fits but ranks near-misses next to
  fits, because "kein Führerschein" contains "Führerschein".
- Reading errors were rare and all on non-fits. Of 750 must-have judgements per
  seed and run: run 5 seed 7 none wrong; run 5 seed 8 one wrong (Beruf
  "erfüllt" for a Maschinen- und Anlagenführer whose reason says the opposite)
  and one "unklar" (experience, where the note says "Ausgelernt Sommer 2024");
  run 6 two and one wrong, all experience: the model counted from a dated
  note's "noch keine BE" and concluded under two years where the truth is two
  (twice it overrode an experience field that showed 2). Date arithmetic at the
  boundary is its one recurring slip. The 150 distance judgements per seed are
  not a reading test, because the distance is computed and shown on each
  record.
- Name swap: top-10 flips on swap (3%, 2%) are at the repeat rate (3%, 3%) in
  both runs, and the yes-list did not move in 1,200 swaps or 600 repeats. This
  is no evidence of a name effect, and too small a sample to exclude one of a
  few percent.

**Pool to pool.** The baselines cost nothing, so they were run on five pools
(seeds 7 to 11, [report](results/offline-seeds/report.md)): rate pooled over
all five, then the range of single seeds.

| Matcher | Recall at k = fits | Shortlist recall | Shortlist precision |
|---|---|---|---|
| `keyword` | 51% [44–57]; 42–59% | 40% [34–47]; 36–47% | 53% [45–61]; 50–57% |
| `keyword+syn` | 57% [50–63]; 45–67% | 44% [37–51]; 32–56% | 58% [50–66]; 43–70% |
| `field-filter-exact` | 42% [35–49]; 40–46% | 34% [28–41]; 31–39% | 100% |
| `field-filter` | 51% [44–58]; 45–54% | 47% [41–54]; 43–52% | 100% |
| `field-filter+syn` | 71% [64–77]; 69–72% | 69% [62–75]; 67–71% | 100% |

Keyword search moves by up to 17 points from one pool to the next, 22 with
query expansion, so a difference of that size between two keyword
configurations on one pool means little. The filters are stable within a few points. Claude was run on two of
the five pools only, for cost.

**Run history.** Each run used a different pool, because each round of fixes
changes the generator, and each is a fresh model sample at the same settings.
So the changes between runs come from the fixes, the redrawn pool and sampling
together, not from the fixes alone.

| Run | Pool | Shortlist recall | "unklar" | Misses |
|---|---|---|---|---|
| [run 1](results/claude-opus-5-5-run1/report.md) | job titles among trade synonyms, certificate lists not declared complete, no buried shift/on-call | 85% (34/40) | 13 | 4 on job titles, 2 not past the prefilter |
| [run 2](results/claude-opus-5-5-run2/report.md) | official names only, but predecessor names regardless of training year | 95% (38/40) | 0 | 2 not past the prefilter |
| [run 3](results/claude-opus-5-5-run3/report.md) | predecessor names checked, current names not: 81 profiles carry a name newer than their training | 100% (39/39) | 1 | none |
| [run 4](results/claude-opus-5-5-run4/report.md) | every shown name valid for the training-start year, reform years sourced; notes could predate the training | 97% (38/39) | 1 | 1 not past the prefilter |
| run 5, seed 7 | official titles for plain fits, synonym kinds planted in turn, notes dated after the training, Gesellenprüfung for Handwerk; prompt says notes are dated | 92% (36/39) | 0 | 3 not past the prefilter |
| run 5, seed 8 | the same, second pool | 92% (33/36) | 1 | 3 not past the prefilter |
| [run 6](results/claude-opus-5-5-presyn/report.md), seed 7 | run 5's pool; prefilter `keyword+syn` | 100% (39/39) | 0 | none |
| [run 6](results/claude-opus-5-5-seed8-presyn/report.md), seed 8 | run 5's pool; prefilter `keyword+syn` | 100% (36/36) | 0 | none |

Run 5 is lower than run 4 (92% against 97% on seed 7). The model did not get
worse at reading: every fit that reached it was shortlisted, as in run 4. The
pool got harder for the prefilter: synonym slots now plant predecessor names on
purpose (5 and 7 synonym fits with a predecessor name, against 3 in run 4), and
the literal keyword prefilter ranks those low for the Bielefeld vacancy, which
accepts four trades. In run 2, 7 true fits carried a predecessor name retired
before their training ended; Claude noted the contradiction on two of them but
still accepted them. Run 6 changes only the prefilter, on run 5's pools and
with run 5's prompt, so the step from 92% to 100% is the prefilter plus a fresh
model sample.

Cost of run 5: 120 calls (per seed 15 for the ranking, 45 for the repeat and the
two swap runs), 785k input and 334k output tokens, $10.34 at list price as
reported by the CLI ($5.12 and $5.22; runs 1 to 4: $5.34, $5.28, $5.24, $5.15).
No call needed a retry. A first run on both seeds, on the pool before notes
named the season wherever experience was only in the notes, cost another $10.50;
it exposed that gap (the model rightly answered "unklar" on "seit 2024 im
Beruf") and was discarded once the generator was fixed. Run 6: 120 calls, 777k
input and 330k output tokens, $10.19 ($5.06 and $5.13), no retries.

## Use

```bash
pip install -e ".[dev]"

# offline, no model: the proof table, the baselines, the baselines over five pools
poolgate proof
poolgate run --matchers bm25,keyword,keyword+syn,field-filter-exact,field-filter,field-filter+syn --dump-pool
poolgate seeds --seeds 7,8,9,10,11

# the Claude reranker, through the claude CLI on a Claude subscription (no API key)
poolgate run --seed 7 --matchers keyword,claude --top-n 50 --batch 10 --workers 3
# the same reader behind the synonym-aware prefilter
poolgate run --seed 7 --matchers keyword+syn,claude --prefilter keyword+syn --top-n 50

# your own matcher, behind HTTP, next to the keyword baseline
poolgate run --matchers keyword --matcher-url http://localhost:8080
```

Each run writes `report.md` (one page) and `run.json` (rankings, every missed
fit, every model answer, fairness runs, usage); `--dump-pool` adds `pool.json`,
every record as the matcher sees it plus the hidden truth.

An HTTP matcher answers one call:

```
POST {url}/rank
{"vacancy": {...}, "profiles": [{...}, ...]}
-> {"ranking": [{"id": "p0042", "score": 0.93, "shortlist": true,
                 "note": "...", "musts": {"beruf": "erfüllt", ...}}, ...]}
```

Best first; omitted profiles rank last; `shortlist`, `note` and `musts` are
optional. With `shortlist` the matcher's own list is graded; with `musts`
("erfüllt", "nicht erfüllt", "unklar" per must-have) every missed fit shows
which must-have was misread. The swap runs send the same pool with other names,
so a matcher that caches by id must not reuse results across calls.

## Limits

- The pool is synthetic, and so is its messiness. Real notes are messier in
  ways not modelled here: contradictions between field and note, stale facts,
  facts that are simply missing. Here every fact is stated somewhere, so the
  truth is recoverable by construction.
- Every training ends in summer, and the facts other than experience (shift,
  licence, town ...) are the same on the note's date as at the Stand. Real
  trainings also end in winter, and people move or lose a licence between a
  call and today; a matcher would have to treat an old note as possibly stale.
- Synonyms are official titles, their spelling variants, common abbreviations
  of them and predecessor titles (shown only where valid for the training
  years, without a date label). A real pool is full of job
  titles and ambiguous words ("Elektriker", "CNC-Fräser", "Servicetechniker")
  that leave the trade genuinely unknown. A matcher should flag those for a
  recruiter, and grading that needs a third outcome. It is not modelled here.
- The `+syn` baselines and the generator share one synonym table, so the
  synonym filter's recall on synonym fits is perfect by construction; a real
  lookup table is never
  complete. Read their columns as the best a lookup can do, not as a typical
  ATS. The reranker gets no table; it names the trade from its own knowledge.
- Run 6's prefilter uses the generator's synonym table, so on these pools it
  passes every fit by construction. Its 100% measures the reader given a
  complete candidate list, not a deployable prefilter.
- Certificate lists are declared complete, so a certificate not named is
  absent. Real records rarely say "sonst keine". There, an unstated certificate
  is unknown, and "unklar" would be the right answer.
- The reranker turns "unklar" into "not a fit". That is a choice of the
  reference matcher, not of the gate: a matcher that returns a third bucket
  can be graded on it through `shortlist` and `note`.
- Three vacancies per pool and 36 to 39 true fits on 36 or 37 distinct
  profiles (a profile can fit two vacancies): per-case rows rest on 12 to 15
  fits and the synonym kinds and buried subtypes on 1 to 7, so their intervals
  are wide. Claude ran on two pools; the baselines on five. Read the
  brackets.
- Distance is straight-line between town centres. The Claude reranker is given
  the distance on each record, as an ATS radius search would show it, so its
  distance judgements do not test whether it knows OWL geography.
- Name swaps hold gender fixed: German notes carry it in word forms
  (Elektronikerin, Frau ...) that a name swap cannot rewrite cleanly. A
  candidate's origin can show in other ways than the name; that is not tested.
- The must-have rules are the vacancy's stated criteria. The gate checks that a
  matcher applies them; it does not judge who would be the better hire.

## Method

The same idea as [screengate](https://github.com/CedricConday/screengate), which
plants known facts in synthetic applicants and grades what a screening bot's
summary keeps, and [bidsgate](https://github.com/CedricConday/bidsgate), which
plants known lesions in brain scans and scores what an analysis pipeline
recovers: put in an answer you know, run the system, grade what comes out.
poolgate reuses screengate's Wilson intervals, its swap-against-repeat fairness
test and its subscription backend for Claude.

## Related

Three small tools on one question: does an AI step in recruiting do what it
claims, in numbers anyone can recompute?

- [screengate](https://github.com/CedricConday/screengate): what a screening
  chatbot's summary keeps, invents, and whether its verdict moves with the name.
- [poolgate](https://github.com/CedricConday/poolgate): who a talent-pool
  matcher shortlists, who it misses, and why.
- [vakanzcheck](https://github.com/CedricConday/vakanzcheck): whether a
  vacancy's offer can fill it, on live Bundesagentur data and written-down rules.

## License

MIT
