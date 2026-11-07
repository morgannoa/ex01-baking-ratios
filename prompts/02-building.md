# Phase 2 onward: Building the deck

Tool: Claude Code (Opus 5.5), terminal.

## Prompt 3 (2026-11-07)

> i accept the PRD , work and create it. It should be in hebrew. RTL aligned from end to end, make sure that every component is aligned correctly. Regarding a font, use googlefonts to find a good looking hebrew font.

**Model response (summary):**

- Treated "every component aligned correctly" as a testable requirement, so RTL alignment gets automated browser checks as well as a visual review.
- Rendered eight Google Fonts headline candidates and four body candidates with the deck's real text, then chose Suez One for headings and Heebo for body text.
- Fixed a test set of 12 published recipes before computing any result, as the PRD required. The score fell from 10 of 12 (recipes recalled from memory) to 9 of 12 (published recipes), and the lower figure is the one the deck uses.
