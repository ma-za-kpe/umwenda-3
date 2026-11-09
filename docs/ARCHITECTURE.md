# Umwenda: architecture

## Information architecture

| Page | Purpose | Primary task | Features |
| --- | --- | --- | --- |
| `index` Umwenda | Orient the analyst to the worksheet and the kept records, and explain what the product is and is not. | J1 | none |
| `worksheet` Scoring worksheet | Let the analyst enter a collateral-less trader's alternative data and get a scored creditworthiness result with a written rationale and a recommended decision. | J1 | M1 Collateral-free credit scoring worksheet, M2 Trader intake form |
| `records` Kept records | Let the analyst reopen a previously scored application and compare two kept scores side by side. | J2 | M3 Keep the scored record on-device, M4 Compare two scored applications |

## Content per page

### Umwenda (`index`)

1. hero: State that Umwenda is a collateral-free credit scoring worksheet for Rwandan fintech and microfinance analysts, and that it works offline on the device with no server or account.
2. list: Link to the two working pages — the scoring worksheet (J1) and the kept records (J2, J3) — so the analyst reaches the task they are here for.
3. problem: Attribute the research context to StartupTribunal: traditional lending in Rwanda keys off tangible collateral and shuts out small traders (E1, E2), and the EMMA launch signals banks acknowledge the broken system (E3), with the caveat that the research was rejected by the StartupTribunal AI Tribunal.
4. list: List the non-goals so the analyst does not mistake the worksheet for a bank, a credit bureau, or EMMA: no live data feeds, no loan-book management, no trader-facing app, no bureau or EMMA integration.

### Scoring worksheet (`worksheet`)

1. hero: Name the page and remind the analyst this is a one-off offline scoring session for a single collateral-less trader.
2. form: Capture the trader's alternative data in one place (M2): trader name, monthly mobile-money inflow, monthly mobile-money outflow, average monthly market sales, and a short repayment history (number of past loans, number repaid on time).
3. results: Show the creditworthiness score, the written rationale, and the recommended decision (approve / decline / refer for review) computed from the entered data (M1), updating as the analyst changes the figures.
4. list: Show the state of the session: loading, empty (no data entered yet), error (the browser will not keep the record), and the kept confirmation, so the analyst always knows what happened to the score.

### Kept records (`records`)

1. hero: Name the page and remind the analyst these are the scored applications kept on this device, available offline.
2. list: List the kept scored applications (M3) by trader name and date, each with its score and decision, so the analyst can reopen one (J2) or pick two to compare (J3).
3. results: Show the reopened application's full detail — the entered data, the score, the rationale, and the decision — or, when two are selected, line them up side by side to check consistency across similar traders (M4, J3).
4. list: Show the state of the kept store: loading, empty (no records kept yet), error (the browser will not keep records), and the count of records available.

## Content model

- **scored application** (indexeddb): id, traderName, monthlyMobileMoneyInflow, monthlyMobileMoneyOutflow, averageMonthlyMarketSales, pastLoans, repaidOnTime, score, rationale, decision, createdAt. The analyst creates and keeps these records on the device (M3); they are queried by trader name and date to reopen (J2) and compare (J3), and they must outlive the session, so they live in IndexedDB, not in memory or a server.

## Decisions

### ADR-1 Store scored applications in IndexedDB

- Context: The analyst keeps scored applications on the device and must reopen or compare them later (M3, M4), so the records must survive the session and be queryable by trader name and date. The product is offline-first with no server.
- Decision: Use IndexedDB via the kit's useCollection hook, with one collection named 'applications' holding the scored application records.
- Rejected: SQLite-WASM: heavier to load and bundle, and overkill for a small number of structured records the analyst queries by name and date; the added complexity is not justified here.
- Rejected: localStorage: simpler, but it is synchronous, has a small quota, and is awkward for a growing list of records the analyst reopens over a month; IndexedDB handles the quota and async access the risk test (50 records on a low-end phone) requires.
- Consequences: Records persist across sessions and browser restarts; the analyst can keep many applications and query them by name and date. The cost is the async loading state the worksheet and records pages must show, and a quota-exceeded path the error state must surface.

### ADR-2 Compute the score client-side with a pure function

- Context: The worksheet must return a score, rationale, and decision from the entered alternative data (M1) with no server and no live feeds, and the formula is the team's own concept, not research data.
- Decision: Keep the scoring formula and the rationale/decision logic as pure functions in lib/score.ts, called by the worksheet island as the analyst changes the inputs, so the result updates in the same session.
- Rejected: A server-side scoring endpoint: rejected because the offline-first local-database rule forbids a server and the analyst works on a patchy connection.
- Rejected: A bundled reference table of thresholds: rejected because the PRD forbids live data feeds and the thresholds are the team's own concept, not StartupTribunal research, so they belong in the formula, not in static-json.
- Consequences: The score is reproducible and testable, and the rationale is generated from the same figures the analyst entered, supporting the success metric that at least 90% of kept records carry a non-empty rationale. The cost is that the formula must be reviewed by analysts before release (the trust risk), so

## Non-functional requirements

- The worksheet's score, rationale, and decision update within 100 ms of the analyst changing any input field, so the result feels immediate on a low-end phone.
- The page is usable on a 360 px-wide phone layout: the intake form and the results stack in a single column, and no horizontal scroll is needed to read the rationale.
- The product works fully offline: opening the worksheet, scoring, keeping, reopening, and comparing all succeed with no network connection, and no network call is made at any point.
- Every interactive control is reachable by keyboard and announced to screen readers: the form fields have labels, the results region uses role=status with aria-live=polite, and the kept-records list items are focusable.
- Motion is limited to a small reveal on the results block and a highlight on a changed row; when prefers-reduced-motion is set, no animation plays.
- Keeping 50 scored records on the oldest supported device and reopening the browser leaves all 50 present and readable, and a quota-exceeded condition shows the error state rather than failing silently.

## Deferred pages

This run's time budget builds 1 page. These designed pages are deferred to a later run; their features are built on the home page (`crew/plan.json`):

- `worksheet` Scoring worksheet: M1, M2
- `records` Kept records: M3, M4
