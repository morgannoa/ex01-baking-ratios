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

**Still open, and needing the team:**

- The bullets in the PRD are still the model's draft, accepted as written.
- Slide 10 has no real team recipe or story yet. The model didn't invent one.
- The team hasn't yet reviewed the finished deck.

## Note on repo access (2026-11-07)

The pasted credentials never reached the model. The team ran `gh auth login` in the terminal instead, so no credentials appear in any prompt. The model tried to create a public repo, auto mode blocked that step, and the model created a private repo and left the switch to public to the team.
