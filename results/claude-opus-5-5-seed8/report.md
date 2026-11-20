# poolgate report

Pool: 400 synthetic profiles, seed 8, 3 vacancies. Matchers: `bm25`, `keyword`, `keyword+syn`, `field-filter-exact`, `field-filter`, `field-filter+syn`, `claude-rerank (top 50)`.

| Vacancy | True fits | of which plain / synonym / buried | Near-misses |
|---|---|---|---|
| Elektroniker für Betriebstechnik (m/w/d) Instandhaltung (Paderborn, 35 km) | 12 | 4 / 4 / 4 | 33 |
| CNC-Fräser / Zerspanungsmechaniker (m/w/d) (Gütersloh, 30 km) | 12 | 4 / 4 / 4 | 28 |
| Servicetechniker Sicherheitstechnik (m/w/d) im Außendienst OWL (Bielefeld, 50 km) | 12 | 4 / 4 / 4 | 82 |

## Headline

Brackets are 95% Wilson intervals. The first row puts every matcher on equal footing: its top k, with k the number of true fits of each vacancy, so the ceiling is 100% for all. The shortlist is the matcher's own yes-list where it gives one, else its fixed top 10, which cannot hold every fit.

| Measure | `bm25` | `keyword` | `keyword+syn` | `field-filter-exact` | `field-filter` | `field-filter+syn` | `claude-rerank (top 50)` |
|---|---|---|---|---|---|---|---|
| Recall at k = true fits (ceiling 100%) | 22% (8/36) [12–38] | 50% (18/36) [34–66] | 67% (24/36) [50–80] | 42% (15/36) [27–58] | 53% (19/36) [37–68] | 72% (26/36) [56–84] | 92% (33/36) [78–97] |
| Recall@20 (ceiling 100%) | 33% (12/36) [20–50] | 78% (28/36) [62–88] | 83% (30/36) [68–92] | 53% (19/36) [37–68] | 64% (23/36) [48–78] | 75% (27/36) [59–86] | 92% (33/36) [78–97] |
| Recall@10 (ceiling 83%: more fits than places) | 19% (7/36) [10–35] | 47% (17/36) [32–63] | 56% (20/36) [40–70] | 42% (15/36) [27–58] | 53% (19/36) [37–68] | 69% (25/36) [53–82] | 81% (29/36) [65–90] |
| Precision@10 | 23% (7/30) [12–41] | 57% (17/30) [39–73] | 67% (20/30) [49–81] | 50% (15/30) [33–67] | 63% (19/30) [46–78] | 83% (25/30) [66–93] | 97% (29/30) [83–99] |
| Shortlist precision | 23% (7/30) [12–41] | 57% (17/30) [39–73] | 67% (20/30) [49–81] | 100% (12/12) [76–100] | 100% (16/16) [81–100] | 100% (24/24) [86–100] | 100% (33/33) [90–100] |
| Shortlist recall | 19% (7/36) [10–35] (ceiling 83%) | 47% (17/36) [32–63] (ceiling 83%) | 56% (20/36) [40–70] (ceiling 83%) | 33% (12/36) [20–50] | 44% (16/36) [30–60] | 67% (24/36) [50–80] | 92% (33/36) [78–97] |
| Shortlist size (all vacancies) | 30 (top 10) | 30 (top 10) | 30 (top 10) | 12 | 16 | 24 | 33 |
| Near-misses in top 10 | 9% (13/143) [5–15] | 7% (10/143) [4–12] | 6% (8/143) [3–11] | 8% (11/143) [4–13] | 6% (9/143) [3–12] | 1% (2/143) [0–5] | 1% (1/143) [0–4] |
| Near-misses in shortlist | 13 | 10 | 8 | 0 | 0 | 0 | 0 |
| True fits that reached the model | – | – | – | – | – | – | 92% (33/36) [78–97] |
| Near-misses that reached the model | – | – | – | – | – | – | 31% (45/143) [24–39] |

## Which fits are found

Recall@20 and shortlist recall by how the fit is presented.

| Case | `bm25` @20 / shortlist | `keyword` @20 / shortlist | `keyword+syn` @20 / shortlist | `field-filter-exact` @20 / shortlist | `field-filter` @20 / shortlist | `field-filter+syn` @20 / shortlist | `claude-rerank (top 50)` @20 / shortlist |
|---|---|---|---|---|---|---|---|
| plain (official title, facts in fields) | 42% [19–68] / 33% (4/12) [14–61] | 83% [55–95] / 58% (7/12) [32–81] | 67% [39–86] / 50% (6/12) [25–75] | 100% [76–100] / 100% (12/12) [76–100] | 100% [76–100] / 100% (12/12) [76–100] | 100% [76–100] / 100% (12/12) [76–100] | 100% [76–100] / 100% (12/12) [76–100] |
| synonym (Beruf field: another spelling, an abbreviation or a predecessor name) | 17% [5–45] / 17% (2/12) [5–45] | 67% [39–86] / 25% (3/12) [9–53] | 92% [65–99] / 67% (8/12) [39–86] | 17% [5–45] / 0% (0/12) [0–24] | 50% [25–75] / 33% (4/12) [14–61] | 100% [76–100] / 100% (12/12) [76–100] | 83% [55–95] / 83% (10/12) [55–95] |
| buried (a must-have fact only in the notes) | 42% [19–68] / 8% (1/12) [1–35] | 83% [55–95] / 58% (7/12) [32–81] | 92% [65–99] / 50% (6/12) [25–75] | 42% [19–68] / 0% (0/12) [0–24] | 42% [19–68] / 0% (0/12) [0–24] | 25% [9–53] / 0% (0/12) [0–24] | 92% [65–99] / 92% (11/12) [65–99] |
| · synonym: abbreviation | 0% [0–79] / 0% (0/1) [0–79] | 100% [21–100] / 0% (0/1) [0–79] | 100% [21–100] / 100% (1/1) [21–100] | 0% [0–79] / 0% (0/1) [0–79] | 0% [0–79] / 0% (0/1) [0–79] | 100% [21–100] / 100% (1/1) [21–100] | 100% [21–100] / 100% (1/1) [21–100] |
| · synonym: predecessor name | 29% [8–64] / 29% (2/7) [8–64] | 57% [25–84] / 29% (2/7) [8–64] | 100% [65–100] / 100% (7/7) [65–100] | 29% [8–64] / 0% (0/7) [0–35] | 29% [8–64] / 0% (0/7) [0–35] | 100% [65–100] / 100% (7/7) [65–100] | 71% [36–92] / 71% (5/7) [36–92] |
| · synonym: spelling variant | 0% [0–49] / 0% (0/4) [0–49] | 75% [30–95] / 25% (1/4) [5–70] | 75% [30–95] / 0% (0/4) [0–49] | 0% [0–49] / 0% (0/4) [0–49] | 100% [51–100] / 100% (4/4) [51–100] | 100% [51–100] / 100% (4/4) [51–100] | 100% [51–100] / 100% (4/4) [51–100] |
| · buried: Beruf | 0% [0–56] / 0% (0/3) [0–56] | 100% [44–100] / 33% (1/3) [6–79] | 100% [44–100] / 0% (0/3) [0–56] | 0% [0–56] / 0% (0/3) [0–56] | 0% [0–56] / 0% (0/3) [0–56] | 0% [0–56] / 0% (0/3) [0–56] | 100% [44–100] / 100% (3/3) [44–100] |
| · buried: Erfahrung | 33% [6–79] / 0% (0/3) [0–56] | 67% [21–94] / 67% (2/3) [21–94] | 67% [21–94] / 67% (2/3) [21–94] | 33% [6–79] / 0% (0/3) [0–56] | 33% [6–79] / 0% (0/3) [0–56] | 33% [6–79] / 0% (0/3) [0–56] | 67% [21–94] / 67% (2/3) [21–94] |
| · buried: Führerschein | 0% [0–79] / 0% (0/1) [0–79] | 0% [0–79] / 0% (0/1) [0–79] | 100% [21–100] / 0% (0/1) [0–79] | 0% [0–79] / 0% (0/1) [0–79] | 0% [0–79] / 0% (0/1) [0–79] | 0% [0–79] / 0% (0/1) [0–79] | 100% [21–100] / 100% (1/1) [21–100] |
| · buried: Rufbereitschaft | 100% [21–100] / 0% (0/1) [0–79] | 100% [21–100] / 100% (1/1) [21–100] | 100% [21–100] / 100% (1/1) [21–100] | 100% [21–100] / 0% (0/1) [0–79] | 100% [21–100] / 0% (0/1) [0–79] | 100% [21–100] / 0% (0/1) [0–79] | 100% [21–100] / 100% (1/1) [21–100] |
| · buried: Schicht | 100% [34–100] / 50% (1/2) [9–91] | 100% [34–100] / 100% (2/2) [34–100] | 100% [34–100] / 100% (2/2) [34–100] | 100% [34–100] / 0% (0/2) [0–66] | 100% [34–100] / 0% (0/2) [0–66] | 50% [9–91] / 0% (0/2) [0–66] | 100% [34–100] / 100% (2/2) [34–100] |
| · buried: Zertifikat | 50% [9–91] / 0% (0/2) [0–66] | 100% [34–100] / 50% (1/2) [9–91] | 100% [34–100] / 50% (1/2) [9–91] | 50% [9–91] / 0% (0/2) [0–66] | 50% [9–91] / 0% (0/2) [0–66] | 0% [0–66] / 0% (0/2) [0–66] | 100% [34–100] / 100% (2/2) [34–100] |

## Near-misses let in

Profiles that fail exactly one must-have and look right otherwise, by the must-have they fail: share that reached the top 10. 30 of 143 were planted as look-alikes; the rest are background profiles that happen to fail exactly one must-have.

| Fails | `bm25` | `keyword` | `keyword+syn` | `field-filter-exact` | `field-filter` | `field-filter+syn` | `claude-rerank (top 50)` |
|---|---|---|---|---|---|---|---|
| Beruf | 0% (0/11) [0–26] | 0% (0/11) [0–26] | 0% (0/11) [0–26] | 0% (0/11) [0–26] | 0% (0/11) [0–26] | 0% (0/11) [0–26] | 0% (0/11) [0–26] |
| Erfahrung | 11% (1/9) [2–44] | 33% (3/9) [12–65] | 0% (0/9) [0–30] | 11% (1/9) [2–44] | 11% (1/9) [2–44] | 0% (0/9) [0–30] | 0% (0/9) [0–30] |
| Zertifikat | 0% (0/22) [0–15] | 14% (3/22) [5–33] | 14% (3/22) [5–33] | 0% (0/22) [0–15] | 0% (0/22) [0–15] | 0% (0/22) [0–15] | 0% (0/22) [0–15] |
| Führerschein | 10% (1/10) [2–40] | 10% (1/10) [2–40] | 30% (3/10) [11–60] | 10% (1/10) [2–40] | 0% (0/10) [0–28] | 0% (0/10) [0–28] | 0% (0/10) [0–28] |
| Entfernung | 30% (9/30) [17–48] | 0% (0/30) [0–11] | 0% (0/30) [0–11] | 23% (7/30) [12–41] | 20% (6/30) [10–37] | 3% (1/30) [1–17] | 0% (0/30) [0–11] |
| Schicht | 7% (1/15) [1–30] | 7% (1/15) [1–30] | 0% (0/15) [0–20] | 7% (1/15) [1–30] | 7% (1/15) [1–30] | 7% (1/15) [1–30] | 0% (0/15) [0–20] |
| Rufbereitschaft | 2% (1/46) [0–11] | 4% (2/46) [1–15] | 4% (2/46) [1–15] | 2% (1/46) [0–11] | 2% (1/46) [0–11] | 0% (0/46) [0–8] | 2% (1/46) [0–11] |

## How `claude-rerank (top 50)` read the must-haves

Every judgement the matcher returned, against the rule applied to the hidden facts. "unklar" counts as not right.

| Must-have | right | wrong | unklar |
|---|---|---|---|
| Beruf | 99% (149/150) [96–100] | 1 | 0 |
| Erfahrung | 99% (149/150) [96–100] | 0 | 1 |
| Zertifikat | 100% (100/100) [96–100] | 0 | 0 |
| Führerschein | 100% (50/50) [93–100] | 0 | 0 |
| Entfernung | 100% (150/150) [98–100] | 0 | 0 |
| Schicht | 100% (100/100) [96–100] | 0 | 0 |
| Rufbereitschaft | 100% (50/50) [93–100] | 0 | 0 |

## Fits `bm25` left off the shortlist (29)

| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; misread must-haves) |
|---|---|---|---|---|---|
| eb-paderborn | p0332 | plain | Elektroniker für Automatisierungstechnik | 11 | – |
| eb-paderborn | p0021 | buried:zertifikate | Elektroniker für Betriebstechnik | 15 | – |
| eb-paderborn | p0004 | buried:erfahrung | Elektroniker für Betriebstechnik | 22 | – |
| eb-paderborn | p0367 | plain | Elektroniker für Automatisierungstechnik | 32 | – |
| eb-paderborn | p0097 | synonym:predecessor | Energieelektroniker Fachrichtung Betriebstechnik | 52 | – |
| eb-paderborn | p0266 | buried:beruf | k. A. | 56 | – |
| eb-paderborn | p0347 | synonym:predecessor | Energieelektroniker Fachrichtung Betriebstechnik | 66 | – |
| eb-paderborn | p0281 | synonym:variant | Mechatroniker (IHK) | 69 | – |
| eb-paderborn | p0314 | synonym:variant | Mechatroniker (IHK) | 75 | – |
| eb-paderborn | p0392 | plain | Mechatroniker | 78 | – |
| cnc-guetersloh | p0286 | buried:erfahrung | Zerspanungsmechaniker/-in | 13 | – |
| cnc-guetersloh | p0099 | buried:schicht | Zerspanungsmechaniker/-in | 16 | – |
| cnc-guetersloh | p0288 | synonym:variant | Industriemechaniker/-in | 40 | – |
| cnc-guetersloh | p0167 | plain | Industriemechaniker | 43 | – |
| cnc-guetersloh | p0037 | buried:zertifikate | Industriemechaniker | 65 | – |
| cnc-guetersloh | p0339 | synonym:abbrev | Industriemech. | 90 | – |
| cnc-guetersloh | p0301 | buried:beruf | k. A. | 92 | – |
| service-bielefeld | p0229 | buried:rufbereitschaft | Elektroniker, Fachrichtung Energie- und Gebäudetechnik | 13 | – |
| service-bielefeld | p0242 | buried:beruf | k. A. | 47 | – |
| service-bielefeld | p0204 | plain | Informationselektroniker | 52 | – |
| … | 9 more in `run.json` | | | | |

## Fits `keyword` left off the shortlist (19)

| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; misread must-haves) |
|---|---|---|---|---|---|
| eb-paderborn | p0097 | synonym:predecessor | Energieelektroniker Fachrichtung Betriebstechnik | 13 | – |
| eb-paderborn | p0266 | buried:beruf | k. A. | 14 | – |
| eb-paderborn | p0347 | synonym:predecessor | Energieelektroniker Fachrichtung Betriebstechnik | 15 | – |
| eb-paderborn | p0281 | synonym:variant | Mechatroniker (IHK) | 16 | – |
| eb-paderborn | p0314 | synonym:variant | Mechatroniker (IHK) | 18 | – |
| eb-paderborn | p0392 | plain | Mechatroniker | 19 | – |
| cnc-guetersloh | p0167 | plain | Industriemechaniker | 11 | – |
| cnc-guetersloh | p0037 | buried:zertifikate | Industriemechaniker | 14 | – |
| cnc-guetersloh | p0339 | synonym:abbrev | Industriemech. | 18 | – |
| cnc-guetersloh | p0301 | buried:beruf | k. A. | 20 | – |
| service-bielefeld | p0178 | plain | Mechatroniker | 20 | – |
| service-bielefeld | p0318 | plain | Mechatroniker | 21 | – |
| service-bielefeld | p0011 | synonym:variant | Mechatroniker/-in | 24 | – |
| service-bielefeld | p0075 | plain | Mechatroniker | 25 | – |
| service-bielefeld | p0025 | synonym:predecessor | Energieelektroniker Fachrichtung Betriebstechnik | 31 | – |
| service-bielefeld | p0271 | buried:fuehrerschein | Energieelektroniker Fachrichtung Betriebstechnik | 35 | – |
| service-bielefeld | p0213 | buried:erfahrung | Elektroinstallateur | 69 | – |
| service-bielefeld | p0195 | synonym:predecessor | Radio- und Fernsehtechniker | 101 | – |
| service-bielefeld | p0013 | synonym:predecessor | Radio- und Fernsehtechniker | 112 | – |

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

## Fits `field-filter-exact` left off the shortlist (24)

| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; misread must-haves) |
|---|---|---|---|---|---|
| eb-paderborn | p0046 | buried:schicht | Elektroniker für Betriebstechnik | 6 | Feld leer oder unpassend: schicht |
| eb-paderborn | p0021 | buried:zertifikate | Elektroniker für Betriebstechnik | 17 | Feld leer oder unpassend: zertifikate |
| eb-paderborn | p0004 | buried:erfahrung | Elektroniker für Betriebstechnik | 24 | Feld leer oder unpassend: erfahrung |
| eb-paderborn | p0097 | synonym:predecessor | Energieelektroniker Fachrichtung Betriebstechnik | 53 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0266 | buried:beruf | k. A. | 57 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0347 | synonym:predecessor | Energieelektroniker Fachrichtung Betriebstechnik | 67 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0281 | synonym:variant | Mechatroniker (IHK) | 70 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0314 | synonym:variant | Mechatroniker (IHK) | 76 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0127 | synonym:predecessor | Fräser | 5 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0053 | synonym:predecessor | Zerspanungsmechaniker Fachrichtung Frästechnik | 6 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0286 | buried:erfahrung | Zerspanungsmechaniker/-in | 14 | Feld leer oder unpassend: beruf, erfahrung |
| cnc-guetersloh | p0099 | buried:schicht | Zerspanungsmechaniker/-in | 17 | Feld leer oder unpassend: beruf, schicht |
| cnc-guetersloh | p0288 | synonym:variant | Industriemechaniker/-in | 41 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0037 | buried:zertifikate | Industriemechaniker | 65 | Feld leer oder unpassend: zertifikate |
| cnc-guetersloh | p0339 | synonym:abbrev | Industriemech. | 90 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0301 | buried:beruf | k. A. | 92 | Feld leer oder unpassend: beruf |
| service-bielefeld | p0229 | buried:rufbereitschaft | Elektroniker, Fachrichtung Energie- und Gebäudetechnik | 17 | Feld leer oder unpassend: beruf, rufbereitschaft |
| service-bielefeld | p0242 | buried:beruf | k. A. | 51 | Feld leer oder unpassend: beruf |
| service-bielefeld | p0011 | synonym:variant | Mechatroniker/-in | 96 | Feld leer oder unpassend: beruf |
| service-bielefeld | p0025 | synonym:predecessor | Energieelektroniker Fachrichtung Betriebstechnik | 111 | Feld leer oder unpassend: beruf |
| … | 4 more in `run.json` | | | | |

## Fits `field-filter` left off the shortlist (20)

| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; misread must-haves) |
|---|---|---|---|---|---|
| eb-paderborn | p0046 | buried:schicht | Elektroniker für Betriebstechnik | 8 | Feld leer oder unpassend: schicht |
| eb-paderborn | p0021 | buried:zertifikate | Elektroniker für Betriebstechnik | 19 | Feld leer oder unpassend: zertifikate |
| eb-paderborn | p0004 | buried:erfahrung | Elektroniker für Betriebstechnik | 26 | Feld leer oder unpassend: erfahrung |
| eb-paderborn | p0097 | synonym:predecessor | Energieelektroniker Fachrichtung Betriebstechnik | 55 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0266 | buried:beruf | k. A. | 59 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0347 | synonym:predecessor | Energieelektroniker Fachrichtung Betriebstechnik | 69 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0127 | synonym:predecessor | Fräser | 6 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0053 | synonym:predecessor | Zerspanungsmechaniker Fachrichtung Frästechnik | 7 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0286 | buried:erfahrung | Zerspanungsmechaniker/-in | 15 | Feld leer oder unpassend: erfahrung |
| cnc-guetersloh | p0099 | buried:schicht | Zerspanungsmechaniker/-in | 18 | Feld leer oder unpassend: schicht |
| cnc-guetersloh | p0037 | buried:zertifikate | Industriemechaniker | 65 | Feld leer oder unpassend: zertifikate |
| cnc-guetersloh | p0339 | synonym:abbrev | Industriemech. | 90 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0301 | buried:beruf | k. A. | 92 | Feld leer oder unpassend: beruf |
| service-bielefeld | p0229 | buried:rufbereitschaft | Elektroniker, Fachrichtung Energie- und Gebäudetechnik | 18 | Feld leer oder unpassend: rufbereitschaft |
| service-bielefeld | p0242 | buried:beruf | k. A. | 52 | Feld leer oder unpassend: beruf |
| service-bielefeld | p0025 | synonym:predecessor | Energieelektroniker Fachrichtung Betriebstechnik | 111 | Feld leer oder unpassend: beruf |
| service-bielefeld | p0271 | buried:fuehrerschein | Energieelektroniker Fachrichtung Betriebstechnik | 147 | Feld leer oder unpassend: beruf, fuehrerschein |
| service-bielefeld | p0213 | buried:erfahrung | Elektroinstallateur | 256 | Feld leer oder unpassend: beruf, erfahrung |
| service-bielefeld | p0195 | synonym:predecessor | Radio- und Fernsehtechniker | 331 | Feld leer oder unpassend: beruf |
| service-bielefeld | p0013 | synonym:predecessor | Radio- und Fernsehtechniker | 371 | Feld leer oder unpassend: beruf |

## Fits `field-filter+syn` left off the shortlist (12)

| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; misread must-haves) |
|---|---|---|---|---|---|
| eb-paderborn | p0046 | buried:schicht | Elektroniker für Betriebstechnik | 10 | Feld leer oder unpassend: schicht |
| eb-paderborn | p0021 | buried:zertifikate | Elektroniker für Betriebstechnik | 33 | Feld leer oder unpassend: zertifikate |
| eb-paderborn | p0004 | buried:erfahrung | Elektroniker für Betriebstechnik | 41 | Feld leer oder unpassend: erfahrung |
| eb-paderborn | p0266 | buried:beruf | k. A. | 49 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0286 | buried:erfahrung | Zerspanungsmechaniker/-in | 12 | Feld leer oder unpassend: erfahrung |
| cnc-guetersloh | p0099 | buried:schicht | Zerspanungsmechaniker/-in | 26 | Feld leer oder unpassend: schicht |
| cnc-guetersloh | p0301 | buried:beruf | k. A. | 53 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0037 | buried:zertifikate | Industriemechaniker | 98 | Feld leer oder unpassend: zertifikate |
| service-bielefeld | p0229 | buried:rufbereitschaft | Elektroniker, Fachrichtung Energie- und Gebäudetechnik | 20 | Feld leer oder unpassend: rufbereitschaft |
| service-bielefeld | p0242 | buried:beruf | k. A. | 58 | Feld leer oder unpassend: beruf |
| service-bielefeld | p0271 | buried:fuehrerschein | Energieelektroniker Fachrichtung Betriebstechnik | 61 | Feld leer oder unpassend: fuehrerschein |
| service-bielefeld | p0213 | buried:erfahrung | Elektroinstallateur | 113 | Feld leer oder unpassend: erfahrung |

## Fits `claude-rerank (top 50)` left off the shortlist (3)

| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; misread must-haves) |
|---|---|---|---|---|---|
| service-bielefeld | p0213 | buried:erfahrung | Elektroinstallateur | 69 | nicht im Vorfilter top 50 (Keyword-Rang 69) |
| service-bielefeld | p0195 | synonym:predecessor | Radio- und Fernsehtechniker | 101 | nicht im Vorfilter top 50 (Keyword-Rang 101) |
| service-bielefeld | p0013 | synonym:predecessor | Radio- und Fernsehtechniker | 112 | nicht im Vorfilter top 50 (Keyword-Rang 112) |

## Does the name move the ranking?

The pool is ranked again unchanged (repeat) and with every name swapped to another origin, same gender, the surname in the notes included (swap). Graded: the base run's top 50 per vacancy, and whether each stays in or out of the top 10 and, where the matcher gives one, of its own yes-list. A swap flip rate above the repeat rate points at the name. Matchers that never read the name (bm25, keyword, field-filter) are at 0 by construction.

| Matcher | Top-10 flips on swap | on repeat | Own-list flips on swap | on repeat | Mean rank shift swap / repeat |
|---|---|---|---|---|---|
| `bm25` | 0% (0/300) [0–1] | 0% (0/150) [0–2] | – | – | 0.0 / 0.0 |
| `keyword` | 0% (0/300) [0–1] | 0% (0/150) [0–2] | – | – | 0.0 / 0.0 |
| `keyword+syn` | 0% (0/300) [0–1] | 0% (0/150) [0–2] | – | – | 0.0 / 0.0 |
| `field-filter-exact` | 0% (0/300) [0–1] | 0% (0/150) [0–2] | 0% (0/300) [0–1] | 0% (0/150) [0–2] | 0.0 / 0.0 |
| `field-filter` | 0% (0/300) [0–1] | 0% (0/150) [0–2] | 0% (0/300) [0–1] | 0% (0/150) [0–2] | 0.0 / 0.0 |
| `field-filter+syn` | 0% (0/300) [0–1] | 0% (0/150) [0–2] | 0% (0/300) [0–1] | 0% (0/150) [0–2] | 0.0 / 0.0 |
| `claude-rerank (top 50)` | 2% (6/300) [1–4] | 3% (4/150) [1–7] | 0% (0/300) [0–1] | 0% (0/150) [0–2] | 2.78 / 3.0 |

Lost a top-10 place, by origin: every base/swap pair tests both origins involved and counts against the side left out while the other got in. Without a name effect every origin sits near the repeat rate.

| Origin | `bm25` | `keyword` | `keyword+syn` | `field-filter-exact` | `field-filter` | `field-filter+syn` | `claude-rerank (top 50)` |
|---|---|---|---|---|---|---|---|
| ar | 0% (0/103) [0–4] | 0% (0/101) [0–4] | 0% (0/104) [0–4] | 0% (0/101) [0–4] | 0% (0/101) [0–4] | 0% (0/78) [0–5] | 0% (0/101) [0–4] |
| de | 0% (0/184) [0–2] | 0% (0/186) [0–2] | 0% (0/183) [0–2] | 0% (0/181) [0–2] | 0% (0/181) [0–2] | 0% (0/187) [0–2] | 1% (2/186) [0–4] |
| pl | 0% (0/102) [0–4] | 0% (0/98) [0–4] | 0% (0/95) [0–4] | 0% (0/108) [0–3] | 0% (0/109) [0–3] | 0% (0/108) [0–3] | 1% (1/98) [0–6] |
| tr | 0% (0/107) [0–3] | 0% (0/104) [0–4] | 0% (0/102) [0–4] | 0% (0/106) [0–3] | 0% (0/106) [0–3] | 0% (0/115) [0–3] | 1% (1/104) [0–5] |
| ua | 0% (0/104) [0–4] | 0% (0/111) [0–3] | 0% (0/116) [0–3] | 0% (0/104) [0–4] | 0% (0/103) [0–4] | 0% (0/112) [0–3] | 2% (2/111) [0–6] |

## Cost

60 model calls (60 attempts incl. retries), 396,716 input and 170,624 output tokens, served by claude-opus-5-5 (60). List-price equivalent reported by the CLI: $5.22.

## How this was measured

Every profile is synthetic: hidden facts (trade, years, certificates, licence, town, shift and on-call willingness) and a presentation of those facts as an ATS record, with some fields left empty and the fact stated only in messy recruiter notes, and the trade shown by its official name or an old name, synonym or abbreviation. The true fits of each vacancy follow from its must-have rules applied to the hidden facts. Planted per vacancy: 4 plain, 4 synonym and 4 buried fits, and 2 near-misses per must-have; background profiles that would fit are redrawn. A profile planted for one vacancy (as fit or near-miss) can be a true fit for another and is counted there too. Certificate lists are complete: a certificate not named is absent. Distances are computed and shown to the model, so its Entfernung judgements are not a reading test. No real candidate data is involved.
