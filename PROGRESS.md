# Progress: Umwenda

As of this commit. Trusted code writes this file from the job's journal; every role reads it first (`AGENTS.md`, Start here).

0 of 4 features pass.

## Features

| Feature | Title | Page | Status | Passes |
| --- | --- | --- | --- | --- |
| M1 | Collateral-free credit scoring worksheet | `index` | in-progress | no |
| M2 | Trader intake form | `index` | in-progress | no |
| M3 | Keep the scored record on-device | `index` | in-progress | no |
| M4 | Compare two scored applications | `index` | in-progress | no |

## Current sprint

Sprint contract: Design direction: home page and shared style

Done means, for each feature:

- [ ] M1 Collateral-free credit scoring worksheet: The analyst enters a collateral-less trader's alternative data — monthly mobile-money inflow and outflow, average market sales, and a short repayment history — and the worksheet returns a creditworthiness score with a written rationale and a recommended decision (approve / decline / refer for review (on `index`, working offline)
- [ ] M2 Trader intake form: The analyst captures the trader's mobile-money flow, market sales and repayment history in one place, instead of juggling separate statements. (on `index`, working offline)
- [ ] M3 Keep the scored record on-device: The analyst keeps each scored application locally and can reopen it later or compare it to the same trader's next application, instead of losing the note when the session ends. (on `index`, working offline)
- [ ] M4 Compare two scored applications: The analyst lines up two kept scores side by side to check consistency across similar traders before a manager review. (on `index`, working offline)

Checked by the implementer, on the exact head:

- `npm run build`
- `python tests/site_view.py && python -m unittest discover -s tests`
- `node tests/browser/qa.mjs`

Judged by the evaluator, on the rendered product: every criterion (design, originality, depth, craft, functionality) scores at least 7 of 10, and so do its 7 hidden rubric categories. Below that the task holds; it never merges.

## Recent commits

- `1c2b8fadcb2b` on `feature/issue-2-home`: docs: product requirements, architecture and design system
- `d5340be05aa3` on `feature/issue-2-home`: docs: brief, plan, decisions, handoff and run record
