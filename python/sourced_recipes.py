"""The test set: twelve published recipes, three per family.

This list was fixed before any result was computed, so the score in the deck
can't have been improved by choosing recipes that flatter the method.

Mapping rules:
- liquid: water, milk
- fat: butter, oil
- sugar: all sugars together
- egg: whole eggs or yolks, by weight
- Salt, yeast, leavening and flavorings aren't part of the five-ingredient model.

Where a source gives volumes or a count, `converted` says how it became grams.
"""

RECIPES = [
    {
        "id": "baguette",
        "name_he": "באגט",
        "family": "bread",
        "grams": {"flour": 100, "liquid": 66},
        "source": "The Fresh Loaf forum: typical French baguette, about 66% hydration",
        "url": "https://www.thefreshloaf.com/comment/231231",
        "converted": "Forum figure for a typical dough, not a single published recipe.",
    },
    {
        "id": "challah",
        "name_he": "חלה",
        "family": "bread",
        "grams": {"flour": 100, "liquid": 43, "fat": 6, "sugar": 11, "egg": 16},
        "source": "Ginsberg and Berg, Inside the Jewish Bakery: Challah",
        "url": "https://cdn.shopify.com/s/files/1/0874/5798/files/Website_excerpt_challah.pdf",
    },
    {
        "id": "brioche",
        "name_he": "בריוש",
        "family": "bread",
        "grams": {"flour": 100, "liquid": 9, "fat": 50, "sugar": 12, "egg": 50},
        "source": "King Arthur Baking, Brioche professional formula",
        "url": "https://www.kingarthurbaking.com/pro/formulas/brioche",
    },
    {
        "id": "yellow_cake",
        "name_he": "עוגת חמאה",
        "family": "cake",
        "grams": {"flour": 850, "liquid": 850, "fat": 680, "sugar": 740, "egg": 425},
        "source": "Kreol Magazine, Yellow Butter Cake",
        "url": "https://kreolmagazine.com/recipes-yellow-butter-cake/",
    },
    {
        "id": "joy_yellow_cake",
        "name_he": "עוגה צהובה",
        "family": "cake",
        "grams": {"flour": 300, "liquid": 240, "fat": 170, "sugar": 265, "egg": 110},
        "source": "Joy of Baking, Yellow Butter Cake",
        "url": "https://www.joyofbaking.com/printpages/YellowCakeprint.html",
        "converted": "240 ml milk counted as 240 g. Egg is yolks.",
    },
    {
        "id": "genoise",
        "name_he": "גנואז",
        "family": "cake",
        "grams": {"flour": 125, "fat": 60, "sugar": 125, "egg": 200},
        "source": "River Cottage, Genoese Sponge Cake",
        "url": "https://rivercottage.net/recipes/genoese-sponge-cake/",
        "converted": "4 medium eggs counted as 200 g.",
    },
    {
        "id": "toll_house",
        "name_he": "שוקולד צ׳יפס",
        "family": "cookie",
        "grams": {"flour": 360, "fat": 220, "sugar": 315, "egg": 100},
        "source": "Original Nestlé Toll House recipe, via Cooking for Engineers",
        "url": "https://CookingForEngineers.com/recipe/185/Nestle-Toll-House-Chocolate-Chip-Cookies",
        "converted": (
            "The recipe is in cups. Grams are the source author's conversion: flour 360 g, "
            "which he concludes was intended (280 g if sifted), butter 220 g, sugars 150 g "
            "plus 165 g, eggs 100 g."
        ),
    },
    {
        "id": "shortbread",
        "name_he": "שורטברד",
        "family": "cookie",
        "grams": {"flour": 180, "fat": 125, "sugar": 55},
        "source": "BBC Food shortbread, as reproduced by Age UK",
        "url": "https://www.ageuk.org.uk/bp-assets/globalassets/northumberland/winter-warmers---shortbread.pdf",
    },
    {
        "id": "sugar_cookie",
        "name_he": "עוגיות סוכר",
        "family": "cookie",
        "grams": {"flour": 250, "fat": 170, "sugar": 200, "egg": 50},
        "source": "Essential Crunchy Sugar Cookies (King Arthur Flour), third-party copy",
        "url": "https://www.snapcalorie.com/recipes/the_essential_crunchy_sugar_cookies_king_arthur_flour.html",
        "converted": "1 large egg counted as 50 g.",
    },
    {
        "id": "pate_brisee",
        "name_he": "פאט בריזה",
        "family": "pie",
        "grams": {"flour": 250, "liquid": 80, "fat": 125},
        "source": "Magimix, Shortcrust Pastry (Pâte Brisée)",
        "url": "https://magimix.com.au/recipes/shortcrust-pastry-pate-brisee",
        "converted": (
            "80 ml water counted as 80 g. The page refuses automated reading, so these "
            "figures come from a search result, not a direct read."
        ),
    },
    {
        "id": "pate_sucree",
        "name_he": "פאט סוקרה",
        "family": "pie",
        "grams": {"flour": 200, "fat": 100, "sugar": 100, "egg": 50},
        "source": "The Pastry Maestra, Pâte Sucrée",
        "url": "https://pastrymaestra.com/wp-content/uploads/2019/05/Pate-Sucree-Recipe-EN-Pastry-Maestra.pdf",
    },
    {
        "id": "all_butter_crust",
        "name_he": "בצק פאי חמאה",
        "family": "pie",
        "grams": {"flour": 300, "liquid": 119, "fat": 227},
        "source": "King Arthur Baking, Easy as Pie class handout (July 2025)",
        "url": "https://shop.kingarthurbaking.com/content/class-pdfs/EasyAsPie_July2025.pdf",
    },
]
