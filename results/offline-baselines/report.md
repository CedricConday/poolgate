# poolgate report

Pool: 400 synthetic profiles, seed 7, 3 vacancies. Matchers: `bm25`, `keyword`, `keyword+syn`, `field-filter-exact`, `field-filter`, `field-filter+syn`.

| Vacancy | True fits | of which plain / synonym / buried | Near-misses |
|---|---|---|---|
| Elektroniker für Betriebstechnik (m/w/d) Instandhaltung (Paderborn, 35 km) | 12 | 4 / 4 / 4 | 27 |
| CNC-Fräser / Zerspanungsmechaniker (m/w/d) (Gütersloh, 30 km) | 12 | 4 / 4 / 4 | 39 |
| Servicetechniker Sicherheitstechnik (m/w/d) im Außendienst OWL (Bielefeld, 50 km) | 15 | 6 / 5 / 4 | 79 |

## Headline

Brackets are 95% Wilson intervals. The first row puts every matcher on equal footing: its top k, with k the number of true fits of each vacancy, so the ceiling is 100% for all. The shortlist is the matcher's own yes-list where it gives one, else its fixed top 10, which cannot hold every fit.

| Measure | `bm25` | `keyword` | `keyword+syn` | `field-filter-exact` | `field-filter` | `field-filter+syn` |
|---|---|---|---|---|---|---|
| Recall at k = true fits (ceiling 100%) | 26% (10/39) [15–41] | 59% (23/39) [43–73] | 56% (22/39) [41–71] | 41% (16/39) [27–57] | 54% (21/39) [39–68] | 72% (28/39) [56–83] |
| Recall@20 (ceiling 100%) | 38% (15/39) [25–54] | 74% (29/39) [59–85] | 77% (30/39) [62–87] | 51% (20/39) [36–66] | 62% (24/39) [46–75] | 74% (29/39) [59–85] |
| Recall@10 (ceiling 77%: more fits than places) | 21% (8/39) [11–36] | 44% (17/39) [29–59] | 44% (17/39) [29–59] | 41% (16/39) [27–57] | 54% (21/39) [39–68] | 69% (27/39) [54–81] |
| Precision@10 | 27% (8/30) [14–44] | 57% (17/30) [39–73] | 57% (17/30) [39–73] | 53% (16/30) [36–70] | 70% (21/30) [52–83] | 90% (27/30) [74–97] |
| Shortlist precision | 27% (8/30) [14–44] | 57% (17/30) [39–73] | 57% (17/30) [39–73] | 100% (13/13) [77–100] | 100% (19/19) [83–100] | 100% (27/27) [88–100] |
| Shortlist recall | 21% (8/39) [11–36] (ceiling 77%) | 44% (17/39) [29–59] (ceiling 77%) | 44% (17/39) [29–59] (ceiling 77%) | 33% (13/39) [21–49] | 49% (19/39) [34–64] | 69% (27/39) [54–81] |
| Shortlist size (all vacancies) | 30 (top 10) | 30 (top 10) | 30 (top 10) | 13 | 19 | 27 |
| Near-misses in top 10 | 10% (14/145) [6–16] | 9% (13/145) [5–15] | 9% (13/145) [5–15] | 8% (11/145) [4–13] | 6% (8/145) [3–11] | 1% (1/145) [0–4] |
| Near-misses in shortlist | 14 | 13 | 13 | 0 | 0 | 0 |

## Which fits are found

Recall@20 and shortlist recall by how the fit is presented.

| Case | `bm25` @20 / shortlist | `keyword` @20 / shortlist | `keyword+syn` @20 / shortlist | `field-filter-exact` @20 / shortlist | `field-filter` @20 / shortlist | `field-filter+syn` @20 / shortlist |
|---|---|---|---|---|---|---|
| plain (official title, facts in fields) | 57% [33–79] / 36% (5/14) [16–61] | 86% [60–96] / 64% (9/14) [39–84] | 71% [45–88] / 50% (7/14) [27–73] | 93% [69–99] / 93% (13/14) [69–99] | 100% [78–100] / 100% (14/14) [78–100] | 100% [78–100] / 100% (14/14) [78–100] |
| synonym (Beruf field: another spelling, an abbreviation or a predecessor name) | 31% [13–58] / 15% (2/13) [4–42] | 69% [42–87] / 38% (5/13) [18–64] | 77% [50–92] / 46% (6/13) [23–71] | 31% [13–58] / 0% (0/13) [0–23] | 54% [29–77] / 38% (5/13) [18–64] | 100% [77–100] / 100% (13/13) [77–100] |
| buried (a must-have fact only in the notes) | 25% [9–53] / 8% (1/12) [1–35] | 67% [39–86] / 25% (3/12) [9–53] | 83% [55–95] / 33% (4/12) [14–61] | 25% [9–53] / 0% (0/12) [0–24] | 25% [9–53] / 0% (0/12) [0–24] | 17% [5–45] / 0% (0/12) [0–24] |
| · synonym: abbreviation | 33% [6–79] / 0% (0/3) [0–56] | 100% [44–100] / 33% (1/3) [6–79] | 100% [44–100] / 33% (1/3) [6–79] | 33% [6–79] / 0% (0/3) [0–56] | 33% [6–79] / 0% (0/3) [0–56] | 100% [44–100] / 100% (3/3) [44–100] |
| · synonym: predecessor name | 20% [4–62] / 20% (1/5) [4–62] | 60% [23–88] / 20% (1/5) [4–62] | 60% [23–88] / 60% (3/5) [23–88] | 20% [4–62] / 0% (0/5) [0–43] | 20% [4–62] / 0% (0/5) [0–43] | 100% [57–100] / 100% (5/5) [57–100] |
| · synonym: spelling variant | 40% [12–77] / 20% (1/5) [4–62] | 60% [23–88] / 60% (3/5) [23–88] | 80% [38–96] / 40% (2/5) [12–77] | 40% [12–77] / 0% (0/5) [0–43] | 100% [57–100] / 100% (5/5) [57–100] | 100% [57–100] / 100% (5/5) [57–100] |
| · buried: Beruf | 0% [0–56] / 0% (0/3) [0–56] | 0% [0–56] / 0% (0/3) [0–56] | 67% [21–94] / 0% (0/3) [0–56] | 0% [0–56] / 0% (0/3) [0–56] | 0% [0–56] / 0% (0/3) [0–56] | 0% [0–56] / 0% (0/3) [0–56] |
| · buried: Erfahrung | 33% [6–79] / 33% (1/3) [6–79] | 67% [21–94] / 33% (1/3) [6–79] | 100% [44–100] / 67% (2/3) [21–94] | 33% [6–79] / 0% (0/3) [0–56] | 33% [6–79] / 0% (0/3) [0–56] | 33% [6–79] / 0% (0/3) [0–56] |
| · buried: Führerschein | 0% [0–79] / 0% (0/1) [0–79] | 100% [21–100] / 0% (0/1) [0–79] | 100% [21–100] / 0% (0/1) [0–79] | 0% [0–79] / 0% (0/1) [0–79] | 0% [0–79] / 0% (0/1) [0–79] | 0% [0–79] / 0% (0/1) [0–79] |
| · buried: Rufbereitschaft | 0% [0–79] / 0% (0/1) [0–79] | 100% [21–100] / 0% (0/1) [0–79] | 0% [0–79] / 0% (0/1) [0–79] | 0% [0–79] / 0% (0/1) [0–79] | 0% [0–79] / 0% (0/1) [0–79] | 0% [0–79] / 0% (0/1) [0–79] |
| · buried: Schicht | 50% [9–91] / 0% (0/2) [0–66] | 100% [34–100] / 50% (1/2) [9–91] | 100% [34–100] / 50% (1/2) [9–91] | 50% [9–91] / 0% (0/2) [0–66] | 50% [9–91] / 0% (0/2) [0–66] | 50% [9–91] / 0% (0/2) [0–66] |
| · buried: Zertifikat | 50% [9–91] / 0% (0/2) [0–66] | 100% [34–100] / 50% (1/2) [9–91] | 100% [34–100] / 50% (1/2) [9–91] | 50% [9–91] / 0% (0/2) [0–66] | 50% [9–91] / 0% (0/2) [0–66] | 0% [0–66] / 0% (0/2) [0–66] |

## Near-misses let in

Profiles that fail exactly one must-have and look right otherwise, by the must-have they fail: share that reached the top 10. 30 of 145 were planted as look-alikes; the rest are background profiles that happen to fail exactly one must-have.

| Fails | `bm25` | `keyword` | `keyword+syn` | `field-filter-exact` | `field-filter` | `field-filter+syn` |
|---|---|---|---|---|---|---|
| Beruf | 0% (0/10) [0–28] | 0% (0/10) [0–28] | 0% (0/10) [0–28] | 0% (0/10) [0–28] | 0% (0/10) [0–28] | 0% (0/10) [0–28] |
| Erfahrung | 12% (2/17) [3–34] | 6% (1/17) [1–27] | 6% (1/17) [1–27] | 12% (2/17) [3–34] | 12% (2/17) [3–34] | 0% (0/17) [0–18] |
| Zertifikat | 0% (0/17) [0–18] | 12% (2/17) [3–34] | 6% (1/17) [1–27] | 0% (0/17) [0–18] | 0% (0/17) [0–18] | 6% (1/17) [1–27] |
| Führerschein | 0% (0/8) [0–32] | 12% (1/8) [2–47] | 25% (2/8) [7–59] | 0% (0/8) [0–32] | 0% (0/8) [0–32] | 0% (0/8) [0–32] |
| Entfernung | 12% (5/42) [5–25] | 0% (0/42) [0–8] | 0% (0/42) [0–8] | 10% (4/42) [4–22] | 7% (3/42) [2–19] | 0% (0/42) [0–8] |
| Schicht | 33% (3/9) [12–65] | 44% (4/9) [19–73] | 44% (4/9) [19–73] | 33% (3/9) [12–65] | 22% (2/9) [6–55] | 0% (0/9) [0–30] |
| Rufbereitschaft | 10% (4/42) [4–22] | 12% (5/42) [5–25] | 12% (5/42) [5–25] | 5% (2/42) [1–16] | 2% (1/42) [0–12] | 0% (0/42) [0–8] |

## Fits `bm25` left off the shortlist (31)

| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; misread must-haves) |
|---|---|---|---|---|---|
| eb-paderborn | p0307 | synonym:abbrev | Elektroniker BT | 11 | – |
| eb-paderborn | p0331 | buried:schicht | Elektroniker für Betriebstechnik | 12 | – |
| eb-paderborn | p0241 | synonym:variant | Elektroniker/-in für Betriebstechnik | 13 | – |
| eb-paderborn | p0282 | buried:zertifikate | Elektroniker/-in für Betriebstechnik | 14 | – |
| eb-paderborn | p0097 | plain | Elektroniker für Betriebstechnik | 19 | – |
| eb-paderborn | p0047 | buried:erfahrung | Elektroniker für Automatisierungstechnik | 28 | – |
| eb-paderborn | p0332 | synonym:predecessor | Energieelektroniker Fachrichtung Betriebstechnik | 42 | – |
| eb-paderborn | p0302 | plain | Mechatroniker | 57 | – |
| eb-paderborn | p0084 | buried:beruf | k. A. | 105 | – |
| cnc-guetersloh | p0390 | plain | Industriemechaniker | 16 | – |
| cnc-guetersloh | p0076 | buried:zertifikate | Industriemechaniker | 42 | – |
| cnc-guetersloh | p0061 | buried:schicht | Industriemechaniker/-in | 44 | – |
| cnc-guetersloh | p0030 | synonym:predecessor | Dreher | 81 | – |
| cnc-guetersloh | p0285 | synonym:abbrev | Industriemech. | 82 | – |
| cnc-guetersloh | p0244 | synonym:abbrev | Industriemech. | 83 | – |
| cnc-guetersloh | p0151 | buried:beruf | k. A. | 94 | – |
| service-bielefeld | p0237 | plain | Elektroniker, Fachrichtung Energie- und Gebäudetechnik | 17 | – |
| service-bielefeld | p0345 | plain | Elektroniker für Betriebstechnik | 36 | – |
| service-bielefeld | p0241 | synonym:variant | Elektroniker/-in für Betriebstechnik | 43 | – |
| service-bielefeld | p0097 | plain | Elektroniker für Betriebstechnik | 45 | – |
| … | 11 more in `run.json` | | | | |

## Fits `keyword` left off the shortlist (22)

| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; misread must-haves) |
|---|---|---|---|---|---|
| eb-paderborn | p0047 | buried:erfahrung | Elektroniker für Automatisierungstechnik | 11 | – |
| eb-paderborn | p0332 | synonym:predecessor | Energieelektroniker Fachrichtung Betriebstechnik | 13 | – |
| eb-paderborn | p0302 | plain | Mechatroniker | 15 | – |
| eb-paderborn | p0084 | buried:beruf | k. A. | 21 | – |
| cnc-guetersloh | p0076 | buried:zertifikate | Industriemechaniker | 11 | – |
| cnc-guetersloh | p0061 | buried:schicht | Industriemechaniker/-in | 12 | – |
| cnc-guetersloh | p0030 | synonym:predecessor | Dreher | 18 | – |
| cnc-guetersloh | p0285 | synonym:abbrev | Industriemech. | 19 | – |
| cnc-guetersloh | p0244 | synonym:abbrev | Industriemech. | 20 | – |
| cnc-guetersloh | p0151 | buried:beruf | k. A. | 23 | – |
| service-bielefeld | p0097 | plain | Elektroniker für Betriebstechnik | 11 | – |
| service-bielefeld | p0155 | buried:fuehrerschein | Elektroniker EGT | 14 | – |
| service-bielefeld | p0100 | buried:rufbereitschaft | Informationselektroniker/-in | 15 | – |
| service-bielefeld | p0131 | plain | Informationselektroniker | 18 | – |
| service-bielefeld | p0353 | buried:beruf | k. A. | 23 | – |
| service-bielefeld | p0352 | plain | Mechatroniker | 27 | – |
| service-bielefeld | p0370 | synonym:variant | Mechatroniker (IHK) | 32 | – |
| service-bielefeld | p0080 | synonym:variant | Mechatroniker/-in | 34 | – |
| service-bielefeld | p0051 | plain | Mechatroniker | 36 | – |
| service-bielefeld | p0012 | synonym:predecessor | Elektroinstallateur | 77 | – |
| … | 2 more in `run.json` | | | | |

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

## Fits `field-filter-exact` left off the shortlist (26)

| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; misread must-haves) |
|---|---|---|---|---|---|
| eb-paderborn | p0182 | synonym:predecessor | Energieelektroniker Fachrichtung Betriebstechnik | 6 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0307 | synonym:abbrev | Elektroniker BT | 13 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0331 | buried:schicht | Elektroniker für Betriebstechnik | 14 | Feld leer oder unpassend: schicht |
| eb-paderborn | p0241 | synonym:variant | Elektroniker/-in für Betriebstechnik | 15 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0282 | buried:zertifikate | Elektroniker/-in für Betriebstechnik | 16 | Feld leer oder unpassend: beruf, zertifikate |
| eb-paderborn | p0047 | buried:erfahrung | Elektroniker für Automatisierungstechnik | 29 | Feld leer oder unpassend: erfahrung |
| eb-paderborn | p0332 | synonym:predecessor | Energieelektroniker Fachrichtung Betriebstechnik | 43 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0084 | buried:beruf | k. A. | 105 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0035 | buried:erfahrung | Zerspanungsmechaniker/-in | 7 | Feld leer oder unpassend: beruf, erfahrung |
| cnc-guetersloh | p0287 | synonym:variant | Zerspanungsmechaniker/-in | 9 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0076 | buried:zertifikate | Industriemechaniker | 42 | Feld leer oder unpassend: zertifikate |
| cnc-guetersloh | p0061 | buried:schicht | Industriemechaniker/-in | 44 | Feld leer oder unpassend: beruf, schicht |
| cnc-guetersloh | p0030 | synonym:predecessor | Dreher | 81 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0285 | synonym:abbrev | Industriemech. | 82 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0244 | synonym:abbrev | Industriemech. | 83 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0151 | buried:beruf | k. A. | 94 | Feld leer oder unpassend: beruf |
| service-bielefeld | p0237 | plain | Elektroniker, Fachrichtung Energie- und Gebäudetechnik | 22 | Feld leer oder unpassend: beruf |
| service-bielefeld | p0241 | synonym:variant | Elektroniker/-in für Betriebstechnik | 47 | Feld leer oder unpassend: beruf |
| service-bielefeld | p0155 | buried:fuehrerschein | Elektroniker EGT | 64 | Feld leer oder unpassend: beruf, fuehrerschein |
| service-bielefeld | p0100 | buried:rufbereitschaft | Informationselektroniker/-in | 66 | Feld leer oder unpassend: beruf, rufbereitschaft |
| … | 6 more in `run.json` | | | | |

## Fits `field-filter` left off the shortlist (20)

| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; misread must-haves) |
|---|---|---|---|---|---|
| eb-paderborn | p0182 | synonym:predecessor | Energieelektroniker Fachrichtung Betriebstechnik | 7 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0307 | synonym:abbrev | Elektroniker BT | 14 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0331 | buried:schicht | Elektroniker für Betriebstechnik | 15 | Feld leer oder unpassend: schicht |
| eb-paderborn | p0282 | buried:zertifikate | Elektroniker/-in für Betriebstechnik | 16 | Feld leer oder unpassend: zertifikate |
| eb-paderborn | p0047 | buried:erfahrung | Elektroniker für Automatisierungstechnik | 29 | Feld leer oder unpassend: erfahrung |
| eb-paderborn | p0332 | synonym:predecessor | Energieelektroniker Fachrichtung Betriebstechnik | 43 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0084 | buried:beruf | k. A. | 105 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0035 | buried:erfahrung | Zerspanungsmechaniker/-in | 8 | Feld leer oder unpassend: erfahrung |
| cnc-guetersloh | p0076 | buried:zertifikate | Industriemechaniker | 42 | Feld leer oder unpassend: zertifikate |
| cnc-guetersloh | p0061 | buried:schicht | Industriemechaniker/-in | 44 | Feld leer oder unpassend: schicht |
| cnc-guetersloh | p0030 | synonym:predecessor | Dreher | 81 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0285 | synonym:abbrev | Industriemech. | 82 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0244 | synonym:abbrev | Industriemech. | 83 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0151 | buried:beruf | k. A. | 94 | Feld leer oder unpassend: beruf |
| service-bielefeld | p0155 | buried:fuehrerschein | Elektroniker EGT | 66 | Feld leer oder unpassend: beruf, fuehrerschein |
| service-bielefeld | p0100 | buried:rufbereitschaft | Informationselektroniker/-in | 68 | Feld leer oder unpassend: rufbereitschaft |
| service-bielefeld | p0353 | buried:beruf | k. A. | 84 | Feld leer oder unpassend: beruf |
| service-bielefeld | p0012 | synonym:predecessor | Elektroinstallateur | 248 | Feld leer oder unpassend: beruf |
| service-bielefeld | p0034 | synonym:predecessor | Elektroinstallateur | 296 | Feld leer oder unpassend: beruf |
| service-bielefeld | p0104 | buried:erfahrung | Radio- und Fernsehtechniker | 298 | Feld leer oder unpassend: beruf, erfahrung |

## Fits `field-filter+syn` left off the shortlist (12)

| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; misread must-haves) |
|---|---|---|---|---|---|
| eb-paderborn | p0331 | buried:schicht | Elektroniker für Betriebstechnik | 9 | Feld leer oder unpassend: schicht |
| eb-paderborn | p0282 | buried:zertifikate | Elektroniker/-in für Betriebstechnik | 26 | Feld leer oder unpassend: zertifikate |
| eb-paderborn | p0047 | buried:erfahrung | Elektroniker für Automatisierungstechnik | 45 | Feld leer oder unpassend: erfahrung |
| eb-paderborn | p0084 | buried:beruf | k. A. | 64 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0035 | buried:erfahrung | Zerspanungsmechaniker/-in | 15 | Feld leer oder unpassend: erfahrung |
| cnc-guetersloh | p0151 | buried:beruf | k. A. | 38 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0076 | buried:zertifikate | Industriemechaniker | 78 | Feld leer oder unpassend: zertifikate |
| cnc-guetersloh | p0061 | buried:schicht | Industriemechaniker/-in | 81 | Feld leer oder unpassend: schicht |
| service-bielefeld | p0104 | buried:erfahrung | Radio- und Fernsehtechniker | 39 | Feld leer oder unpassend: erfahrung |
| service-bielefeld | p0155 | buried:fuehrerschein | Elektroniker EGT | 53 | Feld leer oder unpassend: fuehrerschein |
| service-bielefeld | p0100 | buried:rufbereitschaft | Informationselektroniker/-in | 111 | Feld leer oder unpassend: rufbereitschaft |
| service-bielefeld | p0353 | buried:beruf | k. A. | 132 | Feld leer oder unpassend: beruf |

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

Lost a top-10 place, by origin: every base/swap pair tests both origins involved and counts against the side left out while the other got in. Without a name effect every origin sits near the repeat rate.

| Origin | `bm25` | `keyword` | `keyword+syn` | `field-filter-exact` | `field-filter` | `field-filter+syn` |
|---|---|---|---|---|---|---|
| ar | 0% (0/83) [0–4] | 0% (0/82) [0–4] | 0% (0/86) [0–4] | 0% (0/85) [0–4] | 0% (0/85) [0–4] | 0% (0/83) [0–4] |
| de | 0% (0/175) [0–2] | 0% (0/191) [0–2] | 0% (0/188) [0–2] | 0% (0/172) [0–2] | 0% (0/172) [0–2] | 0% (0/167) [0–2] |
| pl | 0% (0/103) [0–4] | 0% (0/105) [0–4] | 0% (0/101) [0–4] | 0% (0/100) [0–4] | 0% (0/102) [0–4] | 0% (0/98) [0–4] |
| tr | 0% (0/126) [0–3] | 0% (0/113) [0–3] | 0% (0/122) [0–3] | 0% (0/129) [0–3] | 0% (0/129) [0–3] | 0% (0/133) [0–3] |
| ua | 0% (0/113) [0–3] | 0% (0/109) [0–3] | 0% (0/103) [0–4] | 0% (0/114) [0–3] | 0% (0/112) [0–3] | 0% (0/119) [0–3] |

## How this was measured

Every profile is synthetic: hidden facts (trade, years, certificates, licence, town, shift and on-call willingness) and a presentation of those facts as an ATS record, with some fields left empty and the fact stated only in messy recruiter notes, and the trade shown by its official name or an old name, synonym or abbreviation. The true fits of each vacancy follow from its must-have rules applied to the hidden facts. Planted per vacancy: 4 plain, 4 synonym and 4 buried fits, and 2 near-misses per must-have; background profiles that would fit are redrawn. A profile planted for one vacancy (as fit or near-miss) can be a true fit for another and is counted there too. Certificate lists are complete: a certificate not named is absent. Distances are computed and shown to the model, so its Entfernung judgements are not a reading test. No real candidate data is involved.
