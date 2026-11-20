import re

import pytest

from poolgate.keyword import contradicted, tokens
from poolgate.notes import feminine
from poolgate.pool import (
    CERTS,
    PLANT_FITS,
    TODAY,
    VACANCIES,
    VACANCY_BY_KEY,
    is_fit,
    make_pool,
    near_miss,
    swap_names,
    training_end,
    years_at,
)


@pytest.fixture(scope="module")
def pool():
    return make_pool(400, 7)


def test_every_planted_label_agrees_with_the_rules(pool):
    for p in pool.profiles:
        if not p.planted:
            continue
        kind, key, what = p.planted.split(":")
        v = VACANCY_BY_KEY[key]
        if kind == "fit":
            assert is_fit(v, p.facts), p.planted
        else:
            assert near_miss(v, p.facts) == what, (p.id, p.planted)


def test_background_never_fits(pool):
    for p in pool.profiles:
        if p.planted is None:
            assert not any(is_fit(v, p.facts) for v in VACANCIES), p.id


def test_each_vacancy_has_its_planted_fits(pool):
    for v in VACANCIES:
        planted = [p for p in pool.profiles if p.planted and p.planted.startswith(f"fit:{v.key}")]
        assert len(planted) == sum(PLANT_FITS.values())


def test_pool_is_deterministic():
    a, b = make_pool(120, 3), make_pool(120, 3)
    assert [p.public() for p in a.profiles] == [p.public() for p in b.profiles]


_SHIFT_WORDS = ("schicht", "nacht", "tagdienst")
_ONCALL_WORDS = ("rufbereitschaft", "rb", "bereitschaft", "notdienst")


def test_every_hidden_fact_is_stated_in_the_notes(pool):
    """A field left at k. A. must be recoverable from the notes, or the truth is unfair."""
    for p in pool.profiles:
        notes = p.notes.lower()
        f = p.facts
        for h in p.pres.hidden:
            if h == "trade":
                term = feminine(p.pres.term) if p.identity.gender == "f" else p.pres.term
                assert term.lower() in notes, (p.id, term)
            elif h == "years":
                n = years_at(f, f.last_contact)
                assert re.search(rf"\b({n}|{training_end(f)})\b", notes), p.id
            elif h == "licence":
                assert "fs" in tokens(notes) or "führerschein" in notes, p.id
            elif h == "shift":
                assert any(w in notes for w in _SHIFT_WORDS), p.id
            elif h == "on_call":
                assert any(w in tokens(notes) or w in notes for w in _ONCALL_WORDS), p.id
            elif h == "certs":
                if not f.certs:
                    assert "keine" in notes, p.id
                for c in f.certs:
                    assert any(s.lower() in notes for s in (c, *CERTS[c])), (p.id, c)


def test_no_true_fit_is_contradicted_by_its_fields(pool):
    """The keyword prefilter only drops explicit contradictions; a fit never has one."""
    for v in VACANCIES:
        for p in pool.profiles:
            if is_fit(v, p.facts):
                assert contradicted(v.public(), p.public()) == [], (v.key, p.id)


def test_name_swap_changes_only_the_name(pool):
    swapped = swap_names(pool, 99)
    for a, b in zip(pool.profiles, swapped):
        assert a.facts == b.facts and a.pres == b.pres and a.id == b.id
        assert a.identity.gender == b.identity.gender
        assert a.identity.origin != b.identity.origin
        assert len(tokens(a.notes)) == len(tokens(b.notes))
        assert a.identity.last.lower() not in b.notes.lower(), (a.id, b.notes)
        assert "er/sie" not in a.notes
        pa, pb = a.public(), b.public()
        assert {k: v for k, v in pa.items() if k not in ("name", "notizen")} == \
               {k: v for k, v in pb.items() if k not in ("name", "notizen")}


def test_feminine_forms():
    assert feminine("Elektroniker für Betriebstechnik") == "Elektronikerin für Betriebstechnik"
    assert feminine("CNC-Fräser") == "CNC-Fräserin"
    assert feminine("Mechatroniker/-in") == "Mechatroniker/-in"


def test_every_buried_type_occurs_for_every_vacancy(pool):
    from poolgate.pool import case_type

    for v in VACANCIES:
        cases = {case_type(v, p) for p in pool.profiles if is_fit(v, p.facts)}
        for m in v.musts():
            if m != "entfernung":
                assert f"buried:{m}" in cases, (v.key, m)


def test_no_job_titles_among_the_synonyms():
    from poolgate.pool import TRADES

    banned = ("CNC-Fräser", "Servicetechniker", "Zerspaner", "Gebäudeelektroniker",
              "Betriebselektroniker", "E-Techniker", "FR Betriebstechnik", "Infoelektroniker")
    for names in TRADES.values():
        for n in names:
            assert not any(n == b or n.startswith(b) for b in banned), n


def test_certificate_lists_in_notes_are_declared_complete(pool):
    for p in pool.profiles:
        if "certs" in p.pres.hidden and p.facts.certs:
            assert "keine" in p.notes.lower(), p.id


def test_every_shown_trade_name_was_in_use_when_the_training_started(pool):
    """Beruf field and notes alike: no name before it existed or after it was replaced."""
    from poolgate.pool import name_valid, training_start

    old = 0
    for p in pool.profiles:
        start = training_start(p.facts)
        for name in {p.pres.title_text, p.pres.term} - {""}:
            assert name_valid(p.facts.trade, name, start), (p.id, name, start)
        m = re.search(r"Ausbildung als .+? \((\d{4})-(\d{4})\)", p.notes)
        if m:
            assert int(m.group(1)) == start, (p.id, m.group(0))
        old += p.pres.title_text in ("Elektroinstallateur", "Betriebsschlosser", "Dreher",
                                     "Energieelektroniker Fachrichtung Betriebstechnik")
    assert old > 0  # predecessor names still occur, on careers long enough for them


def test_no_training_predates_every_name_of_its_trade(pool):
    from poolgate.pool import earliest_start, training_start

    for p in pool.profiles:
        lo = earliest_start(p.facts.trade)
        assert lo is None or training_start(p.facts) >= lo, p.id


def test_name_validity_rule():
    from poolgate.pool import name_valid

    t = "Elektroniker für Betriebstechnik"
    assert name_valid(t, t, 2003) and not name_valid(t, t, 2002)
    old = "Energieelektroniker Fachrichtung Betriebstechnik"
    assert name_valid(t, old, 2002) and not name_valid(t, old, 2003)
    assert not name_valid(t, old, 1986)
    assert not name_valid("Mechatroniker", "Mechatroniker", 1997)


# Every way the notes state experience as a duration, and as a year.
_DURATION = re.compile(r"(\d+) J\. Berufserfahrung|BE: (\d+) Jahre|nach der Ausbildung (\d+) Jahre"
                       r"|Berufserfahrung nach Ausbildung: (\d+) Jahre", re.IGNORECASE)
_CAREER_YEAR = re.compile(r"Abschluss Sommer (\d{4})|ausgelernt \((\d{4})\)|seit (\d{4}) im Beruf"
                          r"|Abschluss (?:IHK|HWK) (\d{4})|Gesellenprüfung (\d{4})"
                          r"|\((\d{4})-(\d{4})\)", re.IGNORECASE)


@pytest.mark.parametrize("seed", [7, 8, 9, 10, 11])
def test_notes_never_predate_the_career_and_agree_with_the_truth(seed):
    """One rule: a note states the career as of its own date, and the truth is the
    career at the Stand. So no note is dated before the training ended, every
    duration equals the experience on the note's date, and every year named in
    the career is the true one."""
    from poolgate.pool import graduation, training_start

    pool = make_pool(400, seed)
    durations = 0
    for p in pool.profiles:
        f = p.facts
        assert f.last_contact is not None and f.last_contact >= graduation(f), p.id
        assert f.last_contact <= TODAY, p.id
        assert years_at(f, TODAY) == f.years, p.id
        for m in _DURATION.finditer(p.notes):
            n = int(next(g for g in m.groups() if g))
            assert n == years_at(f, f.last_contact), (p.id, m.group(0), f.last_contact)
            durations += 1
        for m in _CAREER_YEAR.finditer(p.notes):
            got = [int(g) for g in m.groups() if g]
            want = ([training_start(f), training_end(f)] if len(got) == 2
                    else [training_end(f)])
            assert got == want, (p.id, m.group(0))
            assert max(got) <= f.last_contact.year, (p.id, m.group(0))
        assert "Abschluss Sommer" not in p.notes or years_at(f, f.last_contact) == 0, p.id
    assert durations > 50  # the rule is exercised, not vacuous


def test_years_are_counted_from_the_summer_the_training_ended():
    from datetime import date

    from poolgate.pool import Facts

    f = Facts("Mechatroniker", 3, frozenset(), True, "Paderborn", "2", True, 40_000, "ab sofort")
    assert training_end(f) == TODAY.year - 3
    assert years_at(f, date(TODAY.year - 3, 7, 1)) == 0
    assert years_at(f, date(TODAY.year - 2, 6, 30)) == 0
    assert years_at(f, date(TODAY.year - 2, 7, 1)) == 1
    assert years_at(f, TODAY) == 3
