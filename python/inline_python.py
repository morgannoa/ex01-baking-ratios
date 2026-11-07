"""Copy the classifier and its precomputed results into index.html.

A page opened from file:// can't fetch a neighboring .py file, so the page needs
its own copy. This script writes that copy, which keeps python/recipe_vectors.py
as the single source of truth. tests/test_recipe_vectors.py fails if they differ.

The precomputed results let the deck quote real numbers and keep working on its
presets if Pyodide can't load.

Run from anywhere: python3 python/inline_python.py
"""

import json
import re
from pathlib import Path

from recipe_vectors import FAMILIES, INGREDIENTS, classify
from sourced_recipes import RECIPES

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "index.html"
SOURCE = Path(__file__).with_name("recipe_vectors.py")


def build_data():
    recipes = [{**recipe, "result": classify(recipe["grams"])} for recipe in RECIPES]
    correct = sum(recipe["result"]["closest"] == recipe["family"] for recipe in recipes)
    return {
        "ingredients": INGREDIENTS,
        "families": {name: dict(zip(INGREDIENTS, vector)) for name, vector in FAMILIES.items()},
        "recipes": recipes,
        "score": {"correct": correct, "total": len(recipes)},
    }


def replace_block(html, element_id, content):
    pattern = re.compile(rf'(<script [^>]*id="{element_id}"[^>]*>).*?(</script>)', re.DOTALL)
    updated, count = pattern.subn(lambda m: f"{m.group(1)}\n{content}\n{m.group(2)}", html)
    if count != 1:
        raise SystemExit(f'expected one <script id="{element_id}"> in index.html, found {count}')
    return updated


def main():
    html = HTML.read_text(encoding="utf-8")
    html = replace_block(html, "py-source", SOURCE.read_text(encoding="utf-8").rstrip())
    data = json.dumps(build_data(), ensure_ascii=False, separators=(",", ":"))
    html = replace_block(html, "py-data", data)
    HTML.write_text(html, encoding="utf-8")
    print(f"inlined {SOURCE.name} and {len(RECIPES)} recipes into {HTML.name}")


if __name__ == "__main__":
    main()
