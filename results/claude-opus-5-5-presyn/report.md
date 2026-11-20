# poolgate report

Pool: 400 synthetic profiles, seed 7, 3 vacancies. Matchers: `keyword+syn`, `claude-rerank@keyword+syn (top 50)`.

| Vacancy | True fits | of which plain / synonym / buried | Near-misses |
|---|---|---|---|
| Elektroniker für Betriebstechnik (m/w/d) Instandhaltung (Paderborn, 35 km) | 12 | 4 / 4 / 4 | 27 |
| CNC-Fräser / Zerspanungsmechaniker (m/w/d) (Gütersloh, 30 km) | 12 | 4 / 4 / 4 | 39 |
| Servicetechniker Sicherheitstechnik (m/w/d) im Außendienst OWL (Bielefeld, 50 km) | 15 | 6 / 5 / 4 | 79 |

## Headline

Brackets are 95% Wilson intervals. The first row puts every matcher on equal footing: its top k, with k the number of true fits of each vacancy, so the ceiling is 100% for all. The shortlist is the matcher's own yes-list where it gives one, else its fixed top 10, which cannot hold every fit.

| Measure | `keyword+syn` | `claude-rerank@keyword+syn (top 50)` |
|---|---|---|
| Recall at k = true fits (ceiling 100%) | 56% (22/39) [41–71] | 100% (39/39) [91–100] |
| Recall@20 (ceiling 100%) | 77% (30/39) [62–87] | 100% (39/39) [91–100] |
| Recall@10 (ceiling 77%: more fits than places) | 44% (17/39) [29–59] | 77% (30/39) [62–87] |
| Precision@10 | 57% (17/30) [39–73] | 100% (30/30) [89–100] |
| Shortlist precision | 57% (17/30) [39–73] | 100% (39/39) [91–100] |
| Shortlist recall | 44% (17/39) [29–59] (ceiling 77%) | 100% (39/39) [91–100] |
| Shortlist size (all vacancies) | 30 (top 10) | 39 |
| Near-misses in top 10 | 9% (13/145) [5–15] | 0% (0/145) [0–3] |
| Near-misses in shortlist | 13 | 0 |
| True fits that reached the model | – | 100% (39/39) [91–100] |
| Near-misses that reached the model | – | 37% (53/145) [29–45] |

## Which fits are found

Recall@20 and shortlist recall by how the fit is presented.

| Case | `keyword+syn` @20 / shortlist | `claude-rerank@keyword+syn (top 50)` @20 / shortlist |
|---|---|---|
| plain (official title, facts in fields) | 71% [45–88] / 50% (7/14) [27–73] | 100% [78–100] / 100% (14/14) [78–100] |
| synonym (Beruf field: another spelling, an abbreviation or a predecessor name) | 77% [50–92] / 46% (6/13) [23–71] | 100% [77–100] / 100% (13/13) [77–100] |
| buried (a must-have fact only in the notes) | 83% [55–95] / 33% (4/12) [14–61] | 100% [76–100] / 100% (12/12) [76–100] |
| · synonym: abbreviation | 100% [44–100] / 33% (1/3) [6–79] | 100% [44–100] / 100% (3/3) [44–100] |
| · synonym: predecessor name | 60% [23–88] / 60% (3/5) [23–88] | 100% [57–100] / 100% (5/5) [57–100] |
| · synonym: spelling variant | 80% [38–96] / 40% (2/5) [12–77] | 100% [57–100] / 100% (5/5) [57–100] |
| · buried: Beruf | 67% [21–94] / 0% (0/3) [0–56] | 100% [44–100] / 100% (3/3) [44–100] |
| · buried: Erfahrung | 100% [44–100] / 67% (2/3) [21–94] | 100% [44–100] / 100% (3/3) [44–100] |
| · buried: Führerschein | 100% [21–100] / 0% (0/1) [0–79] | 100% [21–100] / 100% (1/1) [21–100] |
| · buried: Rufbereitschaft | 0% [0–79] / 0% (0/1) [0–79] | 100% [21–100] / 100% (1/1) [21–100] |
| · buried: Schicht | 100% [34–100] / 50% (1/2) [9–91] | 100% [34–100] / 100% (2/2) [34–100] |
| · buried: Zertifikat | 100% [34–100] / 50% (1/2) [9–91] | 100% [34–100] / 100% (2/2) [34–100] |

## Near-misses let in

Profiles that fail exactly one must-have and look right otherwise, by the must-have they fail: share that reached the top 10. 30 of 145 were planted as look-alikes; the rest are background profiles that happen to fail exactly one must-have.

| Fails | `keyword+syn` | `claude-rerank@keyword+syn (top 50)` |
|---|---|---|
| Beruf | 0% (0/10) [0–28] | 0% (0/10) [0–28] |
| Erfahrung | 6% (1/17) [1–27] | 0% (0/17) [0–18] |
| Zertifikat | 6% (1/17) [1–27] | 0% (0/17) [0–18] |
| Führerschein | 25% (2/8) [7–59] | 0% (0/8) [0–32] |
| Entfernung | 0% (0/42) [0–8] | 0% (0/42) [0–8] |
| Schicht | 44% (4/9) [19–73] | 0% (0/9) [0–30] |
| Rufbereitschaft | 12% (5/42) [5–25] | 0% (0/42) [0–8] |

## How `claude-rerank@keyword+syn (top 50)` read the must-haves

Every judgement the matcher returned, against the rule applied to the hidden facts. "unklar" counts as not right.

| Must-have | right | wrong | unklar |
|---|---|---|---|
| Beruf | 100% (150/150) [98–100] | 0 | 0 |
| Erfahrung | 99% (148/150) [95–100] | 2 | 0 |
| Zertifikat | 100% (100/100) [96–100] | 0 | 0 |
| Führerschein | 100% (50/50) [93–100] | 0 | 0 |
| Entfernung | 100% (150/150) [98–100] | 0 | 0 |
| Schicht | 100% (100/100) [96–100] | 0 | 0 |
| Rufbereitschaft | 100% (50/50) [93–100] | 0 | 0 |

## Fits `keyword+syn` left off the shortlist (22)

| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; misread must-haves) |
|---|---|---|---|---|---|
| eb-paderborn | p0097 | plain | Elektroniker für Betriebstechnik | 11 | – |
| eb-paderborn | p0047 | buried:erfahrung | Elektroniker für Automatisierungstechnik | 12 | – |
| eb-paderborn | p0302 | plain | Mechatroniker | 13 | – |
| eb-paderborn | p0084 | buried:beruf | k. A. | 16 | – |
| cnc-guetersloh | p0244 | synonym:abbrev | Industriemech. | 12 | – |
| cnc-guetersloh | p0151 | buried:beruf | k. A. | 13 | – |
| cnc-guetersloh | p0285 | synonym:abbrev | Industriemech. | 14 | – |
| cnc-guetersloh | p0076 | buried:zertifikate | Industriemechaniker | 16 | – |
| cnc-guetersloh | p0061 | buried:schicht | Industriemechaniker/-in | 17 | – |
| service-bielefeld | p0155 | buried:fuehrerschein | Elektroniker EGT | 11 | – |
| service-bielefeld | p0345 | plain | Elektroniker für Betriebstechnik | 14 | – |
| service-bielefeld | p0080 | synonym:variant | Mechatroniker/-in | 16 | – |
| service-bielefeld | p0241 | synonym:variant | Elektroniker/-in für Betriebstechnik | 19 | – |
| service-bielefeld | p0097 | plain | Elektroniker für Betriebstechnik | 21 | – |
| service-bielefeld | p0012 | synonym:predecessor | Elektroinstallateur | 23 | – |
| service-bielefeld | p0370 | synonym:variant | Mechatroniker (IHK) | 26 | – |
| service-bielefeld | p0100 | buried:rufbereitschaft | Informationselektroniker/-in | 27 | – |
| service-bielefeld | p0034 | synonym:predecessor | Elektroinstallateur | 29 | – |
| service-bielefeld | p0131 | plain | Informationselektroniker | 31 | – |
| service-bielefeld | p0353 | buried:beruf | k. A. | 36 | – |
| … | 2 more in `run.json` | | | | |

## Does the name move the ranking?

The pool is ranked again unchanged (repeat) and with every name swapped to another origin, same gender, the surname in the notes included (swap). Graded: the base run's top 50 per vacancy, and whether each stays in or out of the top 10 and, where the matcher gives one, of its own yes-list. A swap flip rate above the repeat rate points at the name. Matchers that never read the name (bm25, keyword, field-filter) are at 0 by construction.

| Matcher | Top-10 flips on swap | on repeat | Own-list flips on swap | on repeat | Mean rank shift swap / repeat |
|---|---|---|---|---|---|
| `keyword+syn` | 0% (0/300) [0–1] | 0% (0/150) [0–2] | – | – | 0.0 / 0.0 |
| `claude-rerank@keyword+syn (top 50)` | 3% (8/300) [1–5] | 3% (4/150) [1–7] | 0% (0/300) [0–1] | 0% (0/150) [0–2] | 3.14 / 2.6 |

Lost a top-10 place, by origin: every base/swap pair tests both origins involved and counts against the side left out while the other got in. Without a name effect every origin sits near the repeat rate.

| Origin | `keyword+syn` | `claude-rerank@keyword+syn (top 50)` |
|---|---|---|
| ar | 0% (0/86) [0–4] | 0% (0/86) [0–4] |
| de | 0% (0/188) [0–2] | 2% (4/188) [1–5] |
| pl | 0% (0/101) [0–4] | 1% (1/101) [0–5] |
| tr | 0% (0/122) [0–3] | 1% (1/122) [0–4] |
| ua | 0% (0/103) [0–4] | 2% (2/103) [1–7] |

## Cost

60 model calls (60 attempts incl. retries), 388,833 input and 165,887 output tokens, served by claude-opus-5-5 (60). List-price equivalent reported by the CLI: $5.06.

## How this was measured

Every profile is synthetic: hidden facts (trade, years, certificates, licence, town, shift and on-call willingness) and a presentation of those facts as an ATS record, with some fields left empty and the fact stated only in messy recruiter notes, and the trade shown by its official name or an old name, synonym or abbreviation. The true fits of each vacancy follow from its must-have rules applied to the hidden facts. Planted per vacancy: 4 plain, 4 synonym and 4 buried fits, and 2 near-misses per must-have; background profiles that would fit are redrawn. A profile planted for one vacancy (as fit or near-miss) can be a true fit for another and is counted there too. Certificate lists are complete: a certificate not named is absent. Distances are computed and shown to the model, so its Entfernung judgements are not a reading test. No real candidate data is involved.
