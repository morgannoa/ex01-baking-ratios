# PRD: Same Five Ingredients (אותם חמישה מרכיבים)

**Status:** v1.0, accepted by the team on 2026-11-07
**Course:** Generative AI, Bar-Ilan University, Dr. Yoram Segal. Assignment 01.
**Due:** planned for Wed 2026-11-11 (Moodle closes Thu 2026-11-12 23:59; the lecturer's text says 11/11, so we use the earlier date)

## 1. The product

A Hebrew, interactive, single-file HTML presentation of about 10 slides on baking. It argues one idea:

> Bread, cake, cookies and pie are the same five ingredients in different ratios.

The audience reads a recipe as a vector, watches Python classify it, and sees the result bake in 3D.

## 2. Team brief

> **Provenance:** the team supplied the topic ("baking: cakes, breads, cookies, pies") and asked the model to draft the rest. These bullets are the model's draft, and the team accepted them as written.

1. Topic: baking, covering breads, cakes, cookies and pies.
2. Don't make a recipe collection. Make one argument: everything comes from the same five ingredients.
3. Teach baker's percentages, because they let you compare any two recipes regardless of batch size.
4. Python does a real job: it turns a recipe into a vector and finds its closest family with cosine similarity, the method taught in lecture 3.
5. The 3D object responds to Python's answer, so the two aren't separate decorations.
6. Don't use a spinning doughnut. It is the lecture's own example.
7. Show where the method fails. Admitting it is more honest and more interesting than hiding it.
8. Include one real recipe from our own kitchen.
9. Deck in Hebrew with correct RTL and BiDi. Engineering documents and prompts in English, as the lecture recommends for token cost.

## 3. Requirements traceability

| Source | Requirement | How we meet it | Verified by |
|---|---|---|---|
| Homework 1.1 | Topic we understand | Baking; the team reviews all content | Team content review |
| Homework 1.1 | JavaScript in the deck | Navigation, reveals, lab controls, sources panel | T1, T2 |
| Homework 1.1 | Python in the deck, with our own idea | Recipe classifier running in the page (section 6) | T3 |
| Homework 1.1 | Animated 3D with Three.js | Five-second bake (section 7) | T4 |
| Homework 1.1 | Evidence of control | Logged corrections; `## Decisions` in this file | Prompt log, Git history |
| Homework 1.1 | About 10 slides | 10 slides | T1 |
| Homework 1.2 | README with images and work method | Phase 6 | T6 |
| Homework 1.2 | `PRD.md` | This file | Present in repo root |
| Homework 1.2 | Prompt history showing see, fix, refine | `prompts/` | Team reads it |
| Homework 1.2 | Several pushes | One or more per phase, each with a real change | `git log` |
| Moodle | Dedicated prompts folder | `prompts/` | Present in repo |
| Moodle | README shows deck, video and Python output | Phase 6 | T6 |
| Moodle | Repo accessible, or grade 0 | Public repo | T7, incognito |
| Moodle | Separate upload by each student | Each student uploads on their own | Team |
| Moodle | PDF form, template unchanged, named `xxxxxxxx-ex01.pdf` | Form kept outside the repo; Word submission costs 30 points | T8 |
| Moodle | Exactly 8-character group code | `biu-noa7` | T8 |
| Moodle | Self grade | Chosen after T1 to T8 pass | Team |
| Lecture 5.5 | 3D animation of at most 5 seconds | Hard cap in code | T4 |
| Lecture 4 | Fancy, RTL, BiDi, navigation buttons, single file | All five apply | T1, T5 |

## 4. Slides

| # | Slide | Content | Interaction |
|---|---|---|---|
| 1 | Title | The claim, stated as a provocation | Start button |
| 2 | Five ingredients | Flour, liquid, fat, sugar, egg | Click to reveal each |
| 3 | Baker's percentage | Flour = 100%; every other ingredient relative to it | Doubling toggle: grams change, percentages don't |
| 4 | Bread | 5:3 flour to water; gluten and fermentation | Reveal |
| 5 | Cake | 1:1:1:1 pound cake; why it got its name | Reveal |
| 6 | Cookie and pie | Both 3:2:1, differing in one ingredient: sugar or water | Swap toggle |
| 7 | The oven | Five-second bake in 3D | Replay, drag to rotate |
| 8 | Python lab | Live classifier driving the 3D object | Sliders, recipe presets |
| 9 | Where it breaks | Brioche, pâte sucrée, and what cosine can't see | Reveal |
| 10 | Our kitchen | Our real recipe run through the lab; closing line | Sources panel |

All facts carry a source in the sources panel.

## 5. Interface

- Next and previous buttons, arrow keys, progress bar and slide counter.
- Soft fade between slides. Honors `prefers-reduced-motion`.
- `dir="rtl"` on the document. English terms are wrapped with `dir="ltr"` or `<bdi>` so that BiDi holds up inside Hebrew sentences.
- Works at projector and laptop sizes. Phone is a nice-to-have.
- Fonts from Google Fonts: Suez One for headings, Heebo for body text.
- In RTL the next button sits on the left, the left arrow key advances, progress fills from the right, and sliders grow toward the left.
- CSS uses logical properties only. Code samples and formulas are the one deliberate LTR exception, as isolated blocks.

## 6. Python: the recipe classifier

**Input:** grams of flour, liquid, fat, sugar and egg.
**Output:** baker's percentages, a similarity score per family, the closest family and the runner-up.

**Method:**

1. Convert grams to baker's percentages, so batch size disappears.
2. Represent the recipe as a five-dimensional vector: flour, liquid, fat, sugar, egg.
3. Compute cosine similarity against four reference vectors.

**Reference vectors** (from Ruhlman's *Ratio*, confirmed by search):

| Family | Published ratio | Flour | Liquid | Fat | Sugar | Egg |
|---|---|---:|---:|---:|---:|---:|
| Bread | 5 flour : 3 water | 100 | 60 | 0 | 0 | 0 |
| Pound cake | 1:1:1:1 | 100 | 0 | 100 | 100 | 100 |
| Cookie | 3 flour : 2 fat : 1 sugar | 100 | 0 | 67 | 33 | 0 |
| Pie dough | 3 flour : 2 fat : 1 water | 100 | 33 | 67 | 0 | 0 |

**Runtime:** real Python in the browser through Pyodide, loaded from a CDN. Standard library only, so no extra packages are downloaded. The same `python/recipe_vectors.py` file is the source of truth for the page and for command-line use. A browser opened from `file://` cannot fetch a local file, so a small build step inlines it into `index.html`, and a test confirms the two match.

**Result on published recipes:** 9 of 12 correct, on a list in `python/sourced_recipes.py` fixed before any score was computed. An earlier prototype scored 10 of 12 on recipes recalled from memory, so the sourced figure replaced it. The deck shows only the sourced figure.

Flour stays in the vector, because the prototype scored 10 of 12 with it and 8 of 12 without. Caveats:

- Twelve recipes is a small sample, and the family labels are ours.
- Flour dominates every vector, so scores run high. The lab presents the ranking and the gap between first and second, and doesn't treat 0.9 as "90% sure".
- The three misses feed slide 9: brioche (cookie, by a gap of 0.006), Toll House (cake), pâte sucrée (cookie).

## 7. 3D: the five-second bake

- A dough mass rises and browns into a loaf, cake, cookie or pie, depending on Python's answer. The bake is the subject, and rotation isn't.
- Built from Three.js primitives with no image assets, which reflects the lecture's point about objects being cheaper than pixels.
- Runs on entering the slide, capped at 5.0 seconds, then holds the final state. Replay button; drag to rotate.
- The render loop stops when the slide isn't showing.
- Visual parameters are illustrative, not a physics simulation, and the slide says so.
- If WebGL is unavailable, a still image appears instead.

## 8. Repository layout

```
index.html                 the deck
README.md                  what the grader reads first
PRD.md                     this file
prompts/                   real prompts, in order
python/recipe_vectors.py   classifier, source of truth
python/sourced_recipes.py  the 12 published test recipes
python/inline_python.py    copies the classifier into index.html
python/make_charts.py      charts for the README
tests/                     automated checks
assets/                    screenshots, video, charts
```

## 9. Video

A 30 to 60 second screen capture of the deck running. A screen capture rather than an AI-generated video, following the lecture's token-economics argument: animation of objects carries the same message for far fewer resources.

## 10. Risks

| Risk | Mitigation |
|---|---|
| Pyodide takes several seconds, or fails, on `file://` or offline | Test early. Show a loading state. On failure, the lab falls back to results computed in advance by the Python script for the presets, and says so on screen |
| Grader inspects the HTML without running it | Python source is visible in `index.html`; README shows real output |
| Wrong baking facts | Team reviews everything; sources panel; the topic was chosen so that we can catch errors |
| Secrets or IDs reach the public repo | `.gitignore` covers the form. Prompts are checked before each commit. Credentials are never pasted into chat |
| Product looks "born all at once" | Stop for real team corrections at each phase. No invented history |

## 11. Acceptance tests

| ID | Test |
|---|---|
| T1 | Script opens every slide, clicks every button, sees no console errors; 10 slides |
| T2 | Keyboard and button navigation agree, including at both ends |
| T3 | Python runs in the page and matches `python/recipe_vectors.py` on all presets; doubling a recipe doesn't change the result |
| T4 | Bake animation finishes within 5.0 seconds; replay works; opens from `file://` |
| T5 | Automated: every text block computes as RTL unless explicitly isolated, right edges line up, nothing overflows, no physical left or right in the CSS. Team also reads every slide for BiDi errors |
| T6 | Every image link in the README renders on GitHub |
| T7 | Repo and any live link open in an incognito window |
| T8 | Form PDF has the template layout and the correct name; the group code is exactly 8 characters |

## 12. Out of scope

Recipe database, accounts, backend, physics simulation of baking, AI-generated video, more than about 11 slides.

## 13. Open inputs from the team

- Edit the bullets in section 2 in your own words.
- One real recipe with quantities, and the true story behind it (slide 10).
- Names of both students, in Hebrew and English (form only; ID numbers go in the form, never here).

## Decisions

Real decisions only, recorded as they happen.

| Date | Decision | Why | Who |
|---|---|---|---|
| 2026-11-07 | Topic: baking | Team's choice | Team |
| 2026-11-07 | Repo under the `morgannoa` GitHub account | Team's choice | Team |
| 2026-11-07 | Not a doughnut | It is the lecture's own example, so it would read as copied | Model proposal, team accepted |
| 2026-11-07 | Keep flour in the vector | 10 of 12 against 8 of 12 in the prototype | Model proposal, team accepted |
| 2026-11-07 | Deck in Hebrew, RTL end to end, every component aligned | Team requirement | Team |
| 2026-11-07 | Suez One and Heebo | Rendered candidates with the deck's real text and compared them | Model, on the team's instruction to use Google Fonts |
| 2026-11-07 | Report 9 of 12, not 10 of 12 | Published recipes replaced remembered ones | Model, under the rule in this PRD |
