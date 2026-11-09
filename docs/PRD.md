# Umwenda: product requirements

Umwenda is a collateral-free credit scoring worksheet that turns the alternative data the analyst already holds (mobile-money flow, market sales, repayment history) into a defensible score and a keep-for-later record, in one offline session, with no server or account. It is the smallest thing that

## Problem and evidence

Rwandan lending keys off tangible collateral, which shuts out small traders and pushes creditworthy ones to high-interest informal lenders (E1, E2). Banks' own EMMA launch signals the system is broken (E3). The credit analyst at a Rwandan fintech or microfinance team must decide on a trader who has no land or building to pledge, with no reliable internet and no access to a central credit bureau, using only the documents the trader brought (mobile-money statements, market sales records, past repayments). Today they either decline the trader (who then goes to a high-interest informal lender) or escalate to a manager for a second opinion, with nothing kept for the next application.

- Traditional lending in Rwanda focuses almost entirely on tangible assets like land or buildings, shutting out the majority of citizens and small traders who lack formal collateral. (StartupTribunal, E1)
- This forces creditworthy people into high-interest informal lenders or blocks them from accessing capital needed for business growth, emergencies, or home improvement. (StartupTribunal, E2)
- The launch of EMMA signals that banks themselves acknowledge this broken system. (StartupTribunal, E3)

Who is hurt: Credit analysts at Rwandan fintech and microfinance teams who must make defensible approve/decline decisions on collateral-less small traders without reliable internet or a central credit bureau.

## Personas and jobs to be done

### P1 Credit analyst at a Rwandan fintech or microfinance team

Works from a laptop or phone in a city office or at a market outreach point, often on a patchy connection, reviewing a small trader's loan application that has no land title or building to pledge.

- Job to be done: When a collateral-less small trader applies for a loan, I want to score their creditworthiness from their mobile-money and market-sales records so I can make a defensible approve/decline decision without land or building collateral.
- Today's workaround: Today the analyst eyeballs the mobile-money statements and sales lists, writes a gut-feel note, and either declines the trader (who then goes to a high-interest informal lender) or escalates to a manager for a second opinion, with nothing kept for the next application.

## Alternatives today

- Full alternative-data underwriting suite: a multi-module platform ingesting live mobile-money and market feeds, portfolio dashboards, and decision workflows for the whole lending team. Rejected because it needs live data feeds, a server and accounts, which the offline-first local-database rule forb
- Consumer-facing loan self-assessment app for traders: an app the trader themselves uses to check their own creditworthiness and apply for a loan. Rejected because the decision belongs to the analyst, not the trader; a trader cannot reliably self-score, and an app aimed at the trader would need a
- Collateral-free credit scoring worksheet (the wedge): a browser worksheet where the analyst enters the trader's alternative data (mobile-money inflow/outflow, market sales, repayment history) and gets back a scored creditworthiness result with a written rationale, kept on the device for the next

## Value proposition

Umwenda is a collateral-free credit scoring worksheet that turns the alternative data the analyst already holds (mobile-money flow, market sales, repayment history) into a defensible score and a keep-for-later record, in one offline session, with no server or account. It is the smallest thing that

## Solution options and wedge

- O1: Collateral-free credit scoring worksheet (the wedge): a browser worksheet where the analyst enters the trader's alternative data (mobile-money inflow/outflow, market sales, repayment history) and gets back a scored creditworthiness result with a written rationale, kept on the device for the next
- O2: Full alternative-data underwriting suite: a multi-module platform ingesting live mobile-money and market feeds, portfolio dashboards, and decision workflows for the whole lending team. Rejected because it needs live data feeds, a server and accounts, which the offline-first local-database rule forb
- O3: Consumer-facing loan self-assessment app for traders: an app the trader themselves uses to check their own creditworthiness and apply for a loan. Rejected because the decision belongs to the analyst, not the trader; a trader cannot reliably self-score, and an app aimed at the trader would need a

Wedge: O1, Collateral-free credit scoring worksheet (the wedge): a browser worksheet where the analyst enters the trader's alternative data (mobile-money inflow/outflow, market sales, repayment history) and gets back a scored creditworthiness result with a written rationale, kept on the device for the next Why: It directly beats the workaround for the analyst: it turns the same documents they already hold into a consistent, defensible score and a kept record, in one offline session, with no server or account. It is the smallest thing that changes the decision E1 and E2 describe.

## Core feature

M1 Collateral-free credit scoring worksheet, for Credit analyst at a Rwandan fintech or microfinance team: The analyst enters a collateral-less trader's alternative data — monthly mobile-money inflow and outflow, average market sales, and a short repayment history — and the worksheet returns a creditworthiness score with a written rationale and a recommended decision (approve / decline / refer for review

- Primary action: The analyst enters a collateral-less trader's alternative —
- Offline, on the device (indexeddb): true

## MVP scope

- M1 Collateral-free credit scoring worksheet (P1): The analyst enters a collateral-less trader's alternative data — monthly mobile-money inflow and outflow, average market sales, and a short repayment history — and the worksheet returns a creditworthiness score with a written rationale and a recommended decision (approve / decline / refer for review
- M2 Trader intake form (P1): The analyst captures the trader's mobile-money flow, market sales and repayment history in one place, instead of juggling separate statements.
- M3 Keep the scored record on-device (P1): The analyst keeps each scored application locally and can reopen it later or compare it to the same trader's next application, instead of losing the note when the session ends.
- M4 Compare two scored applications (P1): The analyst lines up two kept scores side by side to check consistency across similar traders before a manager review.

## Non-goals

- No live mobile-money or market data feeds: the analyst enters the figures from the documents the trader brought; nothing is pulled from a bank or mobile-money operator.
- No portfolio or loan-book management: the product scores individual applications; it does not track disbursed loans, repayments over time, or team-wide dashboards.
- No consumer-facing trader app or account: the trader does not use the product; only the analyst does.
- No integration with a credit bureau or EMMA: the worksheet stands alone on the device and does not read from or write to any external credit system.

## Success metrics

- Share of scored applications with a defensible written rationale: At least 90% of applications the analyst scores in the worksheet carry a generated rationale the analyst keeps with the decision. (measured by Count of kept scored records that include a non-empty rationale field, divided by total kept scored records, read from the on-device store.)
- Analyst decision time per collateral-less application: Median time from opening the worksheet to a kept score of under 10 minutes, versus the analyst's current workaround. (measured by Timestamp of first data entry versus timestamp of the keep action, recorded per application in the on-device store; median across the last 20 kept applications.)
- Records still usable a month later: At least 80% of scored records kept are reopened or compared within 30 days, showing the kept record outlives the session. (measured by Count of kept records with a reopen or compare event within 30 days of the keep timestamp, divided by total kept records in that window, from the on-device store.)

## Risks

- The scoring formula is not trusted by the analyst Test: Before release, have 3-5 analysts score the same 5 sample applications with the worksheet and against their current method; check whether they would act on the worksheet's recommendation and whether the rationale reads as defensible to them.
- Alternative data entered is too sparse to score a real trader Test: Run the worksheet on 10 real (anonymised) application files the team has; record how many produce a score versus how many fall back to 'refer for review', and whether the sparse-data path is acceptable.
- The offline, on-device store loses records on a low-end phone Test: On the team's oldest supported device, keep 50 scored records, close and reopen the browser, and verify all 50 are still present and readable; check the quota-exceeded message appears if the store is full.
- The product is mistaken for a bank or EMMA system Test: Have 5 people outside the team read the product for two minutes and ask what they think it is and who it is for; verify they identify it as an analyst's scoring worksheet, not a bank or credit bureau.

## Assumptions

- The analyst already holds mobile-money and market-sales documents for the trader at review time Check: Interview 3-5 Rwandan fintech/microfinance analysts and confirm what documents they actually have in hand when scoring a collateral-less trader; adjust the intake fields to match.
- A simple score plus rationale is enough for the analyst to defend a decision Check: Pilot the worksheet with 2-3 analysts on live applications for two weeks and ask whether the output changed or supported their final decision; capture their edits to the rationale.
- The trader's data is entered manually and accurately enough to score Check: Compare the worksheet's score on 10 applications where the analyst also recorded their own manual assessment; measure agreement and note where manual entry introduced error.

Research claims are the source's and are attributed; every feature is the team's own concept.
