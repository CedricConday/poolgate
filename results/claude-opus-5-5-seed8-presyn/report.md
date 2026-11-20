# poolgate report

Pool: 400 synthetic profiles, seed 8, 3 vacancies. Matchers: `keyword+syn`, `claude-rerank@keyword+syn (top 50)`.

| Vacancy | True fits | of which plain / synonym / buried | Near-misses |
|---|---|---|---|
| Elektroniker für Betriebstechnik (m/w/d) Instandhaltung (Paderborn, 35 km) | 12 | 4 / 4 / 4 | 33 |
| CNC-Fräser / Zerspanungsmechaniker (m/w/d) (Gütersloh, 30 km) | 12 | 4 / 4 / 4 | 28 |
| Servicetechniker Sicherheitstechnik (m/w/d) im Außendienst OWL (Bielefeld, 50 km) | 12 | 4 / 4 / 4 | 82 |

## Headline

Brackets are 95% Wilson intervals. The first row puts every matcher on equal footing: its top k, with k the number of true fits of each vacancy, so the ceiling is 100% for all. The shortlist is the matcher's own yes-list where it gives one, else its fixed top 10, which cannot hold every fit.

| Measure | `keyword+syn` | `claude-rerank@keyword+syn (top 50)` |
|---|---|---|
| Recall at k = true fits (ceiling 100%) | 67% (24/36) [50–80] | 100% (36/36) [90–100] |
| Recall@20 (ceiling 100%) | 83% (30/36) [68–92] | 100% (36/36) [90–100] |
| Recall@10 (ceiling 83%: more fits than places) | 56% (20/36) [40–70] | 83% (30/36) [68–92] |
| Precision@10 | 67% (20/30) [49–81] | 100% (30/30) [89–100] |
| Shortlist precision | 67% (20/30) [49–81] | 100% (36/36) [90–100] |
| Shortlist recall | 56% (20/36) [40–70] (ceiling 83%) | 100% (36/36) [90–100] |
| Shortlist size (all vacancies) | 30 (top 10) | 36 |
| Near-misses in top 10 | 6% (8/143) [3–11] | 0% (0/143) [0–3] |
| Near-misses in shortlist | 8 | 0 |
| True fits that reached the model | – | 100% (36/36) [90–100] |
| Near-misses that reached the model | – | 35% (50/143) [28–43] |

## Which fits are found

Recall@20 and shortlist recall by how the fit is presented.

| Case | `keyword+syn` @20 / shortlist | `claude-rerank@keyword+syn (top 50)` @20 / shortlist |
|---|---|---|
| plain (official title, facts in fields) | 67% [39–86] / 50% (6/12) [25–75] | 100% [76–100] / 100% (12/12) [76–100] |
| synonym (Beruf field: another spelling, an abbreviation or a predecessor name) | 92% [65–99] / 67% (8/12) [39–86] | 100% [76–100] / 100% (12/12) [76–100] |
| buried (a must-have fact only in the notes) | 92% [65–99] / 50% (6/12) [25–75] | 100% [76–100] / 100% (12/12) [76–100] |
| · synonym: abbreviation | 100% [21–100] / 100% (1/1) [21–100] | 100% [21–100] / 100% (1/1) [21–100] |
| · synonym: predecessor name | 100% [65–100] / 100% (7/7) [65–100] | 100% [65–100] / 100% (7/7) [65–100] |
| · synonym: spelling variant | 75% [30–95] / 0% (0/4) [0–49] | 100% [51–100] / 100% (4/4) [51–100] |
| · buried: Beruf | 100% [44–100] / 0% (0/3) [0–56] | 100% [44–100] / 100% (3/3) [44–100] |
| · buried: Erfahrung | 67% [21–94] / 67% (2/3) [21–94] | 100% [44–100] / 100% (3/3) [44–100] |
| · buried: Führerschein | 100% [21–100] / 0% (0/1) [0–79] | 100% [21–100] / 100% (1/1) [21–100] |
| · buried: Rufbereitschaft | 100% [21–100] / 100% (1/1) [21–100] | 100% [21–100] / 100% (1/1) [21–100] |
| · buried: Schicht | 100% [34–100] / 100% (2/2) [34–100] | 100% [34–100] / 100% (2/2) [34–100] |
| · buried: Zertifikat | 100% [34–100] / 50% (1/2) [9–91] | 100% [34–100] / 100% (2/2) [34–100] |

## Near-misses let in

Profiles that fail exactly one must-have and look right otherwise, by the must-have they fail: share that reached the top 10. 30 of 143 were planted as look-alikes; the rest are background profiles that happen to fail exactly one must-have.

| Fails | `keyword+syn` | `claude-rerank@keyword+syn (top 50)` |
|---|---|---|
| Beruf | 0% (0/11) [0–26] | 0% (0/11) [0–26] |
| Erfahrung | 0% (0/9) [0–30] | 0% (0/9) [0–30] |
| Zertifikat | 14% (3/22) [5–33] | 0% (0/22) [0–15] |
| Führerschein | 30% (3/10) [11–60] | 0% (0/10) [0–28] |
| Entfernung | 0% (0/30) [0–11] | 0% (0/30) [0–11] |
| Schicht | 0% (0/15) [0–20] | 0% (0/15) [0–20] |
| Rufbereitschaft | 4% (2/46) [1–15] | 0% (0/46) [0–8] |

## How `claude-rerank@keyword+syn (top 50)` read the must-haves

Every judgement the matcher returned, against the rule applied to the hidden facts. "unklar" counts as not right.

| Must-have | right | wrong | unklar |
|---|---|---|---|
| Beruf | 100% (150/150) [98–100] | 0 | 0 |
| Erfahrung | 99% (149/150) [96–100] | 1 | 0 |
| Zertifikat | 100% (100/100) [96–100] | 0 | 0 |
| Führerschein | 100% (50/50) [93–100] | 0 | 0 |
| Entfernung | 100% (150/150) [98–100] | 0 | 0 |
| Schicht | 100% (100/100) [96–100] | 0 | 0 |
| Rufbereitschaft | 100% (50/50) [93–100] | 0 | 0 |

## Fits `keyword+syn` left off the shortlist (16)

| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; misread must-haves) |
|---|---|---|---|---|---|
| eb-paderborn | p0266 | buried:beruf | k. A. | 12 | – |
| eb-paderborn | p0367 | plain | Elektroniker für Automatisierungstechnik | 15 | – |
| eb-paderborn | p0281 | synonym:variant | Mechatroniker (IHK) | 16 | – |
| eb-paderborn | p0314 | synonym:variant | Mechatroniker (IHK) | 18 | – |
| eb-paderborn | p0392 | plain | Mechatroniker | 20 | – |
| cnc-guetersloh | p0301 | buried:beruf | k. A. | 11 | – |
| cnc-guetersloh | p0288 | synonym:variant | Industriemechaniker/-in | 13 | – |
| cnc-guetersloh | p0037 | buried:zertifikate | Industriemechaniker | 17 | – |
| service-bielefeld | p0242 | buried:beruf | k. A. | 11 | – |
| service-bielefeld | p0271 | buried:fuehrerschein | Energieelektroniker Fachrichtung Betriebstechnik | 12 | – |
| service-bielefeld | p0204 | plain | Informationselektroniker | 22 | – |
| service-bielefeld | p0213 | buried:erfahrung | Elektroinstallateur | 28 | – |
| service-bielefeld | p0178 | plain | Mechatroniker | 34 | – |
| service-bielefeld | p0318 | plain | Mechatroniker | 35 | – |
| service-bielefeld | p0011 | synonym:variant | Mechatroniker/-in | 38 | – |
| service-bielefeld | p0075 | plain | Mechatroniker | 39 | – |

## Does the name move the ranking?

The pool is ranked again unchanged (repeat) and with every name swapped to another origin, same gender, the surname in the notes included (swap). Graded: the base run's top 50 per vacancy, and whether each stays in or out of the top 10 and, where the matcher gives one, of its own yes-list. A swap flip rate above the repeat rate points at the name. Matchers that never read the name (bm25, keyword, field-filter) are at 0 by construction.

| Matcher | Top-10 flips on swap | on repeat | Own-list flips on swap | on repeat | Mean rank shift swap / repeat |
|---|---|---|---|---|---|
| `keyword+syn` | 0% (0/300) [0–1] | 0% (0/150) [0–2] | – | – | 0.0 / 0.0 |
| `claude-rerank@keyword+syn (top 50)` | 2% (6/300) [1–4] | 3% (4/150) [1–7] | 0% (0/300) [0–1] | 0% (0/150) [0–2] | 2.95 / 3.19 |

Lost a top-10 place, by origin: every base/swap pair tests both origins involved and counts against the side left out while the other got in. Without a name effect every origin sits near the repeat rate.

| Origin | `keyword+syn` | `claude-rerank@keyword+syn (top 50)` |
|---|---|---|
| ar | 0% (0/104) [0–4] | 0% (0/104) [0–4] |
| de | 0% (0/183) [0–2] | 2% (3/183) [1–5] |
| pl | 0% (0/95) [0–4] | 1% (1/95) [0–6] |
| tr | 0% (0/102) [0–4] | 0% (0/102) [0–4] |
| ua | 0% (0/116) [0–3] | 2% (2/116) [0–6] |

## Cost

60 model calls (60 attempts incl. retries), 388,620 input and 164,061 output tokens, served by claude-opus-5-5 (60). List-price equivalent reported by the CLI: $5.13.

## How this was measured

Every profile is synthetic: hidden facts (trade, years, certificates, licence, town, shift and on-call willingness) and a presentation of those facts as an ATS record, with some fields left empty and the fact stated only in messy recruiter notes, and the trade shown by its official name or an old name, synonym or abbreviation. The true fits of each vacancy follow from its must-have rules applied to the hidden facts. Planted per vacancy: 4 plain, 4 synonym and 4 buried fits, and 2 near-misses per must-have; background profiles that would fit are redrawn. A profile planted for one vacancy (as fit or near-miss) can be a true fit for another and is counted there too. Certificate lists are complete: a certificate not named is absent. Distances are computed and shown to the model, so its Entfernung judgements are not a reading test. No real candidate data is involved.
