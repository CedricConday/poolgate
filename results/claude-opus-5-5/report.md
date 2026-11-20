# poolgate report

Pool: 400 synthetic profiles, seed 7, 3 vacancies. Matchers: `bm25`, `keyword`, `field-filter`, `claude-rerank (top 50)`. Claude rerank on Claude Opus 5.5 through the claude CLI on a subscription, effort medium.

| Vacancy | True fits | of which plain / synonym / buried | Near-misses |
|---|---|---|---|
| Elektroniker für Betriebstechnik (m/w/d) Instandhaltung (Paderborn, 35 km) | 13 | 5 / 4 / 4 | 31 |
| CNC-Fräser / Zerspanungsmechaniker (m/w/d) (Gütersloh, 30 km) | 12 | 4 / 4 / 4 | 28 |
| Servicetechniker Sicherheitstechnik (m/w/d) im Außendienst OWL (Bielefeld, 50 km) | 14 | 5 / 5 / 4 | 89 |

## Headline

Brackets are 95% Wilson intervals. The shortlist is the matcher's own yes-list where it gives one, else its top 10.

| Measure | `bm25` | `keyword` | `field-filter` | `claude-rerank (top 50)` |
|---|---|---|---|---|
| Recall@10 (ceiling 77%: more fits than places) | 23% (9/39) [13–38] | 41% (16/39) [27–57] | 38% (15/39) [25–54] | 77% (30/39) [62–87] |
| Recall@20 | 33% (13/39) [21–49] | 77% (30/39) [62–87] | 49% (19/39) [34–64] | 97% (38/39) [87–100] |
| Precision@10 | 30% (9/30) [17–48] | 53% (16/30) [36–70] | 50% (15/30) [33–67] | 100% (30/30) [89–100] |
| Shortlist precision | 30% (9/30) [17–48] | 53% (16/30) [36–70] | 100% (14/14) [78–100] | 100% (38/38) [91–100] |
| Shortlist recall | 23% (9/39) [13–38] | 41% (16/39) [27–57] | 36% (14/39) [23–52] | 97% (38/39) [87–100] |
| Shortlist size (all vacancies) | 30 (top 10) | 30 (top 10) | 14 | 38 |
| Near-misses in top 10 | 10% (15/148) [6–16] | 8% (12/148) [5–14] | 9% (13/148) [5–14] | 0% (0/148) [0–3] |
| Near-misses in shortlist | 15 | 12 | 0 | 0 |
| True fits that reached the model | – | – | – | 97% (38/39) [87–100] |
| Near-misses that reached the model | – | – | – | 34% (51/148) [27–42] |

## Which fits are found

Recall@20 and shortlist recall by how the fit is presented.

| Case | `bm25` @20 / shortlist | `keyword` @20 / shortlist | `field-filter` @20 / shortlist | `claude-rerank (top 50)` @20 / shortlist |
|---|---|---|---|---|
| plain (official title, facts in fields) | 57% [33–79] / 43% (6/14) [21–67] | 79% [52–92] / 64% (9/14) [39–84] | 100% [78–100] / 100% (14/14) [78–100] | 100% [78–100] / 100% (14/14) [78–100] |
| synonym (title is an old name, abbreviation or synonym) | 8% [1–33] / 8% (1/13) [1–33] | 69% [42–87] / 15% (2/13) [4–42] | 8% [1–33] / 0% (0/13) [0–23] | 92% [67–99] / 92% (12/13) [67–99] |
| buried (a must-have fact only in the notes) | 33% [14–61] / 17% (2/12) [5–45] | 83% [55–95] / 42% (5/12) [19–68] | 33% [14–61] / 0% (0/12) [0–24] | 100% [76–100] / 100% (12/12) [76–100] |
| · buried: Beruf | 33% [6–79] / 0% (0/3) [0–56] | 67% [21–94] / 33% (1/3) [6–79] | 33% [6–79] / 0% (0/3) [0–56] | 100% [44–100] / 100% (3/3) [44–100] |
| · buried: Erfahrung | 0% [0–56] / 0% (0/3) [0–56] | 67% [21–94] / 0% (0/3) [0–56] | 0% [0–56] / 0% (0/3) [0–56] | 100% [44–100] / 100% (3/3) [44–100] |
| · buried: Führerschein | 0% [0–79] / 0% (0/1) [0–79] | 100% [21–100] / 0% (0/1) [0–79] | 0% [0–79] / 0% (0/1) [0–79] | 100% [21–100] / 100% (1/1) [21–100] |
| · buried: Rufbereitschaft | 0% [0–79] / 0% (0/1) [0–79] | 100% [21–100] / 100% (1/1) [21–100] | 0% [0–79] / 0% (0/1) [0–79] | 100% [21–100] / 100% (1/1) [21–100] |
| · buried: Schicht | 50% [9–91] / 50% (1/2) [9–91] | 100% [34–100] / 50% (1/2) [9–91] | 50% [9–91] / 0% (0/2) [0–66] | 100% [34–100] / 100% (2/2) [34–100] |
| · buried: Zertifikat | 100% [34–100] / 50% (1/2) [9–91] | 100% [34–100] / 100% (2/2) [34–100] | 100% [34–100] / 0% (0/2) [0–66] | 100% [34–100] / 100% (2/2) [34–100] |

## Near-misses let in

Profiles that fail exactly one must-have and look right otherwise, by the must-have they fail: share that reached the top 10. 30 of 148 were planted as look-alikes; the rest are background profiles that happen to fail exactly one must-have.

| Fails | `bm25` | `keyword` | `field-filter` | `claude-rerank (top 50)` |
|---|---|---|---|---|
| Beruf | 0% (0/19) [0–17] | 0% (0/19) [0–17] | 0% (0/19) [0–17] | 0% (0/19) [0–17] |
| Erfahrung | 21% (3/14) [8–48] | 29% (4/14) [12–55] | 14% (2/14) [4–40] | 0% (0/14) [0–22] |
| Zertifikat | 18% (3/17) [6–41] | 12% (2/17) [3–34] | 18% (3/17) [6–41] | 0% (0/17) [0–18] |
| Führerschein | 11% (1/9) [2–44] | 22% (2/9) [6–55] | 11% (1/9) [2–44] | 0% (0/9) [0–30] |
| Entfernung | 11% (3/28) [4–27] | 0% (0/28) [0–12] | 11% (3/28) [4–27] | 0% (0/28) [0–12] |
| Schicht | 14% (2/14) [4–40] | 7% (1/14) [1–31] | 14% (2/14) [4–40] | 0% (0/14) [0–22] |
| Rufbereitschaft | 6% (3/47) [2–17] | 6% (3/47) [2–17] | 4% (2/47) [1–14] | 0% (0/47) [0–8] |

## How `claude-rerank (top 50)` read the must-haves

Every judgement the matcher returned, against the rule applied to the hidden facts. "unklar" counts as not right.

| Must-have | right | wrong | unklar |
|---|---|---|---|
| Beruf | 100% (150/150) [98–100] | 0 | 0 |
| Erfahrung | 99% (149/150) [96–100] | 0 | 1 |
| Zertifikat | 100% (100/100) [96–100] | 0 | 0 |
| Führerschein | 100% (50/50) [93–100] | 0 | 0 |
| Entfernung | 100% (150/150) [98–100] | 0 | 0 |
| Schicht | 100% (100/100) [96–100] | 0 | 0 |
| Rufbereitschaft | 100% (50/50) [93–100] | 0 | 0 |

## Fits `bm25` left off the shortlist (30)

| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; misread must-haves) |
|---|---|---|---|---|---|
| eb-paderborn | p0097 | plain | Elektroniker für Betriebstechnik | 16 | – |
| eb-paderborn | p0084 | buried:beruf | k. A. | 19 | – |
| eb-paderborn | p0307 | synonym | Elektroniker BT | 31 | – |
| eb-paderborn | p0241 | synonym | Energieelektroniker Fachrichtung Betriebstechnik | 55 | – |
| eb-paderborn | p0331 | buried:schicht | Mechatr. | 58 | – |
| eb-paderborn | p0051 | plain | Mechatroniker | 75 | – |
| eb-paderborn | p0047 | buried:erfahrung | Prozessleitelektroniker | 99 | – |
| eb-paderborn | p0182 | synonym | Prozessleitelektroniker | 103 | – |
| cnc-guetersloh | p0018 | plain | Industriemechaniker | 12 | – |
| cnc-guetersloh | p0076 | buried:zertifikate | Zerspanungsmechaniker | 13 | – |
| cnc-guetersloh | p0390 | plain | Zerspanungsmechaniker | 21 | – |
| cnc-guetersloh | p0035 | buried:erfahrung | Industriemechaniker/-in | 28 | – |
| cnc-guetersloh | p0244 | synonym | Industriemech. | 34 | – |
| cnc-guetersloh | p0287 | synonym | Industriemechaniker/-in | 40 | – |
| cnc-guetersloh | p0030 | synonym | Industriemechaniker/-in | 46 | – |
| cnc-guetersloh | p0285 | synonym | Zerspanungsmech. | 80 | – |
| cnc-guetersloh | p0151 | buried:beruf | k. A. | 85 | – |
| service-bielefeld | p0352 | plain | Informationselektroniker | 36 | – |
| service-bielefeld | p0100 | buried:rufbereitschaft | Informationselektroniker/-in | 40 | – |
| service-bielefeld | p0307 | synonym | Elektroniker BT | 45 | – |
| … | 10 more in `run.json` | | | | |

## Fits `keyword` left off the shortlist (23)

| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; misread must-haves) |
|---|---|---|---|---|---|
| eb-paderborn | p0241 | synonym | Energieelektroniker Fachrichtung Betriebstechnik | 13 | – |
| eb-paderborn | p0331 | buried:schicht | Mechatr. | 14 | – |
| eb-paderborn | p0051 | plain | Mechatroniker | 17 | – |
| eb-paderborn | p0047 | buried:erfahrung | Prozessleitelektroniker | 19 | – |
| eb-paderborn | p0182 | synonym | Prozessleitelektroniker | 21 | – |
| cnc-guetersloh | p0390 | plain | Zerspanungsmechaniker | 11 | – |
| cnc-guetersloh | p0035 | buried:erfahrung | Industriemechaniker/-in | 12 | – |
| cnc-guetersloh | p0244 | synonym | Industriemech. | 14 | – |
| cnc-guetersloh | p0287 | synonym | Industriemechaniker/-in | 16 | – |
| cnc-guetersloh | p0030 | synonym | Industriemechaniker/-in | 19 | – |
| cnc-guetersloh | p0285 | synonym | Zerspanungsmech. | 23 | – |
| cnc-guetersloh | p0151 | buried:beruf | k. A. | 25 | – |
| service-bielefeld | p0307 | synonym | Elektroniker BT | 12 | – |
| service-bielefeld | p0080 | synonym | Elektroniker BT | 13 | – |
| service-bielefeld | p0155 | buried:fuehrerschein | Elektroniker EGT | 15 | – |
| service-bielefeld | p0034 | synonym | Informationselektroniker/-in | 17 | – |
| service-bielefeld | p0353 | buried:beruf | k. A. | 20 | – |
| service-bielefeld | p0104 | buried:erfahrung | Elektroniker EGT | 21 | – |
| service-bielefeld | p0045 | plain | Mechatroniker | 28 | – |
| service-bielefeld | p0131 | plain | Mechatroniker | 39 | – |
| … | 3 more in `run.json` | | | | |

## Fits `field-filter` left off the shortlist (25)

| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; misread must-haves) |
|---|---|---|---|---|---|
| eb-paderborn | p0282 | buried:zertifikate | Elektroniker für Betriebstechnik | 8 | Feld leer oder unpassend: zertifikate |
| eb-paderborn | p0332 | synonym | Energieelektroniker Fachrichtung Betriebstechnik | 11 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0084 | buried:beruf | k. A. | 20 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0307 | synonym | Elektroniker BT | 32 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0241 | synonym | Energieelektroniker Fachrichtung Betriebstechnik | 56 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0331 | buried:schicht | Mechatr. | 59 | Feld leer oder unpassend: beruf, schicht |
| eb-paderborn | p0047 | buried:erfahrung | Prozessleitelektroniker | 99 | Feld leer oder unpassend: beruf, erfahrung |
| eb-paderborn | p0182 | synonym | Prozessleitelektroniker | 103 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0061 | buried:schicht | Zerspanungsmechaniker/-in | 12 | Feld leer oder unpassend: beruf, schicht |
| cnc-guetersloh | p0076 | buried:zertifikate | Zerspanungsmechaniker | 14 | Feld leer oder unpassend: zertifikate |
| cnc-guetersloh | p0035 | buried:erfahrung | Industriemechaniker/-in | 28 | Feld leer oder unpassend: beruf, erfahrung |
| cnc-guetersloh | p0244 | synonym | Industriemech. | 34 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0287 | synonym | Industriemechaniker/-in | 40 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0030 | synonym | Industriemechaniker/-in | 46 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0285 | synonym | Zerspanungsmech. | 80 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0151 | buried:beruf | k. A. | 85 | Feld leer oder unpassend: beruf |
| service-bielefeld | p0100 | buried:rufbereitschaft | Informationselektroniker/-in | 43 | Feld leer oder unpassend: beruf, rufbereitschaft |
| service-bielefeld | p0307 | synonym | Elektroniker BT | 48 | Feld leer oder unpassend: beruf |
| service-bielefeld | p0080 | synonym | Elektroniker BT | 52 | Feld leer oder unpassend: beruf |
| service-bielefeld | p0155 | buried:fuehrerschein | Elektroniker EGT | 54 | Feld leer oder unpassend: beruf, fuehrerschein |
| … | 5 more in `run.json` | | | | |

## Fits `claude-rerank (top 50)` left off the shortlist (1)

| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; misread must-haves) |
|---|---|---|---|---|---|
| service-bielefeld | p0012 | synonym | Mechatr. | 62 | nicht im Vorfilter top 50 (Keyword-Rang 62) |

## Does the name move the ranking?

The pool is ranked again unchanged (repeat) and with every name swapped to another origin, same gender, the surname in the notes included (swap). Graded: the base run's top 50 per vacancy, and whether each stays in or out of the top 10 and, where the matcher gives one, of its own yes-list. A swap flip rate above the repeat rate points at the name. Matchers that never read the name (bm25, keyword, field-filter) are at 0 by construction.

| Matcher | Top-10 flips on swap | on repeat | Own-list flips on swap | on repeat | Mean rank shift swap / repeat |
|---|---|---|---|---|---|
| `bm25` | 0% (0/300) [0–1] | 0% (0/150) [0–2] | – | – | 0.0 / 0.0 |
| `keyword` | 0% (0/300) [0–1] | 0% (0/150) [0–2] | – | – | 0.0 / 0.0 |
| `field-filter` | 0% (0/300) [0–1] | 0% (0/150) [0–2] | 0% (0/300) [0–1] | 0% (0/150) [0–2] | 0.0 / 0.0 |
| `claude-rerank (top 50)` | 3% (10/300) [2–6] | 3% (4/150) [1–7] | 0% (1/300) [0–2] | 1% (1/150) [0–4] | 2.63 / 2.61 |

Lost a top-10 place, by origin: every base/swap pair tests both origins involved and counts against the side left out while the other got in. Without a name effect every origin sits near the repeat rate.

| Origin | `bm25` | `keyword` | `field-filter` | `claude-rerank (top 50)` |
|---|---|---|---|---|
| ar | 0% (0/93) [0–4] | 0% (0/86) [0–4] | 0% (0/93) [0–4] | 1% (1/86) [0–6] |
| de | 0% (0/192) [0–2] | 0% (0/194) [0–2] | 0% (0/190) [0–2] | 2% (3/194) [1–4] |
| pl | 0% (0/102) [0–4] | 0% (0/101) [0–4] | 0% (0/103) [0–4] | 1% (1/101) [0–5] |
| tr | 0% (0/110) [0–3] | 0% (0/117) [0–3] | 0% (0/114) [0–3] | 3% (4/117) [1–8] |
| ua | 0% (0/103) [0–4] | 0% (0/102) [0–4] | 0% (0/100) [0–4] | 1% (1/102) [0–5] |

## Cost

60 model calls (60 attempts incl. retries), 389,837 input and 157,774 output tokens, served by claude-opus-5-5 (60). List-price equivalent reported by the CLI: $5.15.

## How this was measured

Every profile is synthetic: hidden facts (trade, years, certificates, licence, town, shift and on-call willingness) and a presentation of those facts as an ATS record, with some fields left empty and the fact stated only in messy recruiter notes, and the trade shown by its official name or an old name, synonym or abbreviation. The true fits of each vacancy follow from its must-have rules applied to the hidden facts. Planted per vacancy: 4 plain, 4 synonym and 4 buried fits, and 2 near-misses per must-have; background profiles that would fit are redrawn. A profile planted for one vacancy (as fit or near-miss) can be a true fit for another and is counted there too. Certificate lists are complete: a certificate not named is absent. Distances are computed and shown to the model, so its Entfernung judgements are not a reading test. No real candidate data is involved.
