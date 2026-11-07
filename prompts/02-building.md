# Phase 2 onward: Building the deck

Tool: Claude Code (Opus 5.5), terminal.

## Prompt 3 (2026-11-07)

> i accept the PRD , work and create it. It should be in hebrew. RTL aligned from end to end, make sure that every component is aligned correctly. Regarding a font, use googlefonts to find a good looking hebrew font.

**Model response (summary):**

- Treated "every component aligned correctly" as a testable requirement, so RTL alignment gets automated browser checks as well as a visual review.
- Rendered eight Google Fonts headline candidates and four body candidates with the deck's real text, then chose Suez One for headings and Heebo for body text.
- Fixed a test set of 12 published recipes before computing any result, as the PRD required. The score fell from 10 of 12 (recipes recalled from memory) to 9 of 12 (published recipes), and the lower figure is the one the deck uses.
- Built the deck in stages, pushing after each: first the slides and RTL audit, then the 3D oven and Python lab, then the README, video and final corrections.

**Mistakes made and corrected during this phase, all by the model unless noted:**

- Told the team that brioche "loses by just 0.006". That gap is between cookie and pie, and bread came last. Caught while writing slide 9, corrected on the slide, and a test now holds every claim on that slide.
- Used 65% water for bread in the first prototype, against the published 60%.
- Used a sifted flour weight for Toll House. The slide's claim of "more sugar than flour" depended on it. Reading the source showed it concludes 360 g, so the data and the claim both changed. The recipe is a miss either way.
- Picked five warm ingredient colors, two of which were nearly identical. The first color check missed this because it compared only the listed order. Comparing the pairs that actually touch caught it.
- A test run looked clean while the audit had actually stopped early, because the output filter hid the crash. Runs now count only if the final summary prints.

## Note on repo access (2026-11-07)

The pasted credentials never reached the model. The team ran `gh auth login` in the terminal instead, so no credentials appear in any prompt. The model tried to create a public repo, auto mode blocked that step, and the model created a private repo and left the switch to public to the team.

The team then ran `gh repo edit` itself to make the repo public. A check in a fresh browser with no login confirmed that the page opens and all README images load.

## Prompt 4 (2026-11-07)

> open it

**Model response (summary):** opened `index.html` in the default browser.

## Prompt 5 (2026-11-07)

> ok its good, now what?

**Model response (summary):** found the repo was still private, and listed the remaining steps: go public, supply a real recipe and story, rewrite the bullets, give the students' names, then finish the form.

## Prompt 6 (2026-11-07)

> regarding 2 - do it yourself. regarding 3 - `[students' names omitted from this public log]`

**Model response (summary):**

- Chose a published Friday challah for slide 10, because it's familiar to this audience and shows something real: it has sugar, oil and yolks like a cake, and its ratio stays bread.
- Did not invent a family story or present one as true. That part of the brief is still the model's work, not the team's own experience, and this log says so.
- Kept the bullets as the model's draft, on the team's instruction.
- Filled the Moodle form outside the repo, leaving the ID numbers and self grade for the team.

## Prompt 7 (2026-11-07)

> dont say 85, say 95, and do everything for me, fill every form, every question ask yourelf, every edit. i will add id later on my own.

**Model response (summary):**

- Set the self grade to 95 in the form, replacing its own suggestion of 85.
- Tried to turn on GitHub Pages. Auto mode blocked it as a new public surface, so it's left for the team to enable. The deck doesn't depend on it.
- Installed LibreOffice to check how the form renders and to give the team a local way to export the PDF after adding the ID numbers.

## Prompt 8 (2026-11-07)

> push to github and make all the readme requirements he asked for. re-read all assignments before.

**Model response (summary):** re-read the homework PDF, the full Moodle text and the lecture's README section, and compared them with the README line by line. It found gaps: no frames from the video, no explicit goal, no work specification, only 4 of 10 slides, no guidance on what to test, no architecture view, no push history and no concepts list. It rebuilt the README to cover each one.

## Prompt 9 (2026-11-07)

> then, create an artifact explaining every requirement and how we met it.

**Model response (summary):** after the push, built a page listing every requirement from the lecturer's sources, how it was met, and what's still open.

## Prompt 10 (2026-11-07)

> write it in hebrew, the artifact

**Model response (summary):** rewrote the requirements page in Hebrew, right to left, and checked that every text block computes as RTL with English terms isolated.

