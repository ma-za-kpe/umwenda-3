# Plan

## Pages

| Page | Title | Purpose | Facts |
|---|---|---|---|
| `/` | Umwenda | Orient the analyst to the worksheet and the kept records, and explain what the product is and is not. | F1, F2, F3, F4 |

## Tasks

Status as of this commit.

| Issue | Task | Status |
|---|---|---|
| [#2](https://github.com/ma-za-kpe/umwenda-3/issues/2) | Design direction: home page and shared style | In progress |

## How the work is planned

Build one feature at a time, in this order, each to its sprint contract: M1 Collateral-free credit scoring worksheet on index; M2 Trader intake form on index; M3 Keep the scored record on-device on index; M4 Compare two scored applications on index

## Experience

Umwenda (index): Orient the analyst to the worksheet and the kept records, and explain what the product is and is not.
  1. hero: State that Umwenda is a collateral-free credit scoring worksheet for Rwandan fintech and microfinance analysts, and that it works offline on the device with no server or account.
  2. list: Link to the two working pages — the scoring worksheet (J1) and the kept records (J2, J3) — so the analyst reaches the task they are here for.
  3. problem: Attribute the research context to StartupTribunal: traditional lending in Rwanda keys off tangible collateral and shuts out small traders (E1, E2), and the EMMA launch signals banks acknowledge the broken system (E3), with the caveat that the research was rejected by the StartupTribunal AI Tribunal.
  4. list: List the non-goals so the analyst does not mistake the worksheet for a bank, a credit bureau, or EMMA: no live data feeds, no loan-book management, no trader-facing app, no bureau or EMMA integration.
Scoring worksheet (worksheet): Let the analyst enter a collateral-less trader's alternative data and get a scored creditworthiness result with a written rationale and a recommended decision.
  1. hero: Name the page and remind the analyst this is a one-off offline scoring session for a single collateral-less trader.
  2. form: Capture the trader's alternative data in one place (M2): trader name, monthly mobile-money inflow, monthly mobile-money outflow, average monthly market sales, and a short repayment history (number of past loans, number repaid on time).
  3. results: Show the creditworthiness score, the written rationale, and the recommended decision (approve / decline / refer for review) computed from the entered data (M1), updating as the analyst changes the figures.
  4. list: Show the state of the session: loading, empty (no data entered yet), error (the browser will not keep the record), and the kept confirmation, so the analyst always knows what happened to the score.
Kept records (records): Let the analyst reopen a previously scored application and compare two kept scores side by side.
  1. hero: Name the page and remind the analyst these are the scored applications kept on this device, available offline.
  2. list: List the kept scored applications (M3) by trader name and date, each with its score and decision, so the analyst can reopen one (J2) or pick two to compare (J3).
  3. results: Show the reopened application's full detail — the entered data, the score, the rationale, and the decision — or, when two are selected, line them up side by side to check consistency across similar traders (M4, J3).
  4. list: Show the state of the kept store: loading, empty (no records kept yet), error (the browser will not keep records), and the count of records available.
The design system: docs/design/ and brand/; the tokens: app/tokens.css.
