# Umwenda: The analyst enters a collateral-less trader's alternative — (first release)

The approved brief, as its issue states it.

## Product

**Umwenda is a collateral-free credit scoring worksheet that turns the alternative data the analyst already holds (mobile-money flow, market sales, repayment history) into a defensible score and a keep-for-later record, in one offline session, with no server or account. It is the smallest thing that**

- For P1 Credit analyst at a Rwandan fintech or microfinance team: When a collateral-less small trader applies for a loan, I want to score their creditworthiness from their mobile-money and market-sales records so I can make a defensible approve/decline decision without land or building collateral.
- Wedge: Collateral-free credit scoring worksheet (the wedge): a browser worksheet where the analyst enters the trader's alternative data (mobile-money inflow/outflow, market sales, repayment history) and gets back a scored creditworthiness result with a written rationale, kept on the device for the next Why: It directly beats the workaround for the analyst: it turns the same documents they already hold into a consistent, defensible score and a kept record, in one offline session, with no server or account. It is the smallest thing that changes the decision E1 and E2 describe.
- Core feature: M1 Collateral-free credit scoring worksheet, for Credit analyst at a Rwandan fintech or microfinance team; works offline (indexeddb).
- The full PRD is `docs/PRD.md`.

## User stories

### R1 Score a collateral-less trader
- [ ] With monthly mobile-money inflow 800,000 RWF, outflow 600,000 RWF, average market sales 500,000 RWF, and 12 repayments (1 late), requesting a score returns a numeric creditworthiness score, a non-empty written rationale that cites the entered figures, and exactly one of approve / decline / refer for review
- [ ] With only mobile-money inflow entered and market sales and repayment history left blank, requesting a score returns either a numeric score or a refer-for-review decision whose rationale names the missing inputs
- [ ] The score, rationale, and decision are produced with the network offline and no server or account
Covers: M1 Collateral-free credit scoring worksheet (for Credit analyst at a Rwandan fintech or microfinance team)

### R2 Capture a trader's alternative data in one form
- [ ] Opening the intake form shows fields for monthly mobile-money inflow, monthly mobile-money outflow, average market sales, and repayment history, and each accepts the expected input (numeric RWF amounts, a list of repayment outcomes)
- [ ] Entering inflow 800,000, outflow 600,000, average market sales 500,000, and a 12-item repayment history keeps all values in the form when the analyst moves between fields, with no separate statements to juggle
- [ ] The entered values persist in the form after the page is reloaded while offline, so the analyst does not retype them
Covers: M2 Trader intake form (for Credit analyst at a Rwandan fintech or microfinance team)

### R3 Keep a scored application on the device
- [ ] After scoring an application, keeping it stores the score, rationale, and decision in the device's local database (indexeddb)
- [ ] Closing the browser and reopening it with no network still lists the kept record with the identical score, rationale, and decision
- [ ] Keeping 50 scored records on the team's oldest supported device, then closing and reopening the browser, leaves all 50 present and readable
- [ ] When the local store is at its quota limit, keeping one more record shows a quota-exceeded message instead of failing silently
Covers: M3 Keep the scored record on-device (for Credit analyst at a Rwandan fintech or microfinance team)

### R4 Compare two kept scores side by side
- [ ] With two kept scored applications, selecting both in the compare view lays them out side by side showing each record's score, rationale, and decision
- [ ] The compare view works offline with no network, reading both records from the device's local database
Covers: M4 Compare two scored applications (for Credit analyst at a Rwandan fintech or microfinance team)

### R5 Out of scope (non-goals)
- [ ] No live mobile-money or market data feeds: figures are entered by the analyst from the trader's documents; nothing is pulled from a bank or mobile-money operator (S5)
- [ ] No portfolio or loan-book management: the product scores individual applications only; it does not track disbursed loans, repayments over time, or team-wide dashboards (S6)
- [ ] No consumer-facing trader app or account: only the analyst uses the product; the trader does not (S7)
- [ ] No integration with a credit bureau or EMMA: the worksheet stands alone on the device and reads from or writes to no external credit system (S8)
Covers: S5, S6, S7, S8

## Out of scope

- No live mobile-money or market data feeds: the analyst enters the figures from the documents the trader brought; nothing is pulled from a bank or mobile-money operator.
- No portfolio or loan-book management: the product scores individual applications; it does not track disbursed loans, repayments over time, or team-wide dashboards.
- No consumer-facing trader app or account: the trader does not use the product; only the analyst does.
- No integration with a credit bureau or EMMA: the worksheet stands alone on the device and does not read from or write to any external credit system.

## Journeys

- **J1** (visitor) Score a collateral-less trader's creditworthiness from mobile-money and market-sales data and reach a defensible approve/decline decision. Observed: facts-shown, phone-layout, review.
- **J2** (owner) Reopen a previously scored application and compare it to the same trader's next application. Observed: facts-shown, review.
- **J3** (owner) Line up two kept scored applications side by side to check consistency across similar traders before a manager review. Observed: facts-shown, review.

## Facts the site shows

- `F1`: Who it is for: Fintech and analytics teams and customers in Rwanda
- `F2`: StartupTribunal research reports: Traditional lending in Rwanda focuses almost entirely on tangible assets like land or buildings, shutting out the majority of citizens and small traders who lack formal collateral. This forces creditworthy people into high-interest informal lenders or blocks them from accessing capital needed for business growth, emergencies, or home improvement. The launch of EMMA signals that banks themselves acknowledge this broken system.
- `F3`: Research status: rejected by the StartupTribunal AI Tribunal, published with caveats.
- `F4`: Research by StartupTribunal: https://startuptribunal.com/catalog/rwandans-without-collateral-denied-bank-loans

## Assumptions

- A public repository and a public site on GitHub Pages; no server or database.
- The frozen tests under `tests/` are the acceptance contract; changing them needs the owner's approval.
- Facts appear exactly as the brief gives them.
