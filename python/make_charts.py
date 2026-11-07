"""Run the classifier on the 12 published recipes and save the results.

Writes assets/similarity-heatmap.png and prints the table shown in the README.

Run from anywhere: python3 python/make_charts.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

from recipe_vectors import classify  # noqa: E402
from sourced_recipes import RECIPES  # noqa: E402

OUTPUT = Path(__file__).resolve().parent.parent / "assets" / "similarity-heatmap.png"
FAMILIES = ("bread", "cake", "cookie", "pie")
LABELS = {
    "baguette": "Baguette", "challah": "Challah", "brioche": "Brioche",
    "yellow_cake": "Yellow butter cake", "joy_yellow_cake": "Yellow cake", "genoise": "Genoise",
    "toll_house": "Toll House cookie", "shortbread": "Shortbread", "sugar_cookie": "Sugar cookie",
    "pate_brisee": "Pâte brisée", "pate_sucree": "Pâte sucrée", "all_butter_crust": "All-butter crust",
}


def print_table(results):
    print(f"{'Recipe':20}{'Labeled':9}{'Closest':9}{'Score':>6}  {'Runner-up':11}{'Gap':>6}")
    for recipe, result in results:
        mark = "" if result["closest"] == recipe["family"] else "  <- miss"
        print(
            f"{LABELS[recipe['id']]:20}{recipe['family']:9}{result['closest']:9}"
            f"{result['scores'][result['closest']]:6.3f}  {result['runner_up']:11}{result['gap']:6.3f}{mark}"
        )
    correct = sum(result["closest"] == recipe["family"] for recipe, result in results)
    print(f"\n{correct} of {len(results)} correct")


def save_heatmap(results):
    grid = [[result["scores"][family] for family in FAMILIES] for _, result in results]
    fig, ax = plt.subplots(figsize=(7.4, 7.2), dpi=180)
    image = ax.imshow(grid, cmap="YlOrBr", vmin=0.4, vmax=1, aspect="auto")

    ax.set_xticks(range(len(FAMILIES)), [family.capitalize() for family in FAMILIES])
    ax.set_yticks(range(len(results)), [LABELS[recipe["id"]] for recipe, _ in results])
    ax.xaxis.tick_top()
    ax.tick_params(length=0, labelsize=10.5)
    for spine in ax.spines.values():
        spine.set_visible(False)

    for row, (recipe, result) in enumerate(results):
        for col, family in enumerate(FAMILIES):
            score = result["scores"][family]
            ax.text(col, row, f"{score:.2f}", ha="center", va="center", fontsize=10,
                    color="white" if score > 0.78 else "#3A2314")
        chosen = FAMILIES.index(result["closest"])
        missed = result["closest"] != recipe["family"]
        ax.add_patch(Rectangle((chosen - 0.5, row - 0.5), 1, 1, fill=False,
                               edgecolor="#B3261E" if missed else "#3A2314",
                               linewidth=2.6 if missed else 1.4, linestyle="--" if missed else "-"))

    for row in (2.5, 5.5, 8.5):
        ax.axhline(row, color="white", linewidth=4)

    correct = sum(result["closest"] == recipe["family"] for recipe, result in results)
    ax.set_title(f"Cosine similarity to each family: {correct} of {len(results)} closest match the label",
                 fontsize=12, pad=30, loc="left")
    fig.text(0.02, 0.012, "Outline: the model's pick. Dashed red: the pick disagrees with our label.",
             fontsize=9.5, color="#5C422C")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    OUTPUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUTPUT, facecolor="white")
    print(f"\nsaved {OUTPUT.name}")


def main():
    results = [(recipe, classify(recipe["grams"])) for recipe in RECIPES]
    print_table(results)
    save_heatmap(results)


if __name__ == "__main__":
    main()
