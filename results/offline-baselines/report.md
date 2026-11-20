# poolgate report

Pool: 400 synthetic profiles, seed 7, 3 vacancies. Matchers: `bm25`, `keyword`, `field-filter`.

| Vacancy | True fits | of which plain / synonym / buried | Near-misses |
|---|---|---|---|
| Elektroniker für Betriebstechnik (m/w/d) Instandhaltung (Paderborn, 35 km) | 13 | 5 / 4 / 4 | 31 |
| CNC-Fräser / Zerspanungsmechaniker (m/w/d) (Gütersloh, 30 km) | 12 | 4 / 4 / 4 | 28 |
| Servicetechniker Sicherheitstechnik (m/w/d) im Außendienst OWL (Bielefeld, 50 km) | 14 | 5 / 5 / 4 | 89 |

## Headline

Brackets are 95% Wilson intervals. The shortlist is the matcher's own yes-list where it gives one, else its top 10.

| Measure | `bm25` | `keyword` | `field-filter` |
|---|---|---|---|
| Recall@10 (ceiling 77%: more fits than places) | 21% (8/39) [11–36] | 38% (15/39) [25–54] | 38% (15/39) [25–54] |
| Recall@20 | 38% (15/39) [25–54] | 74% (29/39) [59–85] | 54% (21/39) [39–68] |
| Precision@10 | 27% (8/30) [14–44] | 50% (15/30) [33–67] | 50% (15/30) [33–67] |
| Shortlist precision | 27% (8/30) [14–44] | 50% (15/30) [33–67] | 100% (14/14) [78–100] |
| Shortlist recall | 21% (8/39) [11–36] | 38% (15/39) [25–54] | 36% (14/39) [23–52] |
| Shortlist size (all vacancies) | 30 (top 10) | 30 (top 10) | 14 |
| Near-misses in top 10 | 11% (17/148) [7–18] | 10% (15/148) [6–16] | 8% (12/148) [5–14] |
| Near-misses in shortlist | 17 | 15 | 0 |

## Which fits are found

Recall@20 and shortlist recall by how the fit is presented.

| Case | `bm25` @20 / shortlist | `keyword` @20 / shortlist | `field-filter` @20 / shortlist |
|---|---|---|---|
| plain (official title, facts in fields) | 57% [33–79] / 36% (5/14) [16–61] | 71% [45–88] / 50% (7/14) [27–73] | 100% [78–100] / 100% (14/14) [78–100] |
| synonym (title is an old name, abbreviation or synonym) | 15% [4–42] / 8% (1/13) [1–33] | 69% [42–87] / 23% (3/13) [8–50] | 15% [4–42] / 0% (0/13) [0–23] |
| buried (a must-have fact only in the notes) | 42% [19–68] / 17% (2/12) [5–45] | 83% [55–95] / 42% (5/12) [19–68] | 42% [19–68] / 0% (0/12) [0–24] |
| · buried: Beruf | 33% [6–79] / 0% (0/3) [0–56] | 67% [21–94] / 33% (1/3) [6–79] | 33% [6–79] / 0% (0/3) [0–56] |
| · buried: Erfahrung | 0% [0–56] / 0% (0/3) [0–56] | 67% [21–94] / 0% (0/3) [0–56] | 0% [0–56] / 0% (0/3) [0–56] |
| · buried: Führerschein | 100% [21–100] / 100% (1/1) [21–100] | 100% [21–100] / 100% (1/1) [21–100] | 100% [21–100] / 0% (0/1) [0–79] |
| · buried: Rufbereitschaft | 0% [0–79] / 0% (0/1) [0–79] | 100% [21–100] / 0% (0/1) [0–79] | 0% [0–79] / 0% (0/1) [0–79] |
| · buried: Schicht | 50% [9–91] / 0% (0/2) [0–66] | 100% [34–100] / 50% (1/2) [9–91] | 50% [9–91] / 0% (0/2) [0–66] |
| · buried: Zertifikat | 100% [34–100] / 50% (1/2) [9–91] | 100% [34–100] / 100% (2/2) [34–100] | 100% [34–100] / 0% (0/2) [0–66] |

## Near-misses let in

Profiles that fail exactly one must-have and look right otherwise, by the must-have they fail: share that reached the top 10. 30 of 148 were planted as look-alikes; the rest are background profiles that happen to fail exactly one must-have.

| Fails | `bm25` | `keyword` | `field-filter` |
|---|---|---|---|
| Beruf | 0% (0/19) [0–17] | 0% (0/19) [0–17] | 0% (0/19) [0–17] |
| Erfahrung | 14% (2/14) [4–40] | 14% (2/14) [4–40] | 7% (1/14) [1–31] |
| Zertifikat | 18% (3/17) [6–41] | 12% (2/17) [3–34] | 18% (3/17) [6–41] |
| Führerschein | 11% (1/9) [2–44] | 22% (2/9) [6–55] | 0% (0/9) [0–30] |
| Entfernung | 11% (3/28) [4–27] | 0% (0/28) [0–12] | 7% (2/28) [2–23] |
| Schicht | 29% (4/14) [12–55] | 29% (4/14) [12–55] | 21% (3/14) [8–48] |
| Rufbereitschaft | 9% (4/47) [3–20] | 11% (5/47) [5–23] | 6% (3/47) [2–17] |

## Fits `bm25` left off the shortlist (31)

| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; misread must-haves) |
|---|---|---|---|---|---|
| eb-paderborn | p0307 | synonym | Elektroniker/-in für Betriebstechnik | 11 | – |
| eb-paderborn | p0302 | plain | Elektroniker für Betriebstechnik | 12 | – |
| eb-paderborn | p0374 | plain | Elektroniker für Automatisierungstechnik | 14 | – |
| eb-paderborn | p0182 | synonym | Elektroniker/-in für Automatisierungstechnik | 21 | – |
| eb-paderborn | p0097 | plain | Elektroniker für Betriebstechnik | 23 | – |
| eb-paderborn | p0241 | synonym | Elektroniker/-in für Betriebstechnik | 25 | – |
| eb-paderborn | p0084 | buried:beruf | k. A. | 26 | – |
| eb-paderborn | p0047 | buried:erfahrung | Elektroniker für Automatisierungstechnik | 32 | – |
| eb-paderborn | p0331 | buried:schicht | Mechatroniker | 73 | – |
| eb-paderborn | p0051 | plain | Mechatroniker | 100 | – |
| cnc-guetersloh | p0061 | buried:schicht | Zerspanungsmechaniker | 11 | – |
| cnc-guetersloh | p0076 | buried:zertifikate | Zerspanungsmechaniker | 12 | – |
| cnc-guetersloh | p0151 | buried:beruf | k. A. | 17 | – |
| cnc-guetersloh | p0390 | plain | Zerspanungsmechaniker | 20 | – |
| cnc-guetersloh | p0035 | buried:erfahrung | Industriemechaniker | 28 | – |
| cnc-guetersloh | p0287 | synonym | Industriemechaniker/-in | 34 | – |
| cnc-guetersloh | p0244 | synonym | Industriemech. | 70 | – |
| cnc-guetersloh | p0285 | synonym | Zerspanungsmech. | 85 | – |
| cnc-guetersloh | p0030 | synonym | Industriemech. | 91 | – |
| service-bielefeld | p0307 | synonym | Elektroniker/-in für Betriebstechnik | 36 | – |
| … | 11 more in `run.json` | | | | |

## Fits `keyword` left off the shortlist (24)

| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; misread must-haves) |
|---|---|---|---|---|---|
| eb-paderborn | p0182 | synonym | Elektroniker/-in für Automatisierungstechnik | 11 | – |
| eb-paderborn | p0097 | plain | Elektroniker für Betriebstechnik | 12 | – |
| eb-paderborn | p0241 | synonym | Elektroniker/-in für Betriebstechnik | 13 | – |
| eb-paderborn | p0084 | buried:beruf | k. A. | 14 | – |
| eb-paderborn | p0047 | buried:erfahrung | Elektroniker für Automatisierungstechnik | 15 | – |
| eb-paderborn | p0331 | buried:schicht | Mechatroniker | 20 | – |
| eb-paderborn | p0051 | plain | Mechatroniker | 25 | – |
| cnc-guetersloh | p0390 | plain | Zerspanungsmechaniker | 11 | – |
| cnc-guetersloh | p0035 | buried:erfahrung | Industriemechaniker | 13 | – |
| cnc-guetersloh | p0287 | synonym | Industriemechaniker/-in | 15 | – |
| cnc-guetersloh | p0244 | synonym | Industriemech. | 19 | – |
| cnc-guetersloh | p0285 | synonym | Zerspanungsmech. | 20 | – |
| cnc-guetersloh | p0030 | synonym | Industriemech. | 23 | – |
| service-bielefeld | p0352 | plain | Informationselektroniker | 15 | – |
| service-bielefeld | p0100 | buried:rufbereitschaft | Informationselektroniker | 16 | – |
| service-bielefeld | p0080 | synonym | Elektroniker BT | 19 | – |
| service-bielefeld | p0034 | synonym | Informationselektroniker Schwerpunkt Geräte- und Systemtechnik | 22 | – |
| service-bielefeld | p0353 | buried:beruf | k. A. | 30 | – |
| service-bielefeld | p0104 | buried:erfahrung | Elektroniker EGT | 31 | – |
| service-bielefeld | p0045 | plain | Mechatroniker | 35 | – |
| … | 4 more in `run.json` | | | | |

## Fits `field-filter` left off the shortlist (25)

| Vacancy | Profile | Case | Beruf field | Rank | Why (matcher's words; misread must-haves) |
|---|---|---|---|---|---|
| eb-paderborn | p0282 | buried:zertifikate | Elektroniker/-in für Betriebstechnik | 9 | Feld leer oder unpassend: beruf, zertifikate |
| eb-paderborn | p0332 | synonym | Energieelektroniker Fachrichtung Betriebstechnik (bis 2003) | 11 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0307 | synonym | Elektroniker/-in für Betriebstechnik | 15 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0182 | synonym | Elektroniker/-in für Automatisierungstechnik | 23 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0241 | synonym | Elektroniker/-in für Betriebstechnik | 26 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0084 | buried:beruf | k. A. | 27 | Feld leer oder unpassend: beruf |
| eb-paderborn | p0047 | buried:erfahrung | Elektroniker für Automatisierungstechnik | 33 | Feld leer oder unpassend: erfahrung |
| eb-paderborn | p0331 | buried:schicht | Mechatroniker | 74 | Feld leer oder unpassend: schicht |
| cnc-guetersloh | p0061 | buried:schicht | Zerspanungsmechaniker | 12 | Feld leer oder unpassend: schicht |
| cnc-guetersloh | p0076 | buried:zertifikate | Zerspanungsmechaniker | 13 | Feld leer oder unpassend: zertifikate |
| cnc-guetersloh | p0151 | buried:beruf | k. A. | 18 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0035 | buried:erfahrung | Industriemechaniker | 28 | Feld leer oder unpassend: erfahrung |
| cnc-guetersloh | p0287 | synonym | Industriemechaniker/-in | 34 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0244 | synonym | Industriemech. | 70 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0285 | synonym | Zerspanungsmech. | 85 | Feld leer oder unpassend: beruf |
| cnc-guetersloh | p0030 | synonym | Industriemech. | 91 | Feld leer oder unpassend: beruf |
| service-bielefeld | p0155 | buried:fuehrerschein | Elektroniker für Energie- und Gebäudetechnik | 13 | Feld leer oder unpassend: fuehrerschein |
| service-bielefeld | p0307 | synonym | Elektroniker/-in für Betriebstechnik | 40 | Feld leer oder unpassend: beruf |
| service-bielefeld | p0100 | buried:rufbereitschaft | Informationselektroniker | 70 | Feld leer oder unpassend: rufbereitschaft |
| service-bielefeld | p0080 | synonym | Elektroniker BT | 85 | Feld leer oder unpassend: beruf |
| … | 5 more in `run.json` | | | | |

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
| ar | 0% (0/103) [0–4] | 0% (0/88) [0–4] | 0% (0/104) [0–4] |
| de | 0% (0/174) [0–2] | 0% (0/198) [0–2] | 0% (0/176) [0–2] |
| pl | 0% (0/107) [0–3] | 0% (0/101) [0–4] | 0% (0/103) [0–4] |
| tr | 0% (0/115) [0–3] | 0% (0/108) [0–3] | 0% (0/115) [0–3] |
| ua | 0% (0/101) [0–4] | 0% (0/105) [0–4] | 0% (0/102) [0–4] |

## How this was measured

Every profile is synthetic: hidden facts (trade, years, certificates, licence, town, shift and on-call willingness) and a presentation of those facts as an ATS record, with some fields left empty and the fact stated only in messy recruiter notes, and the trade shown by its official name or an old name, synonym or abbreviation. The true fits of each vacancy follow from its must-have rules applied to the hidden facts. Planted per vacancy: 4 plain, 4 synonym and 4 buried fits, and 2 near-misses per must-have; background profiles that would fit are redrawn. A profile planted for one vacancy (as fit or near-miss) can be a true fit for another and is counted there too. Certificate lists are complete: a certificate not named is absent. Distances are computed and shown to the model, so its Entfernung judgements are not a reading test. No real candidate data is involved.
