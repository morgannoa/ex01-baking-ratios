# Phase 1: Planning

Tool: Claude Code (Opus 5.5), terminal.

## Prompt 1 (2026-11-07)

> look at the attached files, they are files we got from our lecturer, here are all of the lecturer's requirements:
>
> `[Moodle assignment text omitted: the lecturer's course material]`
>
> , please read all the files, all the requirements, and let me know if you understood the assignment and prepare a short and concise plan for executing the requirements from end to end, including all the animations, 3d, etc etc.

**Model response (summary):** read the two PDFs and the Word form and checked which tools the machine has. Confirmed the assignment, then listed traps:

- the conflict between the 11/11 and 12/11 deadlines
- the video, which appears only in the Moodle text
- the 5-second limit on the 3D animation
- no Word or LibreOffice on this machine to produce the form PDF

Proposed a seven-phase plan and asked five questions: topic, bullets, language, team details, repo access.

## Prompt 2 (2026-11-07)

> answer the questions below, we would like to have a presenation about baking (cakes, breads, stuff like that). Provie answers to all of the questions provided. we will need it to be on morgannoa github, here it is: [Pasted text #2 +71 lines] , these are the repo
> credentials. Worst case scenario we will upload it ourselves. Now, regarding 1- the topic is baking.
> Cakes, breads, cookies, pies, etc etc.

The marker `[Pasted text #2 +71 lines]` is what reached the model. The pasted credentials did not arrive, so none are in this log.

**Model response (summary):**

- Re-read the homework PDF and the lecture summary before writing the PRD.
- Noticed that the lecture's 3D example is a doughnut, so a baking deck should not use one.
- Proposed treating a recipe as a vector of baker's percentages and classifying it with cosine similarity from lecture 3.
- Tested that idea with a throwaway prototype: 10 of 12 test recipes correct with flour in the vector, 8 of 12 without. The test recipes came from the model's memory, so this shows feasibility only.
- Searched for the published ratios and confirmed them against Ruhlman's *Ratio*. The search also caught a model error: the prototype used 65% water for bread, but 5:3 is 60%. Corrected and re-run, with the same score.
- Drafted the team bullets at the team's request and wrote `PRD.md` v0.1.
- Stopped for team review.
