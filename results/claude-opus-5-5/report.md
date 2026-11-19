# poolgate report

Pool: 400 synthetic profiles, seed 7, 3 vacancies. Matchers: `bm25`, `keyword`, `field-filter`, `claude-rerank (top 50)`. Claude rerank on Claude Opus 5.5 through the claude CLI on a subscription, effort medium.

| Vacancy | True fits | of which plain / synonym / buried | Near-misses |
|---|---|---|---|
| Elektroniker für Betriebstechnik (m/w/d) Instandhaltung (Paderborn, 35 km) | 14 | 5 / 5 / 4 | 31 |
| CNC-Fräser / Zerspanungsmechaniker (m/w/d) (Gütersloh, 30 km) | 12 | 4 / 4 / 4 | 34 |
| Servicetechniker Sicherheitstechnik (m/w/d) im Außendienst OWL (Bielefeld, 50 km) | 14 | 5 / 5 / 4 | 78 |

## Headline

Brackets are 95% Wilson intervals. The shortlist is the matcher's own yes-list where it gives one, else its top 10.

| Measure | `bm25` | `keyword` | `field-filter` | `claude-rerank (top 50)` |
|---|---|---|---|---|
| Recall@10 (ceiling 75%: more fits than places) | 22% (9/40) [12–38] | 45% (18/40) [31–60] | 40% (16/40) [26–55] | 75% (30/40) [60–86] |
| Recall@20 | 32% (13/40) [20–48] | 70% (28/40) [55–82] | 42% (17/40) [29–58] | 95% (38/40) [83–99] |
| Precision@10 | 30% (9/30) [17–48] | 60% (18/30) [42–75] | 53% (16/30) [36–70] | 100% (30/30) [89–100] |
| Shortlist precision | 30% (9/30) [17–48] | 60% (18/30) [42–75] | 100% (14/14) [78–100] | 100% (34/34) [90–100] |
| Shortlist recall | 22% (9/40) [12–38] | 45% (18/40) [31–60] | 35% (14/40) [22–50] | 85% (34/40) [71–93] |
| Shortlist size (all vacancies) | 30 (top 10) | 30 (top 10) | 14 | 34 |
| Near-misses in top 10 | 9% (13/143) [5–15] | 6% (9/143) [3–12] | 5% (7/143) [2–10] | 0% (0/143) [0–3] |
| Near-misses in shortlist | 13 | 9 | 0 | 0 |
| True fits that reached the model | – | – | – | 95% (38/40) [83–99] |

## Which fits are found

Recall@20 and shortlist recall by how the fit is presented.

| Case | `bm25` @20 / shortlist | `keyword` @20 / shortlist | `field-filter` @20 / shortlist | `claude-rerank (top 50)` @20 / shortlist |
|---|---|---|---|---|
| plain (official title, facts in fields) | 71% [45–88] / 43% (6/14) [21–67] | 86% [60–96] / 71% (10/14) [45–88] | 100% [78–100] / 100% (14/14) [78–100] | 100% [78–100] / 100% (14/14) [78–100] |
| synonym (title is an old name, abbreviation or synonym) | 14% [4–40] / 14% (2/14) [4–40] | 57% [33–79] / 36% (5/14) [16–61] | 14% [4–40] / 0% (0/14) [0–22] | 93% [69–99] / 71% (10/14) [45–88] |
| buried (a must-have fact only in the notes) | 8% [1–35] / 8% (1/12) [1–35] | 67% [39–86] / 25% (3/12) [9–53] | 8% [1–35] / 0% (0/12) [0–24] | 92% [65–99] / 83% (10/12) [55–95] |
| · buried: Beruf | 0% [0–43] / 0% (0/5) [0–43] | 40% [12–77] / 0% (0/5) [0–43] | 0% [0–43] / 0% (0/5) [0–43] | 80% [38–96] / 80% (4/5) [38–96] |
| · buried: Erfahrung | 0% [0–66] / 0% (0/2) [0–66] | 100% [34–100] / 50% (1/2) [9–91] | 0% [0–66] / 0% (0/2) [0–66] | 100% [34–100] / 100% (2/2) [34–100] |
| · buried: Führerschein | 50% [9–91] / 50% (1/2) [9–91] | 100% [34–100] / 50% (1/2) [9–91] | 50% [9–91] / 0% (0/2) [0–66] | 100% [34–100] / 100% (2/2) [34–100] |
| · buried: Zertifikat | 0% [0–56] / 0% (0/3) [0–56] | 67% [21–94] / 33% (1/3) [6–79] | 0% [0–56] / 0% (0/3) [0–56] | 100% [44–100] / 67% (2/3) [21–94] |

## Near-misses let in

Profiles that fail exactly one must-have and look right otherwise, by the must-have they fail: share that reached the top 10.

| Fails | `bm25` | `keyword` | `field-filter` | `claude-rerank (top 50)` |
|---|---|---|---|---|
| Beruf | 0% (0/15) [0–20] | 7% (1/15) [1–30] | 0% (0/15) [0–20] | 0% (0/15) [0–20] |
| Erfahrung | 13% (2/15) [4–38] | 7% (1/15) [1–30] | 7% (1/15) [1–30] | 0% (0/15) [0–20] |
| Zertifikat | 14% (3/21) [5–35] | 5% (1/21) [1–23] | 10% (2/21) [3–29] | 0% (0/21) [0–15] |
| Führerschein | 30% (3/10) [11–60] | 10% (1/10) [2–40] | 20% (2/10) [6–51] | 0% (0/10) [0–28] |
| Entfernung | 9% (3/32) [3–24] | 0% (0/32) [0–11] | 0% (0/32) [0–11] | 0% (0/32) [0–11] |
| Schicht | 13% (2/15) [4–38] | 20% (3/15) [7–45] | 13% (2/15) [4–38] | 0% (0/15) [0–20] |
| Rufbereitschaft | 0% (0/35) [0–10] | 6% (2/35) [2–19] | 0% (0/35) [0–10] | 0% (0/35) [0–10] |

## How `claude-rerank (top 50)` read the must-haves

Every judgement the matcher returned, against the rule applied to the hidden facts. "unklar" counts as not right.

| Must-have | right | wrong | unklar |
|---|---|---|---|
| Beruf | 95% (143/150) [91–98] | 0 | 7 |
| Erfahrung | 100% (150/150) [98–100] | 0 | 0 |
| Zertifikat | 94% (94/100) [88–97] | 0 | 6 |
| Führerschein | 100% (50/50) [93–100] | 0 | 0 |
| Entfernung | 100% (150/150) [98–100] | 0 | 0 |
| Schicht | 100% (100/100) [96–100] | 0 | 0 |
| Rufbereitschaft | 100% (50/50) [93–100] | 0 | 0 |

## Fits `bm25` left off the shortlist (31)

| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; misread must-haves) |
|---|---|---|---|---|---|
| eb-paderborn | p0097 | plain | Elektroniker für Betriebstechnik | 15 | – |
| eb-paderborn | p0047 | buried:zertifikate | Elektroniker für Betriebstechnik | 38 | – |
| eb-paderborn | p0307 | synonym | Elektroniker BT | 40 | – |
| eb-paderborn | p0282 | buried:erfahrung | E-Techniker Betriebstechnik | 42 | – |
| eb-paderborn | p0241 | synonym | Elektroniker BT | 51 | – |
| eb-paderborn | p0084 | buried:beruf | k. A. | 54 | – |
| eb-paderborn | p0131 | plain | Mechatroniker | 66 | – |
| eb-paderborn | p0182 | synonym | Automatisierungselektroniker | 105 | – |
| eb-paderborn | p0331 | buried:zertifikate | Servicetechniker Mechatronik | 107 | – |
| eb-paderborn | p0370 | synonym | Servicetechniker Mechatronik | 114 | – |
| cnc-guetersloh | p0390 | plain | Zerspanungsmechaniker | 17 | – |
| cnc-guetersloh | p0151 | buried:zertifikate | Industriemechaniker | 36 | – |
| cnc-guetersloh | p0076 | buried:erfahrung | Industriemechaniker | 40 | – |
| cnc-guetersloh | p0244 | synonym | Maschinenschlosser | 75 | – |
| cnc-guetersloh | p0061 | buried:beruf | k. A. | 88 | – |
| cnc-guetersloh | p0035 | buried:beruf | k. A. | 98 | – |
| cnc-guetersloh | p0287 | synonym | Betriebsschlosser | 102 | – |
| cnc-guetersloh | p0030 | synonym | Betriebsschlosser | 104 | – |
| service-bielefeld | p0051 | plain | Elektroniker für Energie- und Gebäudetechnik | 12 | – |
| service-bielefeld | p0237 | plain | Elektroniker für Betriebstechnik | 18 | – |
| … | 11 more in `run.json` | | | | |

## Fits `keyword` left off the shortlist (22)

| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; misread must-haves) |
|---|---|---|---|---|---|
| eb-paderborn | p0241 | synonym | Elektroniker BT | 11 | – |
| eb-paderborn | p0084 | buried:beruf | k. A. | 12 | – |
| eb-paderborn | p0131 | plain | Mechatroniker | 15 | – |
| eb-paderborn | p0182 | synonym | Automatisierungselektroniker | 21 | – |
| eb-paderborn | p0331 | buried:zertifikate | Servicetechniker Mechatronik | 22 | – |
| eb-paderborn | p0370 | synonym | Servicetechniker Mechatronik | 24 | – |
| cnc-guetersloh | p0151 | buried:zertifikate | Industriemechaniker | 11 | – |
| cnc-guetersloh | p0076 | buried:erfahrung | Industriemechaniker | 13 | – |
| cnc-guetersloh | p0244 | synonym | Maschinenschlosser | 17 | – |
| cnc-guetersloh | p0061 | buried:beruf | k. A. | 20 | – |
| cnc-guetersloh | p0035 | buried:beruf | k. A. | 21 | – |
| cnc-guetersloh | p0287 | synonym | Betriebsschlosser | 24 | – |
| cnc-guetersloh | p0030 | synonym | Betriebsschlosser | 25 | – |
| service-bielefeld | p0370 | synonym | Servicetechniker Mechatronik | 12 | – |
| service-bielefeld | p0353 | buried:fuehrerschein | Informationselektroniker Geräte- und Systemtechnik | 13 | – |
| service-bielefeld | p0045 | plain | Mechatroniker | 20 | – |
| service-bielefeld | p0352 | plain | Mechatroniker | 21 | – |
| service-bielefeld | p0012 | synonym | Mechatroniker/in IHK | 23 | – |
| service-bielefeld | p0131 | plain | Mechatroniker | 26 | – |
| service-bielefeld | p0100 | buried:beruf | k. A. | 41 | – |
| … | 2 more in `run.json` | | | | |

## Fits `field-filter` left off the shortlist (26)

| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; misread must-haves) |
|---|---|---|---|---|---|
| eb-paderborn | p0332 | synonym | Elektroniker FR Betriebstechnik | 6 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0047 | buried:zertifikate | Elektroniker für Betriebstechnik | 39 | Feld leer oder unpassend: zertifikate |
| eb-paderborn | p0307 | synonym | Elektroniker BT | 41 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0282 | buried:erfahrung | E-Techniker Betriebstechnik | 43 | Feld leer oder unpassend: beruf, erfahrung |
| eb-paderborn | p0241 | synonym | Elektroniker BT | 52 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0084 | buried:beruf | k. A. | 55 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0182 | synonym | Automatisierungselektroniker | 105 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0331 | buried:zertifikate | Servicetechniker Mechatronik | 107 | Feld leer oder unpassend: beruf, zertifikate |
| eb-paderborn | p0370 | synonym | Servicetechniker Mechatronik | 114 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0285 | synonym | CNC-Fräser | 7 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0151 | buried:zertifikate | Industriemechaniker | 36 | Feld leer oder unpassend: zertifikate |
| cnc-guetersloh | p0076 | buried:erfahrung | Industriemechaniker | 40 | Feld leer oder unpassend: erfahrung |
| cnc-guetersloh | p0244 | synonym | Maschinenschlosser | 75 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0061 | buried:beruf | k. A. | 88 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0035 | buried:beruf | k. A. | 98 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0287 | synonym | Betriebsschlosser | 102 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0030 | synonym | Betriebsschlosser | 104 | Feld leer oder unpassend: beruf |
| service-bielefeld | p0155 | buried:fuehrerschein | Elektroniker für Energie- und Gebäudetechnik | 11 | Feld leer oder unpassend: fuehrerschein |
| service-bielefeld | p0080 | synonym | Servicetechniker Mechatronik | 47 | Feld leer oder unpassend: beruf |
| service-bielefeld | p0307 | synonym | Elektroniker BT | 62 | Feld leer oder unpassend: beruf |
| … | 6 more in `run.json` | | | | |

## Fits `claude-rerank (top 50)` left off the shortlist (6)

| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; misread must-haves) |
|---|---|---|---|---|---|
| eb-paderborn | p0370 | synonym | Servicetechniker Mechatronik | 13 | Ob eine abgeschlossene Ausbildung als Mechatroniker vorliegt, lässt sich aus der Tätigkeitsbezeichnung nicht ableiten – das muss geklärt werden. [Beruf gelesen:; misread: Beruf |
| eb-paderborn | p0331 | buried:zertifikate | Servicetechniker Mechatronik | 20 | Servicetechniker Mechatronik ist kein anerkannter Ausbildungsberuf; ob ein Abschluss als Mechatroniker vorliegt, muss noch geklärt werden. [Beruf gelesen: Servi; misread: Beruf |
| cnc-guetersloh | p0285 | synonym | CNC-Fräser | 12 | Unklar ist der Abschluss: 'CNC-Fräser' ist eine Tätigkeitsbezeichnung, und eine Ausbildung zum Zerspanungsmechaniker oder Fräser ist nicht belegt. Alle anderen ; misread: Beruf |
| service-bielefeld | p0370 | synonym | Servicetechniker Mechatronik | 12 | Ein anerkannter Ausbildungsabschluss ist nicht belegt, nur die Tätigkeit als Servicetechniker. [Beruf gelesen: unklar (Servicetechniker Mechatronik, kein Ausbil; misread: Beruf |
| service-bielefeld | p0034 | synonym | Betriebselektroniker | 92 | nicht im Vorfilter top 50 (Keyword-Rang 92) |
| service-bielefeld | p0104 | buried:beruf | k. A. | 100 | nicht im Vorfilter top 50 (Keyword-Rang 100) |

## Does the name move the ranking?

The pool is ranked again unchanged (repeat) and with every name swapped to another origin, same gender, the surname in the notes included (swap). Graded: the base run's top 50 per vacancy, and whether each stays in or out of the top 10. A swap flip rate above the repeat rate points at the name.

| Matcher | Flips on swap | Flips on repeat | Mean rank shift swap / repeat |
|---|---|---|---|
| `bm25` | 0% (0/300) [0–1] | 0% (0/150) [0–2] | 0.0 / 0.0 |
| `keyword` | 0% (0/300) [0–1] | 0% (0/150) [0–2] | 0.0 / 0.0 |
| `field-filter` | 0% (0/300) [0–1] | 0% (0/150) [0–2] | 0.0 / 0.0 |
| `claude-rerank (top 50)` | 1% (2/300) [0–2] | 4% (6/150) [2–8] | 2.68 / 2.53 |

Lost a shortlist place, by origin: every base/swap pair tests both origins involved and counts against the side left out while the other got in. Without a name effect every origin sits near the repeat rate.

| Origin | `bm25` | `keyword` | `field-filter` | `claude-rerank (top 50)` |
|---|---|---|---|---|
| ar | 0% (0/83) [0–4] | 0% (0/71) [0–5] | 0% (0/83) [0–4] | 0% (0/71) [0–5] |
| de | 0% (0/190) [0–2] | 0% (0/186) [0–2] | 0% (0/187) [0–2] | 0% (0/186) [0–2] |
| pl | 0% (0/99) [0–4] | 0% (0/122) [0–3] | 0% (0/101) [0–4] | 1% (1/122) [0–4] |
| tr | 0% (0/119) [0–3] | 0% (0/122) [0–3] | 0% (0/122) [0–3] | 0% (0/122) [0–3] |
| ua | 0% (0/109) [0–3] | 0% (0/99) [0–4] | 0% (0/107) [0–3] | 1% (1/99) [0–6] |

## Cost

60 model calls (60 attempts incl. retries), 378,547 input and 170,510 output tokens, served by claude-opus-5-5 (60). List-price equivalent reported by the CLI: $5.34.

## How this was measured

Every profile is synthetic: hidden facts (trade, years, certificates, licence, town, shift and on-call willingness) and a presentation of those facts as an ATS record, with some fields left empty and the fact stated only in messy recruiter notes, and the trade shown by its official name or an old name, synonym or abbreviation. The true fits of each vacancy follow from its must-have rules applied to the hidden facts. Planted per vacancy: 4 plain, 4 synonym and 4 buried fits, and 2 near-misses per must-have; background profiles that would fit are redrawn. Fits planted for one vacancy can fit another and are counted there too. No real candidate data is involved.
