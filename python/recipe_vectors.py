"""Classify a recipe by the ratio of its ingredients.

A recipe becomes a five-dimensional vector of baker's percentages, and cosine
similarity finds the closest of four reference families.

This exact file also runs inside the presentation, through Pyodide. It uses the
standard library only, so the browser has no extra packages to download.
"""

import json
import math

INGREDIENTS = ("flour", "liquid", "fat", "sugar", "egg")

# How sharply the 3D blend favors the winning family. Scores sit close together
# because flour dominates every vector, so a plain share of the scores would
# blend all four shapes into a shapeless lump.
BLEND_SHARPNESS = 24


def _ratio(**parts):
    """Turn published parts, such as flour=5, liquid=3, into a percentage vector."""
    return tuple(100 * parts.get(name, 0) / parts["flour"] for name in INGREDIENTS)


# Published ratios, from Michael Ruhlman, "Ratio" (2009).
FAMILIES = {
    "bread": _ratio(flour=5, liquid=3),
    "cake": _ratio(flour=1, fat=1, sugar=1, egg=1),
    "cookie": _ratio(flour=3, fat=2, sugar=1),
    "pie": _ratio(flour=3, fat=2, liquid=1),
}


def bakers_percentages(grams):
    """Express every ingredient as a percentage of the flour's weight."""
    values = [float(grams.get(name, 0)) for name in INGREDIENTS]
    if any(value < 0 for value in values):
        raise ValueError("negative_amount")
    flour = values[0]
    if flour <= 0:
        raise ValueError("no_flour")
    return {name: 100 * value / flour for name, value in zip(INGREDIENTS, values)}


def cosine(a, b):
    """Cosine of the angle between two vectors: 1.0 means the same direction."""
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.hypot(*a) * math.hypot(*b))


def classify(grams):
    """Rank the four families for a recipe given in grams."""
    percentages = bakers_percentages(grams)
    vector = tuple(percentages[name] for name in INGREDIENTS)
    scores = {name: cosine(vector, ref) for name, ref in FAMILIES.items()}
    ranking = sorted(scores, key=scores.get, reverse=True)

    weights = {name: math.exp(BLEND_SHARPNESS * score) for name, score in scores.items()}
    total = sum(weights.values())

    return {
        "percentages": percentages,
        "scores": scores,
        "ranking": ranking,
        "closest": ranking[0],
        "runner_up": ranking[1],
        "gap": scores[ranking[0]] - scores[ranking[1]],
        "blend": {name: weight / total for name, weight in weights.items()},
    }


def classify_json(payload):
    """Entry point for the page: JSON text in, JSON text out."""
    try:
        return json.dumps(classify(json.loads(payload)))
    except ValueError as problem:
        return json.dumps({"error": str(problem)})
