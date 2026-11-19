# poolgate report

Pool: 400 synthetic profiles, seed 7, 3 vacancies. Matchers: `bm25`, `keyword`, `field-filter`.

| Vacancy | True fits | of which plain / synonym / buried | Near-misses |
|---|---|---|---|
| Elektroniker für Betriebstechnik (m/w/d) Instandhaltung (Paderborn, 35 km) | 14 | 5 / 5 / 4 | 31 |
| CNC-Fräser / Zerspanungsmechaniker (m/w/d) (Gütersloh, 30 km) | 12 | 4 / 4 / 4 | 34 |
| Servicetechniker Sicherheitstechnik (m/w/d) im Außendienst OWL (Bielefeld, 50 km) | 14 | 5 / 5 / 4 | 78 |

## Headline

Brackets are 95% Wilson intervals. The shortlist is the matcher's own yes-list where it gives one, else its top 10.

| Measure | `bm25` | `keyword` | `field-filter` |
|---|---|---|---|
| Recall@10 (ceiling 75%: more fits than places) | 15% (6/40) [7–29] | 40% (16/40) [26–55] | 35% (14/40) [22–50] |
| Recall@20 | 32% (13/40) [20–48] | 68% (27/40) [52–80] | 48% (19/40) [33–63] |
| Precision@10 | 20% (6/30) [10–37] | 53% (16/30) [36–70] | 47% (14/30) [30–64] |
| Shortlist precision | 20% (6/30) [10–37] | 53% (16/30) [36–70] | 100% (14/14) [78–100] |
| Shortlist recall | 15% (6/40) [7–29] | 40% (16/40) [26–55] | 35% (14/40) [22–50] |
| Shortlist size (all vacancies) | 30 (top 10) | 30 (top 10) | 14 |
| Near-misses in top 10 | 8% (12/143) [5–14] | 6% (9/143) [3–12] | 5% (7/143) [2–10] |
| Near-misses in shortlist | 12 | 9 | 0 |

## Which fits are found

Recall@20 and shortlist recall by how the fit is presented.

| Case | `bm25` @20 / shortlist | `keyword` @20 / shortlist | `field-filter` @20 / shortlist |
|---|---|---|---|
| plain (official title, facts in fields) | 57% [33–79] / 36% (5/14) [16–61] | 79% [52–92] / 71% (10/14) [45–88] | 100% [78–100] / 100% (14/14) [78–100] |
| synonym (title is an old name, abbreviation or synonym) | 21% [8–48] / 7% (1/14) [1–31] | 57% [33–79] / 29% (4/14) [12–55] | 21% [8–48] / 0% (0/14) [0–22] |
| buried (a must-have fact only in the notes) | 17% [5–45] / 0% (0/12) [0–24] | 67% [39–86] / 17% (2/12) [5–45] | 17% [5–45] / 0% (0/12) [0–24] |
| · buried: Beruf | 0% [0–56] / 0% (0/3) [0–56] | 33% [6–79] / 0% (0/3) [0–56] | 0% [0–56] / 0% (0/3) [0–56] |
| · buried: Erfahrung | 0% [0–56] / 0% (0/3) [0–56] | 67% [21–94] / 0% (0/3) [0–56] | 0% [0–56] / 0% (0/3) [0–56] |
| · buried: Führerschein | 0% [0–79] / 0% (0/1) [0–79] | 100% [21–100] / 0% (0/1) [0–79] | 0% [0–79] / 0% (0/1) [0–79] |
| · buried: Rufbereitschaft | 0% [0–79] / 0% (0/1) [0–79] | 100% [21–100] / 0% (0/1) [0–79] | 0% [0–79] / 0% (0/1) [0–79] |
| · buried: Schicht | 50% [9–91] / 0% (0/2) [0–66] | 100% [34–100] / 50% (1/2) [9–91] | 50% [9–91] / 0% (0/2) [0–66] |
| · buried: Zertifikat | 50% [9–91] / 0% (0/2) [0–66] | 50% [9–91] / 50% (1/2) [9–91] | 50% [9–91] / 0% (0/2) [0–66] |

## Near-misses let in

Profiles that fail exactly one must-have and look right otherwise, by the must-have they fail: share that reached the top 10. 30 of 143 were planted as look-alikes; the rest are background profiles that happen to fail exactly one must-have.

| Fails | `bm25` | `keyword` | `field-filter` |
|---|---|---|---|
| Beruf | 0% (0/15) [0–20] | 7% (1/15) [1–30] | 0% (0/15) [0–20] |
| Erfahrung | 20% (3/15) [7–45] | 20% (3/15) [7–45] | 13% (2/15) [4–38] |
| Zertifikat | 14% (3/21) [5–35] | 10% (2/21) [3–29] | 10% (2/21) [3–29] |
| Führerschein | 30% (3/10) [11–60] | 10% (1/10) [2–40] | 10% (1/10) [2–40] |
| Entfernung | 3% (1/32) [1–16] | 0% (0/32) [0–11] | 3% (1/32) [1–16] |
| Schicht | 13% (2/15) [4–38] | 0% (0/15) [0–20] | 7% (1/15) [1–30] |
| Rufbereitschaft | 0% (0/35) [0–10] | 6% (2/35) [2–19] | 0% (0/35) [0–10] |

## Fits `bm25` left off the shortlist (34)

| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; misread must-haves) |
|---|---|---|---|---|---|
| eb-paderborn | p0307 | synonym | Elektroniker/-in für Betriebstechnik | 11 | – |
| eb-paderborn | p0282 | buried:zertifikate | Elektroniker/-in für Betriebstechnik | 12 | – |
| eb-paderborn | p0302 | plain | Elektroniker für Betriebstechnik | 13 | – |
| eb-paderborn | p0182 | synonym | Elektroniker/-in für Automatisierungstechnik | 16 | – |
| eb-paderborn | p0097 | plain | Elektroniker für Betriebstechnik | 21 | – |
| eb-paderborn | p0241 | synonym | Elektroniker/-in für Betriebstechnik | 27 | – |
| eb-paderborn | p0047 | buried:erfahrung | Elektroniker für Betriebstechnik | 28 | – |
| eb-paderborn | p0331 | buried:schicht | Mechatroniker | 58 | – |
| eb-paderborn | p0131 | plain | Mechatroniker | 74 | – |
| eb-paderborn | p0084 | buried:beruf | k. A. | 75 | – |
| eb-paderborn | p0370 | synonym | Mechatr. | 117 | – |
| cnc-guetersloh | p0061 | buried:schicht | Zerspanungsmechaniker | 12 | – |
| cnc-guetersloh | p0390 | plain | Zerspanungsmechaniker | 15 | – |
| cnc-guetersloh | p0035 | buried:erfahrung | Industriemechaniker | 24 | – |
| cnc-guetersloh | p0287 | synonym | Industriemechaniker/-in | 35 | – |
| cnc-guetersloh | p0244 | synonym | Maschinenschlosser (bis 1987) | 71 | – |
| cnc-guetersloh | p0285 | synonym | Zerspanungsmech. | 89 | – |
| cnc-guetersloh | p0076 | buried:zertifikate | Industriemech. | 93 | – |
| cnc-guetersloh | p0151 | buried:beruf | k. A. | 98 | – |
| cnc-guetersloh | p0030 | synonym | Betriebsschlosser (bis 1987) | 103 | – |
| … | 14 more in `run.json` | | | | |

## Fits `keyword` left off the shortlist (24)

| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; misread must-haves) |
|---|---|---|---|---|---|
| eb-paderborn | p0241 | synonym | Elektroniker/-in für Betriebstechnik | 12 | – |
| eb-paderborn | p0047 | buried:erfahrung | Elektroniker für Betriebstechnik | 13 | – |
| eb-paderborn | p0331 | buried:schicht | Mechatroniker | 16 | – |
| eb-paderborn | p0131 | plain | Mechatroniker | 22 | – |
| eb-paderborn | p0084 | buried:beruf | k. A. | 23 | – |
| eb-paderborn | p0370 | synonym | Mechatr. | 31 | – |
| cnc-guetersloh | p0035 | buried:erfahrung | Industriemechaniker | 11 | – |
| cnc-guetersloh | p0287 | synonym | Industriemechaniker/-in | 14 | – |
| cnc-guetersloh | p0244 | synonym | Maschinenschlosser (bis 1987) | 18 | – |
| cnc-guetersloh | p0285 | synonym | Zerspanungsmech. | 20 | – |
| cnc-guetersloh | p0076 | buried:zertifikate | Industriemech. | 22 | – |
| cnc-guetersloh | p0151 | buried:beruf | k. A. | 24 | – |
| cnc-guetersloh | p0030 | synonym | Betriebsschlosser (bis 1987) | 26 | – |
| service-bielefeld | p0155 | buried:fuehrerschein | Elektroniker EGT | 12 | – |
| service-bielefeld | p0100 | buried:rufbereitschaft | Elektroniker EGT | 15 | – |
| service-bielefeld | p0353 | buried:beruf | k. A. | 17 | – |
| service-bielefeld | p0352 | plain | Mechatroniker | 20 | – |
| service-bielefeld | p0080 | synonym | Mechatroniker/-in | 21 | – |
| service-bielefeld | p0045 | plain | Mechatroniker | 25 | – |
| service-bielefeld | p0131 | plain | Mechatroniker | 29 | – |
| … | 4 more in `run.json` | | | | |

## Fits `field-filter` left off the shortlist (26)

| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; misread must-haves) |
|---|---|---|---|---|---|
| eb-paderborn | p0332 | synonym | Energieelektroniker Fachrichtung Betriebstechnik (bis 2003) | 13 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0307 | synonym | Elektroniker/-in für Betriebstechnik | 14 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0282 | buried:zertifikate | Elektroniker/-in für Betriebstechnik | 15 | Feld leer oder unpassend: beruf, zertifikate |
| eb-paderborn | p0182 | synonym | Elektroniker/-in für Automatisierungstechnik | 18 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0241 | synonym | Elektroniker/-in für Betriebstechnik | 28 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0047 | buried:erfahrung | Elektroniker für Betriebstechnik | 29 | Feld leer oder unpassend: erfahrung |
| eb-paderborn | p0331 | buried:schicht | Mechatroniker | 59 | Feld leer oder unpassend: schicht |
| eb-paderborn | p0084 | buried:beruf | k. A. | 75 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0370 | synonym | Mechatr. | 117 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0061 | buried:schicht | Zerspanungsmechaniker | 13 | Feld leer oder unpassend: schicht |
| cnc-guetersloh | p0035 | buried:erfahrung | Industriemechaniker | 24 | Feld leer oder unpassend: erfahrung |
| cnc-guetersloh | p0287 | synonym | Industriemechaniker/-in | 35 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0244 | synonym | Maschinenschlosser (bis 1987) | 71 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0285 | synonym | Zerspanungsmech. | 89 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0076 | buried:zertifikate | Industriemech. | 93 | Feld leer oder unpassend: beruf, zertifikate |
| cnc-guetersloh | p0151 | buried:beruf | k. A. | 98 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0030 | synonym | Betriebsschlosser (bis 1987) | 103 | Feld leer oder unpassend: beruf |
| service-bielefeld | p0307 | synonym | Elektroniker/-in für Betriebstechnik | 34 | Feld leer oder unpassend: beruf |
| service-bielefeld | p0155 | buried:fuehrerschein | Elektroniker EGT | 76 | Feld leer oder unpassend: beruf, fuehrerschein |
| service-bielefeld | p0100 | buried:rufbereitschaft | Elektroniker EGT | 80 | Feld leer oder unpassend: beruf, rufbereitschaft |
| … | 6 more in `run.json` | | | | |

## Does the name move the ranking?

The pool is ranked again unchanged (repeat) and with every name swapped to another origin, same gender, the surname in the notes included (swap). Graded: the base run's top 50 per vacancy, and whether each stays in or out of the top 10 and, where the matcher gives one, of its own yes-list. A swap flip rate above the repeat rate points at the name. Matchers that never read the name (bm25, keyword, field-filter) are at 0 by construction.

| Matcher | Top-10 flips on swap | on repeat | Own-list flips on swap | on repeat | Mean rank shift swap / repeat |
|---|---|---|---|---|---|
| `bm25` | 0% (0/300) [0–1] | 0% (0/150) [0–2] | – | – | 0.0 / 0.0 |
| `keyword` | 0% (0/300) [0–1] | 0% (0/150) [0–2] | – | – | 0.0 / 0.0 |
| `field-filter` | 0% (0/300) [0–1] | 0% (0/150) [0–2] | 0% (0/300) [0–1] | 0% (0/150) [0–2] | 0.0 / 0.0 |

Lost a top-10 place, by origin: every base/swap pair tests both origins involved and counts against the side left out while the other got in. Without a name effect every origin sits near the repeat rate.

| Origin | `bm25` | `keyword` | `field-filter` |
|---|---|---|---|
| ar | 0% (0/87) [0–4] | 0% (0/91) [0–4] | 0% (0/88) [0–4] |
| de | 0% (0/186) [0–2] | 0% (0/184) [0–2] | 0% (0/185) [0–2] |
| pl | 0% (0/99) [0–4] | 0% (0/93) [0–4] | 0% (0/100) [0–4] |
| tr | 0% (0/120) [0–3] | 0% (0/133) [0–3] | 0% (0/123) [0–3] |
| ua | 0% (0/108) [0–3] | 0% (0/99) [0–4] | 0% (0/104) [0–4] |

## How this was measured

Every profile is synthetic: hidden facts (trade, years, certificates, licence, town, shift and on-call willingness) and a presentation of those facts as an ATS record, with some fields left empty and the fact stated only in messy recruiter notes, and the trade shown by its official name or an old name, synonym or abbreviation. The true fits of each vacancy follow from its must-have rules applied to the hidden facts. Planted per vacancy: 4 plain, 4 synonym and 4 buried fits, and 2 near-misses per must-have; background profiles that would fit are redrawn. A profile planted for one vacancy (as fit or near-miss) can be a true fit for another and is counted there too. Certificate lists are complete: a certificate not named is absent. Distances are computed and shown to the model, so its Entfernung judgements are not a reading test. No real candidate data is involved.
