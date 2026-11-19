import pytest

from poolgate.gate import evaluate_vacancy, run_matcher, wilson
from poolgate.keyword import FieldFilterMatcher, KeywordMatcher
from poolgate.offline import OfflineMatcher
from poolgate.pool import make_pool, origin_of
from poolgate.types import Ranked


@pytest.fixture(scope="module")
def pool():
    return make_pool(400, 7)


def _run(pool, m, **kw):
    return run_matcher(m, pool, **kw)


def test_wilson_bounds():
    lo, hi = wilson(0, 10)
    assert lo == 0.0 and 0.25 < hi < 0.35
    lo, hi = wilson(10, 10)
    assert hi == 1.0 and 0.65 < lo < 0.75
    assert wilson(0, 0) == (0.0, 1.0)


def test_clean_stand_in_is_perfect(pool):
    r = _run(pool, OfflineMatcher(pool.by_id()))
    m = r["metrics"]
    assert m["recall@20"]["rate"] == 1.0
    assert m["precision@10"]["rate"] == 1.0
    assert m["near_miss@10"]["k"] == 0
    assert m["shortlist"]["precision"]["rate"] == 1.0
    assert m["shortlist"]["recall"]["rate"] == 1.0
    assert all(c["right"]["rate"] == 1.0 for c in m["must_reading"].values())
    assert r["fairness"]["shortlist_flips_on_swap"]["k"] == 0
    assert r["fairness"]["shortlist_flips_on_repeat"]["k"] == 0
    assert r["errors"] == []


def test_recall_at_10_ceiling_is_reported(pool):
    m = _run(pool, OfflineMatcher(pool.by_id()), fairness=False)["metrics"]
    # More fits than places: recall@10 is capped below 1 and the cap is stated.
    assert m["recall@10"]["rate"] == pytest.approx(m["recall@10"]["ceiling"])
    assert m["recall@10"]["ceiling"] < 1.0


def test_missed_synonyms_show_in_the_synonym_row_only(pool):
    m = _run(pool, OfflineMatcher(pool.by_id(), miss_synonym=1.0), fairness=False)["metrics"]
    assert m["by_case"]["synonym"]["in_shortlist"]["rate"] == 0.0
    assert m["by_case"]["plain"]["in_shortlist"]["rate"] == 1.0
    assert m["by_case"]["buried"]["in_shortlist"]["rate"] == 1.0


def test_missed_buried_facts_show_in_the_buried_rows(pool):
    r = _run(pool, OfflineMatcher(pool.by_id(), miss_buried=1.0), fairness=False)
    m = r["metrics"]
    assert m["by_case"]["buried"]["in_shortlist"]["rate"] == 0.0
    assert m["by_case"]["plain"]["in_shortlist"]["rate"] == 1.0
    missed = [x for e in r["per_vacancy"] for x in e["missed"]]
    assert missed and all(x["case"].startswith("buried:") for x in missed)
    # The stand-in says which must-have it misread, and the gate reports it.
    assert all(x["misread"] == [x["case"].split(":")[1]] for x in missed)


def test_near_misses_taken_for_fits_are_caught(pool):
    r = _run(pool, OfflineMatcher(pool.by_id(), near_miss=1.0), fairness=False)
    m = r["metrics"]
    assert m["near_miss@20"]["k"] > 0
    assert m["shortlist"]["near_misses_in"] > 0
    assert m["shortlist"]["precision"]["rate"] < 0.6
    fps = [x for e in r["per_vacancy"] for x in e["false_positives"]]
    assert fps and all(x["near_miss"] for x in fps)


def test_name_bias_shows_above_repeat_baseline_and_lands_on_the_group(pool):
    r = _run(pool, OfflineMatcher(pool.by_id(), bias={"tr": 1}))
    f = r["fairness"]
    assert f["shortlist_flips_on_swap"]["k"] > 0
    assert f["shortlist_flips_on_repeat"]["k"] == 0
    lost = f["lost_shortlist_place"]
    assert lost["tr"]["rate"] > 0.2
    for g in ("de", "pl", "ua", "ar"):
        assert lost[g]["rate"] < 0.05, (g, lost[g])
    assert f["mean_rank_gain_when_renamed_to"]["tr"] < 0


def test_noise_shows_in_the_repeat_baseline(pool):
    f = _run(pool, OfflineMatcher(pool.by_id(), noise=30.0))["fairness"]
    assert f["shortlist_flips_on_repeat"]["k"] > 0


def test_keyword_matchers_are_name_blind(pool):
    for m in (KeywordMatcher(), KeywordMatcher(soft_filter=False), FieldFilterMatcher()):
        f = _run(pool, m)["fairness"]
        assert f["shortlist_flips_on_swap"]["k"] == 0, m.name


def test_field_filter_is_precise_and_blind_to_notes(pool):
    m = _run(pool, FieldFilterMatcher(), fairness=False)["metrics"]
    assert m["shortlist"]["precision"]["rate"] == 1.0
    assert m["by_case"]["plain"]["recall@20"]["rate"] == 1.0
    assert m["by_case"]["buried"]["recall@20"]["rate"] < 0.5


def test_soft_filter_keeps_every_fit_ahead_of_contradicted_records(pool):
    for v in pool.vacancies:
        ranking = KeywordMatcher().rank(v.public(), pool.public())
        e = evaluate_vacancy(pool, v, ranking)
        n_ok = sum(1 for r in ranking if not r.note)
        assert all(e["pos"][pid] <= n_ok for pid in e["fits"])


def test_a_failing_matcher_does_not_sink_the_run(pool):
    class Flaky(OfflineMatcher):
        def rank(self, vacancy, profiles):
            if vacancy["key"] == "cnc-guetersloh":
                raise RuntimeError("boom")
            return super().rank(vacancy, profiles)

    r = _run(pool, Flaky(pool.by_id()), fairness=False)
    assert r["metrics"]["vacancies"] == 2
    assert r["errors"][0]["where"].endswith("cnc-guetersloh")


def test_omitted_profiles_rank_last(pool):
    from poolgate.gate import _positions

    pos = _positions([Ranked("p0002", 1.0)], ["p0001", "p0002", "p0003"])
    assert pos == {"p0002": 1, "p0001": 2, "p0003": 3}


def test_origin_of_reads_the_name():
    assert origin_of("Ayşe Yılmaz") == "tr"
    assert origin_of("Lukas Brinkmann") == "de"
