"""A synthetic talent pool with known fits, and the vacancies matched against it.

Every profile is a set of hidden facts (what is true about the candidate) plus
a presentation: how those facts appear in the record a matcher sees. A fact can
sit in a structured field, or only in the free-text notes ("k. A." in the
field), and the trade can be shown by its official name or by a synonym, an
old name or an abbreviation. The ground truth for every vacancy is computed
from the hidden facts by the vacancy's explicit must-have rules, never from
the text, so a matcher is graded on what is true, not on what is easy to read.

Facts, identities, presentation and notes come from separate random streams,
so swapping a candidate's name leaves every fact and every word of the notes
other than the name untouched.
"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass, field, replace
from datetime import date

from . import geo

TODAY = date(2026, 11, 15)  # the pool's "Stand"; years in the notes count from here

# Canonical trade -> synonyms, old names and abbreviations that mean the same
# qualification. Every synonym maps to exactly one trade, so the truth stays
# recoverable from the text; ambiguous words ("Elektriker") are not used.
TRADES: dict[str, tuple[str, ...]] = {
    "Elektroniker für Betriebstechnik": (
        "Elektroniker BT", "E-Techniker Betriebstechnik", "Betriebselektroniker",
        "Energieelektroniker Betriebstechnik", "Elektroniker FR Betriebstechnik"),
    "Elektroniker für Automatisierungstechnik": (
        "Automatisierungselektroniker", "Elektroniker AT", "Prozessleitelektroniker",
        "E-Techniker Automatisierung"),
    "Elektroniker für Energie- und Gebäudetechnik": (
        "Elektroniker EGT", "Elektroinstallateur", "Elektroniker E+G", "Gebäudeelektroniker"),
    "Informationselektroniker": (
        "Infoelektroniker", "Radio- und Fernsehtechniker",
        "Informationselektroniker Geräte- und Systemtechnik"),
    "Mechatroniker": ("Mechatr.", "Mechatroniker/in IHK", "Servicetechniker Mechatronik"),
    "Industriemechaniker": (
        "Indu-Mech", "Industriemech.", "Betriebsschlosser", "Maschinenschlosser"),
    "Zerspanungsmechaniker": (
        "CNC-Fräser", "Zerspaner", "Zerspanungsmech. FR Frästechnik", "CNC-Dreher/Fräser",
        "Dreher"),
    # Lookalikes: they read like the right trade and are not.
    "Industrieelektriker": ("Industrieelektriker Betriebstechnik", "Elektro-Facharbeiter (2 J.)"),
    "Maschinen- und Anlagenführer": ("CNC-Maschinenbediener", "MAF", "Anlagenführer"),
    "Kfz-Mechatroniker": ("KFZ-Mechaniker", "Kfz-Mech.", "Kfz-Mechatroniker PKW"),
    # Background trades.
    "Konstruktionsmechaniker": ("Metallbauer Konstruktionstechnik", "Konstruktionsmech."),
    "Fachkraft für Lagerlogistik": ("Fachlagerist", "Lagerlogistiker"),
    "Anlagenmechaniker SHK": ("Heizungsbauer", "Anlagenmech. SHK", "Gas-Wasser-Installateur"),
    "Werkzeugmechaniker": ("Werkzeugmacher", "Formenbauer"),
    "Verfahrensmechaniker Kunststoff": ("Kunststoff-Verfahrensmechaniker", "Einrichter Spritzguss"),
}

# Certificates and skills, with the ways notes and CVs spell them.
CERTS: dict[str, tuple[str, ...]] = {
    "SPS S7": ("Simatic S7", "Step 7", "S7-1500", "SPS-Programmierung Siemens"),
    "TIA Portal": ("TIA", "TIA-Portal V17"),
    "Heidenhain": ("Heidenhain TNC 640", "TNC 530", "Heidenhain-Klartext"),
    "Sinumerik 840D": ("Siemens 840D", "Sinumerik", "ShopMill"),
    "DIN 14675": ("BMA nach DIN 14675", "Brandmelde-Sachkunde"),
    "VdS EMA": ("VdS-Schulung EMA", "Einbruchmeldetechnik VdS"),
    "KNX": ("KNX-Grundkurs", "KNX Partner"),
    "Schweißschein": ("MAG-Schweißschein", "Schweißpass"),
    "Staplerschein": ("Flurförderzeugschein", "Gabelstaplerschein"),
    "Hubarbeitsbühne": ("Bühnenschein", "PAL-Card"),
    "Elektrofachkraft": ("EFK", "Elektrofachkraft (EFK)"),
}

_ELECTRICAL = ("SPS S7", "TIA Portal", "KNX", "Elektrofachkraft", "DIN 14675", "VdS EMA",
               "Hubarbeitsbühne")
_METAL = ("Heidenhain", "Sinumerik 840D", "Schweißschein", "Staplerschein")
CERT_POOL = {
    "Elektroniker für Betriebstechnik": _ELECTRICAL,
    "Elektroniker für Automatisierungstechnik": _ELECTRICAL,
    "Elektroniker für Energie- und Gebäudetechnik": _ELECTRICAL,
    "Informationselektroniker": ("DIN 14675", "VdS EMA", "KNX", "Elektrofachkraft"),
    "Industrieelektriker": _ELECTRICAL,
    "Mechatroniker": ("SPS S7", "TIA Portal", "Staplerschein", "Schweißschein",
                      "Hubarbeitsbühne", "Heidenhain"),
    "Industriemechaniker": _METAL + ("Hubarbeitsbühne",),
    "Zerspanungsmechaniker": _METAL,
    "Maschinen- und Anlagenführer": _METAL,
    "Werkzeugmechaniker": _METAL,
}
DEFAULT_CERTS = ("Staplerschein", "Schweißschein", "Hubarbeitsbühne")

SHIFTS = ("3", "2", "tag")  # most to least: 3-Schicht incl. Nacht, 2-Schicht, nur Tag
SHIFT_LABEL = {"3": "3-Schicht", "2": "2-Schicht", "tag": "nur Tagschicht"}

# The must-have checks, in the order they are reported.
MUSTS = ("beruf", "erfahrung", "zertifikate", "fuehrerschein", "entfernung", "schicht",
         "rufbereitschaft")
MUST_LABEL = {
    "beruf": "Beruf", "erfahrung": "Erfahrung", "zertifikate": "Zertifikat",
    "fuehrerschein": "Führerschein", "entfernung": "Entfernung", "schicht": "Schicht",
    "rufbereitschaft": "Rufbereitschaft",
}
# Which fact a must-have reads; "buried" means that fact's field is k. A.
MUST_FACT = {
    "beruf": "trade", "erfahrung": "years", "zertifikate": "certs",
    "fuehrerschein": "licence", "entfernung": "town", "schicht": "shift",
    "rufbereitschaft": "on_call",
}
HIDEABLE = ("trade", "years", "certs", "licence", "shift", "on_call")


@dataclass(frozen=True)
class Vacancy:
    key: str
    title: str
    company: str
    site: str  # town in geo.TOWNS
    radius_km: int
    trades: tuple[str, ...]  # accepted qualifications
    lookalikes: tuple[str, ...]  # trades that read as right and are not
    min_years: int
    certs_any: tuple[str, ...] = ()  # at least one of these; () = no requirement
    licence: bool = False
    shift: str | None = None  # "3" or "2": the shift model the job runs
    on_call: bool = False
    nice: tuple[str, ...] = ()

    def musts(self) -> tuple[str, ...]:
        out = ["beruf", "erfahrung"]
        if self.certs_any:
            out.append("zertifikate")
        if self.licence:
            out.append("fuehrerschein")
        out.append("entfernung")
        if self.shift:
            out.append("schicht")
        if self.on_call:
            out.append("rufbereitschaft")
        return tuple(out)

    def must_text(self) -> list[str]:
        lines = [
            "abgeschlossene Berufsausbildung als " + " oder ".join(self.trades)
            + " (auch unter einem Vorgängernamen des Berufs)",
            f"mindestens {self.min_years} Jahre Berufserfahrung nach der Ausbildung",
        ]
        if self.certs_any:
            lines.append("Kenntnisse/Nachweis: " + " oder ".join(self.certs_any))
        if self.licence:
            lines.append("Führerschein Klasse B")
        lines.append(f"Wohnort höchstens {self.radius_km} km Luftlinie von {self.site}")
        if self.shift == "3":
            lines.append("Bereitschaft zu 3-Schicht inklusive Nachtschicht")
        elif self.shift == "2":
            lines.append("Bereitschaft zu 2-Schicht (Früh/Spät)")
        if self.on_call:
            lines.append("Bereitschaft zu Rufbereitschaft")
        return lines

    def posting(self) -> str:
        return (f"{self.title}\n{self.company}, Einsatzort {self.site}\n\nMuss-Kriterien:\n"
                + "\n".join(f"- {m}" for m in self.must_text())
                + ("\n\nWünschenswert:\n" + "\n".join(f"- {n}" for n in self.nice)
                   if self.nice else ""))

    def public(self) -> dict:
        return {
            "key": self.key, "title": self.title, "company": self.company, "site": self.site,
            "site_plz": geo.plz(self.site), "radius_km": self.radius_km,
            "trades": list(self.trades), "min_years": self.min_years,
            "certs_any": list(self.certs_any), "licence": self.licence, "shift": self.shift,
            "on_call": self.on_call, "musts": list(self.musts()),
            "must_text": dict(zip(self.musts(), self.must_text())), "nice": list(self.nice),
            "posting": self.posting(),
        }


VACANCIES = (
    Vacancy(
        key="eb-paderborn",
        title="Elektroniker für Betriebstechnik (m/w/d) Instandhaltung",
        company="Kunststoffverarbeiter, ca. 220 Mitarbeitende",
        site="Paderborn", radius_km=35,
        trades=("Elektroniker für Betriebstechnik", "Elektroniker für Automatisierungstechnik",
                "Mechatroniker"),
        lookalikes=("Industrieelektriker",),
        min_years=2, certs_any=("SPS S7", "TIA Portal"), shift="3",
        nice=("Elektrofachkraft-Verantwortung", "Erfahrung an Spritzgussmaschinen"),
    ),
    Vacancy(
        key="cnc-guetersloh",
        title="CNC-Fräser / Zerspanungsmechaniker (m/w/d)",
        company="Maschinenbau-Zulieferer, ca. 90 Mitarbeitende",
        site="Gütersloh", radius_km=30,
        trades=("Zerspanungsmechaniker", "Industriemechaniker"),
        lookalikes=("Maschinen- und Anlagenführer",),
        min_years=3, certs_any=("Heidenhain",), shift="2",
        nice=("5-Achs-Fräsen", "Messen mit Zeiss-KMG"),
    ),
    Vacancy(
        key="service-bielefeld",
        title="Servicetechniker Sicherheitstechnik (m/w/d) im Außendienst OWL",
        company="Errichter für Brandmelde- und Einbruchmeldetechnik, ca. 40 Mitarbeitende",
        site="Bielefeld", radius_km=50,
        trades=("Elektroniker für Energie- und Gebäudetechnik", "Informationselektroniker",
                "Elektroniker für Betriebstechnik", "Mechatroniker"),
        lookalikes=("Kfz-Mechatroniker",),
        min_years=2, licence=True, on_call=True,
        nice=("DIN 14675", "VdS EMA"),
    ),
)
VACANCY_BY_KEY = {v.key: v for v in VACANCIES}


@dataclass(frozen=True)
class Facts:
    trade: str
    years: int
    certs: frozenset[str]
    licence: bool
    town: str
    shift: str
    on_call: bool
    salary_eur: int
    available: str
    last_contact: date


@dataclass(frozen=True)
class Identity:
    name: str  # exactly "First Last", one token each, so a swap keeps text length
    gender: str  # "f" | "m"
    origin: str

    @property
    def last(self) -> str:
        return self.name.split()[-1]

    def label(self) -> str:
        return f"{self.name} ({self.gender}, {self.origin})"


@dataclass(frozen=True)
class Presentation:
    title: str  # "canonical" | "synonym" | "none"
    title_text: str  # what the Beruf field shows ("" when none)
    term: str  # how the notes name the trade
    hidden: frozenset[str] = field(default_factory=frozenset)  # facts shown only in notes
    style: str = "stichpunkte"


@dataclass(frozen=True)
class Profile:
    id: str
    identity: Identity
    facts: Facts
    pres: Presentation
    notes: str
    planted: str | None = None  # e.g. "fit:cnc-guetersloh:synonym", for the record only

    def public(self) -> dict:
        """What a matcher sees: the ATS record, never the hidden facts."""
        f, h = self.facts, self.pres.hidden
        return {
            "id": self.id,
            "name": self.identity.name,
            "beruf": self.pres.title_text or None,
            "plz": geo.plz(f.town),
            "ort": f.town,
            "erfahrung_jahre": None if "years" in h else f.years,
            "zertifikate": None if "certs" in h else sorted(f.certs),
            "fuehrerschein": None if "licence" in h else ("B" if f.licence else "keiner"),
            "schicht": None if "shift" in h else SHIFT_LABEL[f.shift],
            "rufbereitschaft": None if "on_call" in h else ("ja" if f.on_call else "nein"),
            "gehaltswunsch_eur": f.salary_eur,
            "verfuegbar": f.available,
            "letzter_kontakt": f.last_contact.isoformat(),
            "notizen": self.notes,
        }


# ---------------------------------------------------------------- the rules

def check(v: Vacancy, f: Facts) -> dict[str, bool]:
    """Each of the vacancy's must-haves, met or not. This is the ground truth."""
    out = {}
    for m in v.musts():
        if m == "beruf":
            out[m] = f.trade in v.trades
        elif m == "erfahrung":
            out[m] = f.years >= v.min_years
        elif m == "zertifikate":
            out[m] = bool(f.certs & set(v.certs_any))
        elif m == "fuehrerschein":
            out[m] = f.licence
        elif m == "entfernung":
            out[m] = geo.km(f.town, v.site) <= v.radius_km
        elif m == "schicht":
            out[m] = SHIFTS.index(f.shift) <= SHIFTS.index(v.shift)
        elif m == "rufbereitschaft":
            out[m] = f.on_call
    return out


def is_fit(v: Vacancy, f: Facts) -> bool:
    return all(check(v, f).values())


def near_miss(v: Vacancy, f: Facts) -> str | None:
    """The one failed must-have of a profile that looks right, else None.

    A near-miss fails exactly one must-have. When that one is the trade, it
    only counts if the trade is one of the vacancy's lookalikes; a baker who
    meets everything else is not a near-miss for an electrician job.
    """
    failed = [m for m, ok in check(v, f).items() if not ok]
    if len(failed) != 1:
        return None
    if failed[0] == "beruf" and f.trade not in v.lookalikes:
        return None
    return failed[0]


def case_type(v: Vacancy, p: Profile) -> str:
    """How hard a true fit is to see: plain, synonym, or buried:<must>.

    buried wins over synonym: a fit whose must-have fact is only in the notes
    is missed by any field filter, whatever its title says.
    """
    for m in v.musts():
        fact = MUST_FACT[m]
        if fact in p.pres.hidden:
            return f"buried:{m}"
    return "synonym" if p.pres.title != "canonical" else "plain"


def case_family(case: str) -> str:
    return case.split(":")[0]


# ---------------------------------------------------------------- identities

FIRST = {
    "de": {"m": ["Lukas", "Jonas", "Stefan", "Thomas", "Michael", "Daniel", "Sven", "Marco"],
           "f": ["Anna", "Julia", "Katrin", "Sabrina", "Lisa", "Jana", "Nina", "Carina"]},
    "tr": {"m": ["Mehmet", "Emre", "Murat", "Burak", "Can", "Serkan", "Hakan", "Ali"],
           "f": ["Ayşe", "Elif", "Zeynep", "Merve", "Esra", "Derya", "Selin", "Büşra"]},
    "pl": {"m": ["Piotr", "Tomasz", "Marek", "Krzysztof", "Paweł", "Łukasz", "Michał", "Adam"],
           "f": ["Katarzyna", "Agnieszka", "Magdalena", "Joanna", "Monika", "Ewa", "Natalia",
                 "Justyna"]},
    "ar": {"m": ["Ahmed", "Omar", "Karim", "Youssef", "Mahmoud", "Hassan", "Samir", "Tarek"],
           "f": ["Fatima", "Leila", "Nour", "Rania", "Amira", "Salma", "Yasmin", "Dina"]},
    "ua": {"m": ["Andrii", "Dmytro", "Serhii", "Oleksandr", "Vitalii", "Taras", "Bohdan",
                 "Mykola"],
           "f": ["Olena", "Iryna", "Oksana", "Tetiana", "Yuliia", "Kateryna", "Svitlana",
                 "Larysa"]},
}
LAST = {
    "de": ["Becker", "Schmidt", "Fischer", "Wagner", "Hoffmann", "Meier", "Kröger", "Brinkmann"],
    "tr": ["Yılmaz", "Demir", "Kaya", "Çelik", "Şahin", "Öztürk", "Arslan", "Doğan"],
    "pl": ["Nowak", "Wójcik", "Kowalczyk", "Mazur", "Krawczyk", "Zając", "Król", "Wieczorek"],
    "ar": ["Haddad", "Mansour", "Khalil", "Nasser", "Saleh", "Hamdan", "Darwish", "Aziz"],
    "ua": ["Kovalenko", "Shevchenko", "Bondarenko", "Tkachenko", "Kravchenko", "Melnyk", "Boiko",
           "Lysenko"],
}
ORIGINS = tuple(FIRST)
ORIGIN_WEIGHTS = (0.5, 0.125, 0.125, 0.125, 0.125)


def random_identity(rng: random.Random, origin: str | None = None,
                    gender: str | None = None) -> Identity:
    origin = origin or rng.choices(ORIGINS, ORIGIN_WEIGHTS)[0]
    gender = gender or ("f" if rng.random() < 0.12 else "m")
    return Identity(f"{rng.choice(FIRST[origin][gender])} {rng.choice(LAST[origin])}",
                    gender, origin)


def origin_of(name: str) -> str | None:
    first, last = name.split()
    for o in ORIGINS:
        if last in LAST[o]:
            return o
    for o in ORIGINS:
        if any(first in FIRST[o][g] for g in ("m", "f")):
            return o
    return None


# ---------------------------------------------------------------- facts

_TRADE_WEIGHTS = {
    "Elektroniker für Betriebstechnik": 10, "Elektroniker für Automatisierungstechnik": 4,
    "Elektroniker für Energie- und Gebäudetechnik": 8, "Informationselektroniker": 3,
    "Mechatroniker": 9, "Industriemechaniker": 10, "Zerspanungsmechaniker": 7,
    "Industrieelektriker": 3, "Maschinen- und Anlagenführer": 5, "Kfz-Mechatroniker": 5,
    "Konstruktionsmechaniker": 4, "Fachkraft für Lagerlogistik": 5, "Anlagenmechaniker SHK": 4,
    "Werkzeugmechaniker": 3, "Verfahrensmechaniker Kunststoff": 3,
}

_AVAIL = ("ab sofort", "zum 01.01.2027", "zum 01.02.2027", "zum 01.04.2027",
          "3 Monate Kündigungsfrist", "6 Wochen zum Quartalsende", "nach Absprache")


def _towns_within(site: str, lo: float, hi: float, pool=None) -> list[str]:
    return [t for t in (pool or geo.TOWNS) if lo <= geo.km(t, site) <= hi]


def random_facts(rng: random.Random, trade: str | None = None) -> Facts:
    trade = trade or rng.choices(list(_TRADE_WEIGHTS), list(_TRADE_WEIGHTS.values()))[0]
    years = rng.choice((0, 1, 1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 18, 22, 27))
    pool = CERT_POOL.get(trade, DEFAULT_CERTS)
    certs = frozenset(rng.sample(pool, k=rng.choice((0, 1, 1, 2, 2, 3))))
    town = rng.choice(list(geo.OWL)) if rng.random() < 0.85 else rng.choice(list(geo.FAR))
    salary = 36_000 + 1_000 * min(years, 20) + rng.randrange(0, 9_000, 500)
    contact = date.fromordinal(TODAY.toordinal() - rng.randint(5, 1400))
    return Facts(trade=trade, years=years, certs=certs, licence=rng.random() < 0.85,
                 town=town, shift=rng.choices(SHIFTS, (0.4, 0.35, 0.25))[0],
                 on_call=rng.random() < 0.5, salary_eur=salary, available=rng.choice(_AVAIL),
                 last_contact=contact)


def fitting_facts(v: Vacancy, rng: random.Random) -> Facts:
    """Facts that meet every must-have of v, with a margin on the radius."""
    f = random_facts(rng, rng.choice(v.trades))
    certs = set(f.certs)
    if v.certs_any and not certs & set(v.certs_any):
        certs.add(rng.choice(v.certs_any))
    shift = f.shift
    if v.shift and SHIFTS.index(shift) > SHIFTS.index(v.shift):
        shift = rng.choice(SHIFTS[: SHIFTS.index(v.shift) + 1])
    return replace(
        f, years=max(f.years, v.min_years + rng.choice((0, 1, 2, 4, 7, 11))),
        certs=frozenset(certs), shift=shift,
        licence=True if v.licence else f.licence,
        on_call=True if v.on_call else f.on_call,
        town=rng.choice(_towns_within(v.site, 0, v.radius_km - 5, geo.OWL)))


def failing_facts(v: Vacancy, must: str, rng: random.Random) -> Facts:
    """Facts that meet every must-have of v except one."""
    f = fitting_facts(v, rng)
    if must == "beruf":
        f = replace(f, trade=rng.choice(v.lookalikes))
    elif must == "erfahrung":
        f = replace(f, years=rng.randint(0, v.min_years - 1))
    elif must == "zertifikate":
        pool = [c for c in CERT_POOL.get(f.trade, DEFAULT_CERTS) if c not in v.certs_any]
        f = replace(f, certs=frozenset(rng.sample(pool, k=min(len(pool), rng.choice((1, 2))))))
    elif must == "fuehrerschein":
        f = replace(f, licence=False)
    elif must == "entfernung":
        f = replace(f, town=rng.choice(_towns_within(v.site, v.radius_km + 20, 400)))
    elif must == "schicht":
        f = replace(f, shift=rng.choice(SHIFTS[SHIFTS.index(v.shift) + 1:]))
    elif must == "rufbereitschaft":
        f = replace(f, on_call=False)
    return f


# ---------------------------------------------------------------- presentation

def _synonym(trade: str, rng: random.Random) -> str:
    return rng.choice(TRADES[trade])


def presentation(f: Facts, rng: random.Random, title: str, hidden=()) -> Presentation:
    text = {"canonical": f.trade, "synonym": _synonym(f.trade, rng), "none": ""}[title]
    # The notes name the trade the way the title does, or by another synonym.
    term = text if text and rng.random() < 0.6 else (
        f.trade if title == "canonical" else _synonym(f.trade, rng))
    hidden = set(hidden) | ({"trade"} if title == "none" else set())
    return Presentation(title=title, title_text=text, term=term, hidden=frozenset(hidden),
                        style=rng.choice(("stichpunkte", "fliesstext", "cv", "chaos")))


def random_presentation(f: Facts, rng: random.Random) -> Presentation:
    title = rng.choices(("canonical", "synonym", "none"), (0.55, 0.35, 0.10))[0]
    hidden = {h for h in HIDEABLE[1:] if rng.random() < 0.2}
    return presentation(f, rng, title, hidden)


# ---------------------------------------------------------------- the pool

PLANT_FITS = {"plain": 4, "synonym": 4, "buried": 4}  # per vacancy
PLANT_NEAR = 2  # per vacancy and failed must-have


@dataclass
class Pool:
    profiles: list[Profile]
    vacancies: tuple[Vacancy, ...]
    seed: int

    def by_id(self) -> dict[str, Profile]:
        return {p.id: p for p in self.profiles}

    def public(self) -> list[dict]:
        return [p.public() for p in self.profiles]


def make_pool(n: int = 400, seed: int = 7, vacancies: tuple[Vacancy, ...] = VACANCIES) -> Pool:
    """n profiles: planted fits and near-misses per vacancy, the rest background.

    Background profiles that happen to fit any vacancy are redrawn, so every
    true fit in the pool is a planted one and the number per vacancy is known.
    Near-misses arise in the background too and are counted as such.
    """
    from .notes import render_notes

    fact_rng = random.Random(f"facts-{seed}")
    pres_rng = random.Random(f"pres-{seed}")
    id_rng = random.Random(f"identity-{seed}")
    note_rng = random.Random(f"notes-{seed}")
    order_rng = random.Random(f"order-{seed}")

    drafts: list[tuple[Facts, Presentation, str | None]] = []
    for v in vacancies:
        for case, count in PLANT_FITS.items():
            for _ in range(count):
                f = fitting_facts(v, fact_rng)
                if case == "plain":
                    pr = presentation(f, pres_rng, "canonical")
                elif case == "synonym":
                    pr = presentation(f, pres_rng, "synonym")
                else:
                    must = pres_rng.choice([m for m in v.musts() if m != "entfernung"])
                    title = pres_rng.choice(("canonical", "synonym"))
                    if must == "beruf":
                        title = "none"
                    pr = presentation(f, pres_rng, title, {MUST_FACT[must]} - {"trade"})
                drafts.append((f, pr, f"fit:{v.key}:{case}"))
        for must in v.musts():
            for _ in range(PLANT_NEAR):
                f = failing_facts(v, must, fact_rng)
                # Looks right: the title is the trade's own name, and the failing fact
                # is more often than not left to the notes.
                hidden = {MUST_FACT[must]} if (must not in ("beruf", "entfernung")
                                              and pres_rng.random() < 0.6) else set()
                pr = presentation(f, pres_rng, "canonical", hidden)
                drafts.append((f, pr, f"near:{v.key}:{must}"))
    while len(drafts) < n:
        f = random_facts(fact_rng)
        if any(is_fit(v, f) for v in vacancies):
            continue
        drafts.append((f, random_presentation(f, pres_rng), None))

    order_rng.shuffle(drafts)
    profiles = []
    for i, (f, pr, planted) in enumerate(drafts):
        ident = random_identity(id_rng)
        pid = f"p{i + 1:04d}"
        missing = None
        if planted and planted.endswith(":zertifikate"):
            missing = VACANCY_BY_KEY[planted.split(":")[1]].certs_any[0]
        notes = render_notes(f, pr, ident, random.Random(f"{note_rng.random()}"), missing)
        profiles.append(Profile(pid, ident, f, pr, notes, planted))
    return Pool(profiles, tuple(vacancies), seed)


def swap_names(pool: Pool, seed: int) -> list[Profile]:
    """The same profiles with only the name changed, to another origin, same gender.

    The surname is also replaced where the notes use it ("Herr Kaya"). Names are
    one token each, so the text keeps its length and a keyword index scores the
    swapped record exactly as before except for the name itself.
    """
    rng = random.Random(f"swap-{seed}")
    out = []
    for p in pool.profiles:
        others = [o for o in ORIGINS if o != p.identity.origin]
        new = random_identity(rng, rng.choice(others), p.identity.gender)
        notes = re.sub(rf"\b{re.escape(p.identity.last)}\b",
                       lambda m, n=new.last: n.lower() if m.group(0).islower() else n,
                       p.notes, flags=re.IGNORECASE)
        out.append(replace(p, identity=new, notes=notes))
    return out
