"""Tests for the classifier. Run from the repository root: pytest tests"""

import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python"))

from recipe_vectors import FAMILIES, classify, classify_json, bakers_percentages, cosine  # noqa: E402
from sourced_recipes import RECIPES  # noqa: E402

BY_ID = {recipe["id"]: recipe for recipe in RECIPES}


def test_flour_is_always_100_percent():
    assert bakers_percentages({"flour": 500, "liquid": 300}) == pytest.approx(
        {"flour": 100, "liquid": 60, "fat": 0, "sugar": 0, "egg": 0}
    )


@pytest.mark.parametrize("factor", [2, 10, 0.25])
def test_batch_size_does_not_change_the_answer(factor):
    grams = BY_ID["challah"]["grams"]
    scaled = {name: amount * factor for name, amount in grams.items()}
    original, doubled = classify(grams), classify(scaled)
    assert doubled["ranking"] == original["ranking"]
    assert doubled["scores"] == pytest.approx(original["scores"])


def test_each_family_matches_itself_perfectly():
    for name, vector in FAMILIES.items():
        assert cosine(vector, vector) == pytest.approx(1)
        grams = dict(zip(("flour", "liquid", "fat", "sugar", "egg"), vector))
        assert classify(grams)["closest"] == name


def test_blend_weights_sum_to_one():
    assert sum(classify(BY_ID["brioche"]["grams"])["blend"].values()) == pytest.approx(1)


@pytest.mark.parametrize("grams, code", [({"liquid": 10}, "no_flour"), ({"flour": 10, "fat": -1}, "negative_amount")])
def test_bad_input_reports_a_code_and_does_not_crash(grams, code):
    assert json.loads(classify_json(json.dumps(grams))) == {"error": code}


def test_test_set_has_three_published_recipes_per_family():
    for family in FAMILIES:
        assert sum(recipe["family"] == family for recipe in RECIPES) == 3
    assert all(recipe["url"].startswith("https://") for recipe in RECIPES)


def test_score_quoted_in_the_deck():
    correct = sum(classify(r["grams"])["closest"] == r["family"] for r in RECIPES)
    assert (correct, len(RECIPES)) == (9, 12)


def test_claims_made_on_slide_9():
    brioche = classify(BY_ID["brioche"]["grams"])
    assert brioche["closest"] == "cookie" and brioche["runner_up"] == "pie"
    assert f'{brioche["gap"]:.3f}' == "0.006"
    assert brioche["ranking"][-1] == "bread", "the slide says bread came last"

    toll_house = BY_ID["toll_house"]["grams"]
    assert toll_house["egg"] > 0, "the slide says the recipe has eggs"
    assert classify(toll_house)["closest"] == "cake"

    sucree = BY_ID["pate_sucree"]["grams"]
    assert classify(sucree)["closest"] == "cookie"
    assert "liquid" not in sucree and sucree["sugar"] and sucree["egg"], "the slide says no water, with sugar and egg"


def test_page_runs_the_same_python_as_the_repo():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    inlined = re.search(r'id="py-source">\n(.*?)\n</script>', html, re.DOTALL).group(1)
    assert inlined == (ROOT / "python" / "recipe_vectors.py").read_text(encoding="utf-8").rstrip()
