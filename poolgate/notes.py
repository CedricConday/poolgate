"""Free-text profile notes, written the way recruiters and CVs write them.

Notes mix telephone-call shorthand, CV snippets, abbreviations and typos. Every
fact whose structured field is empty ("k. A.") is stated here, unambiguously;
other facts are repeated sometimes, as real notes do. Typos only touch filler
words, so a fact never becomes unreadable by accident: hard cases are hard by
design (synonyms, buried facts), not by noise.
"""

from __future__ import annotations

import random
import re

from .pool import (
    CERTS,
    DURATION,
    HANDWERK,
    SHIFT_LABEL,
    TODAY,
    Facts,
    Identity,
    Presentation,
    training_end,
    years_at,
)

_HEADS = ("niker", "chaniker", "techniker", "fräser", "zerspaner", "elektriker", "schlosser",
          "installateur", "dreher", "bediener", "führer", "lagerist", "macher", "bauer",
          "einrichter", "logistiker")


def feminine(term: str) -> str:
    """Elektroniker für X -> Elektronikerin für X; first matching head noun only."""
    pat = r"\b([\wÄÖÜäöüß-]*(?:" + "|".join(_HEADS) + r"))\b(?!/-?in|in)"
    return re.sub(pat, r"\1in", term, count=1, flags=re.IGNORECASE)


def _date(d) -> str:
    return d.strftime("%d.%m.%y")


FIRMS = ("einem Kunststoffverarbeiter", "einem Automobilzulieferer", "einem Antriebshersteller",
         "einem Möbelhersteller", "einem Landmaschinenhersteller", "einem Metallbaubetrieb",
         "einer Molkerei", "einem Verpackungshersteller", "einem Familienbetrieb im Maschinenbau",
         "einem Sondermaschinenbauer", "einem Elektro-Handwerksbetrieb", "einer Gießerei",
         "einem Zeitarbeitsunternehmen", "einer Großbäckerei", "einem Haustechnik-Betrieb")

FILLER = (
    "Wechselmotivation: mehr Geld und kürzerer Arbeitsweg",
    "wirkt ruhig, fachlich aber sicher",
    "sehr motiviert, will sich weiterentwickeln",
    "Interesse an Weiterbildung zum Techniker",
    "Rückruf lieber abends nach 17 Uhr",
    "bevorzugt Kontakt per Mail",
    "aktuell in Kurzarbeit, deshalb offen",
    "hatte schon mal Kontakt zu uns, damals Stelle besetzt",
    "Unterlagen vollständig, Zeugnisse liegen vor",
    "Lebenslauf etwas lückenhaft, im Gespräch aber plausibel erklärt",
    "kam über Empfehlung",
    "will nicht in die Zeitarbeit",
    "Arbeitszeugnis gut bis sehr gut",
    "fragt nach Firmenwagen und Weiterbildungsbudget",
    "eher passiv wechselwillig",
)


def _trade(f: Facts, pr: Presentation, ident: Identity, rng: random.Random) -> str:
    term = feminine(pr.term) if ident.gender == "f" else pr.term
    end = training_end(f)
    # Handwerk trades end in the Gesellenprüfung at the Handwerkskammer, the rest at the IHK.
    exam = (f"Gesellenprüfung {end} (HWK)" if rng.random() < HANDWERK.get(f.trade, 0.0)
            else f"Abschluss IHK {end}")
    return rng.choice((
        f"Ausbildung als {term} ({end - DURATION.get(f.trade, 3)}-{end})",
        f"gelernt: {term}",
        f"{term}, {exam}",
        f"lt. CV Ausb. {term} bei {rng.choice(FIRMS)}",
        f"hat {term} gelernt",
    ))


def _years(f: Facts, rng: random.Random, anchored: bool) -> str:
    """Experience as of the note's date. A duration counts from the training's end
    to the day of the call; "Sommer 2019" holds at any date. Where the field is
    empty (`anchored`), the note names the season and year the training ended:
    a duration from an old note ("BE: 1 Jahr" in April 2025) cannot tell 1 year
    today from 2, so it alone would leave the truth unrecoverable."""
    n = years_at(f, f.last_contact)
    since = training_end(f)
    dated = ((f"Berufseinsteiger, Abschluss Sommer {since}",
              f"ausgelernt Sommer {since}, noch keine BE") if n == 0 else
             (f"seit Sommer {since} im Beruf (nach Ausbildung)",
              f"Abschluss Sommer {since}, seitdem im Beruf"))
    if anchored:
        return rng.choice(dated)
    return rng.choice(dated + ((
        f"{n} J. Berufserfahrung",
        f"BE: {n} Jahre",
        f"nach der Ausbildung {n} Jahre bei {rng.choice(FIRMS)}",
        f"Berufserfahrung nach Ausbildung: {n} Jahre",
    ) if n else ()))


def _cert(c: str, rng: random.Random) -> str:
    return rng.choice((c,) + CERTS[c])


def _certs(f: Facts, rng: random.Random, explicit_none: bool) -> str:
    if not f.certs:
        return rng.choice(("keine Zusatzqualifikationen", "Zusatzquali: keine",
                           "keine Lehrgänge/Scheine")) if explicit_none else ""
    shown = [_cert(c, rng) for c in sorted(f.certs)]
    # The list is declared complete, so a certificate not named is absent, not unknown.
    return rng.choice((
        "Zusatzqualis: " + ", ".join(shown) + ", sonst keine",
        "kann " + " und ".join(shown) + " (sonst keine Scheine/Lehrgänge)",
        "Lehrgänge: " + ", ".join(shown) + " - weitere keine",
        "Kenntnisse " + " / ".join(shown) + " vorhanden, darüber hinaus keine Zusatzqualis",
    ))


def _missing(c: str, rng: random.Random) -> str:
    return rng.choice((
        f"{_cert(c, rng)}: nein, hat damit nie gearbeitet",
        f"keine {c}-Kenntnisse",
        f"{c} kennt er/sie nur vom Namen, nie selbst gemacht",
    ))


def _licence(f: Facts, rng: random.Random) -> str:
    if f.licence:
        return rng.choice(("FS B vorhanden", "Führerschein Kl. B + eigenes Auto",
                           "FS Klasse B ja", "hat Führerschein B"))
    return rng.choice(("kein Führerschein", "FS ist weg (Punkte), MPU offen - aktuell kein FS",
                       "hat keinen FS, kommt mit Bus/Rad", "Führerschein: keiner"))


def _shift(f: Facts, rng: random.Random) -> str:
    return rng.choice({
        "3": ("3-Schicht ok", "Wechselschicht inkl. Nacht kein Problem",
              "Schichtbereitschaft: ja, auch Nachtschicht"),
        "2": ("2-Schicht ja, Nacht nein", "Früh/Spät ok, keine Nachtschicht",
              "Schicht nur Früh/Spät, Nachtschicht macht er/sie nicht mehr"),
        "tag": ("nur Tagschicht (Normalschicht)", "keine Schichtarbeit mehr gewünscht",
                "Schicht: nein, nur Tagdienst"),
    }[f.shift])


def _on_call(f: Facts, rng: random.Random) -> str:
    if f.on_call:
        return rng.choice(("Rufbereitschaft ok", "RB / Bereitschaft: ja",
                           "auch Notdienst am WE ok"))
    return rng.choice(("keine Rufbereitschaft", "Bereitschaftsdienste lehnt er/sie ab",
                       "RB: nein"))


def _salary(f: Facts, rng: random.Random) -> str:
    s = f.salary_eur
    return rng.choice((f"GV ca. {s // 1000}k", f"Gehaltsvorstellung {s:,} € p.a.".replace(",", "."),
                       f"will mind. {s // 1000}T brutto im Jahr"))


def _contact(f: Facts, ident: Identity, rng: random.Random) -> str:
    who = ("Frau " if ident.gender == "f" else "Herr ") + ident.last
    whom = ("Frau " if ident.gender == "f" else "Herrn ") + ident.last
    d = _date(f.last_contact)
    return rng.choice((f"TK {d} mit {whom}", f"[{d}] {whom} angerufen", f"zuletzt gesprochen {d}",
                       f"{d}: Telefonat mit {whom}", f"{d} {who} meldet sich"))


def _typos(text: str, rng: random.Random, rate: float) -> str:
    words = text.split(" ")
    for i, w in enumerate(words):
        core = w.strip(".,;:()")
        if len(core) > 4 and core.isalpha() and core.islower() and rng.random() < rate:
            j = rng.randrange(len(core) - 1)
            words[i] = w.replace(core, core[:j] + core[j + 1] + core[j] + core[j + 2:], 1)
    return " ".join(words)


def render_notes(f: Facts, pr: Presentation, ident: Identity, rng: random.Random,
                 missing_cert: str | None = None) -> str:
    """The notes for one profile. Facts in pr.hidden are always stated."""
    h = pr.hidden
    facts: list[str] = [_contact(f, ident, rng)]
    if "trade" in h or rng.random() < 0.7:
        facts.append(_trade(f, pr, ident, rng))
    if "years" in h or rng.random() < 0.4:
        facts.append(_years(f, rng, anchored="years" in h))
    if "certs" in h or rng.random() < 0.4:
        c = _certs(f, rng, explicit_none="certs" in h)
        if c:
            facts.append(c)
    if "licence" in h or rng.random() < 0.4:
        facts.append(_licence(f, rng))
    if "shift" in h or rng.random() < 0.4:
        facts.append(_shift(f, rng))
    if "on_call" in h or rng.random() < 0.4:
        facts.append(_on_call(f, rng))
    if rng.random() < 0.5:
        facts.append(_salary(f, rng))
    # Availability is a current fact; an old note does not repeat it.
    if (TODAY - f.last_contact).days <= 180 and rng.random() < 0.4:
        facts.append("verfügbar " + f.available)
    fillers = rng.sample(FILLER, k=rng.choice((1, 2, 2, 3)))
    if missing_cert:
        facts.append(_missing(missing_cert, rng))

    pronoun = "sie" if ident.gender == "f" else "er"
    facts = [x.replace("er/sie", pronoun) for x in facts]
    head, rest = facts[0], facts[1:]
    rng.shuffle(rest)
    if pr.style == "chaos":
        fillers = [_typos(x, rng, 0.35) for x in fillers]
        parts = [head] + rest + fillers
        rng.shuffle(parts)
        return " ".join(p.lower() if rng.random() < 0.5 else p for p in parts)
    if pr.style == "cv":
        return (head + ".\nWerdegang lt. CV:\n" + "\n".join(f"- {x}" for x in rest)
                + "\nNotiz: " + "; ".join(fillers))
    if pr.style == "fliesstext":
        return head + ". " + ". ".join(x[0].upper() + x[1:] for x in rest + fillers) + "."
    return "; ".join([head] + rest + fillers)


def shift_label(f: Facts) -> str:
    return SHIFT_LABEL[f.shift]
