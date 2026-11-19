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
                assert re.search(rf"\b({f.years}|{TODAY.year - f.years})\b", notes), p.id
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
    assert feminine("Mechatroniker/in IHK") == "Mechatroniker/in IHK"
