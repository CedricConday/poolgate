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
   - 4 **plain**: official trade name in the Beruf field, every fact in its field;
   - 4 **synonym**: the Beruf field shows another name for the same
     qualification: an official predecessor name with its year ("Betriebsschlosser
     (bis 1987)", "Elektroinstallateur (bis 2003)"), the official long form, or a
     common abbreviation of the official name ("Elektroniker BT"). Job titles
     and unofficial names are not used;
   - 4 **buried**: one must-have fact is "k. A." in its field and stated only in
     the notes, one fit for each must-have other than distance (trade, years,
     and per vacancy certificate, shift, licence or on-call);

   and 2 **near-misses** per must-have: profiles that meet every must-have but
   one (no licence, 80 km away, a Kfz-Mechatroniker for a Mechatroniker job,
   S7 never used, nights refused), with the failing fact usually in the notes.
   Background profiles that would fit are redrawn, so every true fit is known.
   Certificate lists, in the field and in the notes, are declared complete: a
   certificate not named is absent, not unknown.
2. **Present.** Each profile is rendered as an ATS record: structured fields,
   some empty, and free-text notes in the way recruiters write them (call
   shorthand, CV snippets, abbreviations, typos in filler words).
3. **Truth.** The fits of a vacancy follow from its must-have rules applied to
   the hidden facts, never from the text. Tests check that every fact left
   empty in a field is stated in the notes.
4. **Match and grade.** Every matcher ranks the whole pool for each vacancy. The
   gate reports recall@10 and @20, precision@10, the matcher's own shortlist
   (precision and recall), near-misses in the top 10, and recall per hard case,
   each with a 95% Wilson interval. When the matcher reports its reading of each
   must-have, every missed fit is listed with the must-have it misread.
5. **Swap.** The pool is ranked again unchanged (the chance baseline) and twice
   with every name swapped to another origin, same gender, the surname in the
   notes included. Names are one token each, so the text keeps its token count.
   For the base run's top 50, the gate counts how often top-10 membership flips,
   and, where the matcher gives one, membership of its own yes-list. A flip rate
   above the repeat rate points at the name; per origin, the gate counts who lost
   a top-10 place. Matchers that never read the name (`bm25`, `keyword`,
   `field-filter`) score 0 here by construction.

The three vacancies: Elektroniker für Betriebstechnik in Paderborn (3-Schicht,
S7/TIA, 35 km), CNC-Fräser in Gütersloh (2-Schicht, Heidenhain, 30 km),
Servicetechniker Sicherheitstechnik in Bielefeld (licence, on-call, 50 km).
A profile planted for one vacancy, as a fit or as a near-miss, sometimes fits
another and counts there too: 14, 12 and 14 true fits, 40 in all, on 37
distinct profiles, so the fits are not fully independent. With more fits than
places, recall@10 cannot exceed 75%.

## Matchers

| Matcher | What it does |
|---|---|
| `bm25` | BM25 keyword search over the whole record |
| `keyword` | the same, behind a soft field filter: a record whose filled field contradicts a must-have (too far, too few years, "Führerschein: keiner") moves behind the rest; empty fields never exclude |
| `field-filter` | strict filter on structured fields, as an ATS filter panel would; its shortlist is the records that pass |
| `claude` | the `keyword` top 50, read in full by Claude Opus 5.5 in batches of 10; Claude judges each must-have per candidate (structured output), the shortlist is the candidates it judges as meeting all of them |
| HTTP | any matcher behind one endpoint, see below |

The Claude reranker is a reference built the way such a preselection is commonly
built (cheap search, then a model reads the top N). It is not a claim about any
vendor's pipeline or prompt.

## Proof the gate sees each failure

An offline stand-in reads the hidden facts and has one knob per failure, so the
gate can be shown to catch each one before it is pointed at a real matcher.
Same pool, seed 7 ([report](results/offline-proof/report.md)):

| Planted fault | Recall@20 | Synonym fits shortlisted | Buried fits shortlisted | Near-misses in top 10 | Top-10 flips on swap | on repeat | Lost a top-10 place |
|---|---|---|---|---|---|---|---|
| none | 100% | 100% | 100% | 0% | 0% | 0% | nobody |
| misses synonym fits (p=0.5) | 85% | 43% | 100% | 0% | 0% | 0% | nobody |
| misses buried facts (p=0.5) | 88% | 100% | 58% | 0% | 0% | 0% | nobody |
| takes near-misses for fits (p=0.5) | 48% | 100% | 100% | 15% | 0% | 0% | nobody |
| downgrades Turkish and Arabic names | 95% | 79% | 83% | 0% | 13% | 0% | tr 27/101, ar 10/63, de 1/231 |
| random score noise (±25) | 98% | 93% | 100% | 0% | 12% | 12% | spread over all origins |

Each fault lands in its own column. Noise raises swap and repeat flips alike and
spreads the losses over every origin; a name bias raises only the swap flips
and puts the losses on the penalised origins. These are numbers about the gate,
not about any real matcher.

## Results

Same pool, seed 7, three vacancies, 40 true fits ([report](results/claude-opus-5-5/report.md),
[pool with hidden truth](results/claude-opus-5-5/pool.json)). Claude Opus 5.5, effort medium,
through the claude CLI; keyword top 50 per vacancy, 10 candidates per call.

| Measure | `keyword` | `field-filter` | `claude` |
|---|---|---|---|
| Recall@10 (ceiling 75%) | 40% [26–55] | 35% [22–50] | 75% [60–86] |
| Recall@20 | 68% [52–80] | 48% [33–63] | 95% [83–99] |
| Precision@10 | 53% [36–70] | 47% [30–64] | 100% [89–100] |
| Shortlist precision | 53% (16/30, top 10) | 100% (14/14) | 100% (38/38) [91–100] |
| Shortlist recall | 40% (16/40) | 35% (14/40) | 95% (38/40) [83–99] |
| Near-misses in top 10 | 9 of 143 | 7 of 143 | 0 of 143 (47 reached the model, all rejected) |
| Shortlist recall, synonym fits | 29% (4/14) | 0% (0/14) | 93% (13/14) |
| Shortlist recall, buried fits | 17% (2/12) | 0% (0/12) | 92% (11/12) |
| Top-10 flips on name swap / on repeat | 0% / 0% (by construction) | 0% / 0% (by construction) | 3% (8/300) / 4% (6/150) |
| Own-list flips on name swap / on repeat | – | 0% / 0% | 0% (0/300) / 0% (0/150) |

Pure BM25 without the field filter: recall@20 32%, shortlist recall 15%. Of
the 143 near-misses, 30 were planted look-alikes; 113 are background profiles
that happen to fail exactly one must-have.

What the numbers say, within their intervals:

- The field filter is precise and blind to the notes: it shortlists every plain
  fit and no synonym or buried fit. Keyword search finds some of them, but
  ranks near-misses next to fits, because "kein Führerschein" contains
  "Führerschein".
- The Claude reranker shortlisted 38 of 40 fits and no non-fit. Of the 47
  near-misses that reached it, it let none in. All 750 of its must-have
  judgements matched the rules, none "unklar". The 150 distance judgements are
  not a reading test, because the distance is computed and shown on each record.
- Both of its misses never reached it. They ranked 73 and 113 in the keyword
  prefilter for the Bielefeld vacancy, which accepts four trades, so the keyword
  ranking spreads thin there. Within what the prefilter passed, recall was 38
  of 38. The weak point of this design is the prefilter, not the model.
- No name effect is visible. Top-10 flips on swap (3%) are within the repeat
  rate (4%), the yes-list did not move at all, and no origin lost more than 3
  top-10 places in about 100 tests. An effect of a few percent would not show
  at this sample size.

Changes from the first live run ([run 1](results/claude-opus-5-5-run1/report.md)),
which used an earlier pool. That pool listed job titles ("Servicetechniker
Mechatronik", "CNC-Fräser") and unofficial names as trade synonyms. It also did
not declare certificate lists complete, and it had no buried shift or on-call
fit. Claude answered "unklar" on the job titles, and 4 of its 6 misses came
from that: shortlist recall was 85% (34/40), with 13 "unklar" judgements. With
the pool fixed, shortlist recall is 95% and nothing is "unklar". The prefilter
misses (2) are the same in both runs.

Cost: 60 calls (15 for the ranking, 45 for the repeat and the two swap runs),
388k input and 164k output tokens, $5.28 at list price as reported by the CLI
(run 1: $5.34). No call needed a retry.

## Use

```bash
pip install -e ".[dev]"

# offline, no model: the proof table and the keyword baselines
poolgate proof
poolgate run --matchers bm25,keyword,field-filter --dump-pool

# the Claude reranker, through the claude CLI on a Claude subscription (no API key)
poolgate run --matchers keyword,claude --top-n 50 --batch 10 --workers 3

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
  facts that are simply missing. Here every fact is stated somewhere and never
  contradicted, so the truth is recoverable by construction.
- Synonyms are official names only: long forms, predecessor names with the
  year, and abbreviations of the official name. A real pool is full of job
  titles and ambiguous words ("Elektriker", "CNC-Fräser", "Servicetechniker")
  that leave the trade genuinely unknown. A matcher should flag those for a
  recruiter, and grading that needs a third outcome. It is not modelled here.
- Certificate lists are declared complete, so a certificate not named is
  absent. Real records rarely say "sonst keine". There, an unstated certificate
  is unknown, and "unklar" would be the right answer.
- The reranker turns "unklar" into "not a fit". That is a choice of the
  reference matcher, not of the gate: a matcher that returns a third bucket
  can be graded on it through `shortlist` and `note`.
- Three vacancies and 40 true fits on 37 distinct profiles (a profile can fit
  two vacancies): per-case rows rest on 12 to 14 fits and the buried subtypes on
  1 to 3, so their intervals are wide. Read the brackets.
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

## License

MIT
