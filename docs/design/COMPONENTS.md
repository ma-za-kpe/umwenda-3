# Umwenda components (U4, U5)

## StandingInput

The analyst's primary entry: records a collateral-less trader's standing (name, trade, monthly turnover, umuryango membership) in place of a parcel of land or a

Anatomy: trader name field, trade field, monthly turnover field (RWF), umuryango membership field, save control.

| State | Treatment |
| --- | --- |
| default | Quiet surface #e2efe6 card on paper #eef6f0; labels in muted #51645b; fields empty with a thin line #c3d8cb underline; save control disabled. |
| hover | Field underline deepens to accent #0d4028; no lift, no shadow, so the surface stays unshowy. |
| focus | Focused field shows a 2px focus #0d4028 ring and a 44px minimum target; the rest of the card stays still. |
| active | While typing, the field underline is solid accent #0d4028 and the save control becomes enabled. |
| disabled | All fields dim to muted #51645b at reduced opacity; save control greyed; used when the record is locked after a decision. |
| loading | Fields show a skeleton shimmer in surface #e2efe6 while the local record loads from IndexedDB; save control shows a spinner. |
| empty | No trader entered: a single standing icon in muted #51645b and the line 'Enter a trader's standing to begin the circle.' in the brand's candid voice. |
| error | Invalid turnover or missing membership: field underline turns danger #a83325, an inline message in danger #a83325 names the fix, and the error moment plays at d |
| success | Standing saved: a brief success #1f6d42 check on the save control and the save moment plays at d-settle 220ms; the record becomes the selected StandingRecord. |
| selected | The active trader's standing is loaded into the fields and a thin accent #0d4028 left rule marks the card as the one being worked on. |
| offline | A small offline chip in warning #7a4b00 reads 'On this device'; all entry still works because data lives in IndexedDB, and the save moment confirms locally. |

## StandingRecord

The saved trader's standing shown as the thing the circle is judging, replacing the parcel of land or building a bank would have asked for.

Anatomy: trader name and trade line, monthly turnover figure (mono), umuryango membership count, standing status chip, select control.

| State | Treatment |
| --- | --- |
| default | Surface #e2efe6 row with the name in ink #08231a, turnover in jetbrains-mono, and a neutral status chip in muted #51645b. |
| hover | Row background shifts to surface #e2efe6 one step darker; the select control gains a focus-ready outline. |
| focus | Keyboard focus draws a 2px focus #0d4028 ring around the row; target is at least 44px tall. |
| active | Pressed state darkens the row and the select control reads 'Open' in accent #0d4028. |
| disabled | Row dims to muted #51645b and cannot be selected; used for a standing already decided and locked. |
| loading | Skeleton rows in surface #e2efe6 while the local ledger loads; the change moment plays at d-enter 340ms as rows settle. |
| empty | No standing yet: a standing icon in muted #51645b and 'No standing entered. The circle is empty.' in the brand's direct voice. |
| error | If the local record fails to read, a danger #a83325 line reads 'Could not read this standing on this device.' and the error moment plays at d-settle 220ms. |
| success | After a fresh save, the row flashes a success #1f6d42 left rule for one beat via the save moment at d-settle 220ms. |
| selected | The working standing carries a solid accent #0d4028 left rule and its status chip is filled; this is the one the decision point acts on. |
| offline | An offline chip in warning #7a4b00 sits at the row's edge; the standing is fully readable and editable from IndexedDB. |

## UmuryangoLedger

The cooperative credit-circle ledger: the trader's standing read against the circle's members and amounts, the core record the analyst reviews before deciding.

Anatomy: ledger header (circle name, member count), member rows (name, contribution, standing), amount column (RWF, mono), canopy band behind the ledger, totals footer.

| State | Treatment |
| --- | --- |
| default | A composed table on the desktop grid; member rows in ink #08231a on paper #eef6f0, amounts in jetbrains-mono, thin line #c3d8cb rules; the canopy band is the |
| hover | The hovered member row tints to surface #e2efe6; the amount column stays still so the eye reads the figure, not the motion. |
| focus | A focused row shows a 2px focus #0d4028 ring; the canopy band does not move, keeping the metaphor quiet. |
| active | Pressing a member row opens its detail inline; the change moment plays at d-shift 480ms as the row expands. |
| disabled | When the circle is locked after a decision, rows dim to muted #51645b and the totals footer reads 'Circle closed.' in muted #51645b. |
| loading | Member rows arrive one by one via the load moment, a beat apart at d-enter 340ms, then the totals footer reveals at d-reveal 640ms. |
| empty | No members yet: a members icon in muted #51645b and 'The circle has no members yet. Add a standing to open it.' in the candid voice. |
| error | If a row's data is corrupt, that row shows a danger #a83325 marker and the error moment plays at d-settle 220ms; other rows stay readable. |
| success | When a contribution is recorded, the affected amount ticks up in success #1f6d42 and the save moment plays at d-settle 220ms. |
| selected | The trader under review is highlighted with an accent #0d4028 row rule so the analyst sees exactly whose standing the circle is weighing. |
| offline | An offline chip in warning #7a4b00 reads 'Ledger on this device'; the full ledger is available from IndexedDB with no connection. |

## DecisionPoint

The single decision the analyst makes on the selected trader's standing, and the one place in the product where the sun-gold accent is spent.

Anatomy: decision prompt (whose standing, what is asked), approve control (sun-gold), decline control (quiet), reason field, decision status line.

| State | Treatment |
| --- | --- |
| default | A quiet band on surface #e2efe6; the approve control is the only sun-gold element, the decline control is muted #51645b, and the reason field is empty. |
| hover | The approve control deepens its sun-gold fill slightly; the decline control gains a line #c3d8cb outline; no other surface reacts. |
| focus | Keyboard focus draws a 2px focus #0d4028 ring on whichever control is focused; both controls are at least 44px targets. |
| active | Pressing approve or decline commits the decision; the decision moment plays at d-burst 900ms and the burst moment releases the sun-gold accent once. |
| disabled | No standing selected: both controls dim to muted #51645b and the prompt reads 'Select a standing to decide.' in muted #51645b. |
| loading | While the decision writes to IndexedDB, the pressed control shows a spinner and the decision status line reads 'Recording on this device…' in muted #51645b. |
| empty | Same as disabled when nothing is selected: the prompt invites the analyst to choose a standing before the circle can act. |
| error | If the write fails, the decision status line turns danger #a83325 with 'The decision was not saved on this device.' and the error moment plays at d-settle 220ms |
| success | On a saved decision, the status line reads the outcome in success #1f6d42 (approve) or muted #51645b (decline) and the save moment plays at d-settle 220ms. |
| selected | When a standing is selected, the prompt fills with that trader's name and trade, and the approve control lights to full sun-gold, ready for the one decision. |
| offline | An offline chip in warning #7a4b00 reads 'Decision on this device'; the decision is fully usable and stored locally with no connection. |

## StatusChip

The small label that names a standing's outcome so the analyst can scan the circle at a glance.

Anatomy: status word, identity icon, colour role fill.

| State | Treatment |
| --- | --- |
| default | A quiet pill in surface #e2efe6 with the status word in ink #08231a and its identity icon; no fill until the standing has an outcome. |
| hover | The pill's line #c3d8cb outline deepens to accent #0d4028; the word and icon stay still. |
| focus | When the chip is interactive (e.g. filters by status), a 2px focus #0d4028 ring appears; target is at least 44px. |
| active | Pressed, the pill fills with its colour role and the word inverts to accentInk #eef6f0 for contrast. |
| disabled | The chip dims to muted #51645b and is not selectable; used for a status that does not apply to the current view. |
| loading | A skeleton pill in surface #e2efe6 while the standing's outcome loads from IndexedDB. |
| empty | No outcome yet: the chip reads 'Pending' in muted #51645b with the standing icon, signalling the circle has not decided. |
| error | If the outcome cannot be read, the chip shows the standing icon in danger #a83325 and the word 'Unread' in danger #a83325. |
| success | When the outcome is set, the chip fills with its colour role (e.g. success #1f6d42 for Approved) and the word inverts to accentInk #eef6f0. |
| selected | The chip for the working standing carries a solid accent #0d4028 ring so it reads as the one under review. |
| offline | An offline chip variant in warning #7a4b00 reads 'On device' with the canopy icon, marking data held locally. |

## CanopyBand

The one place the forest-canopy metaphor is spent: a quiet band behind the ledger that grounds the circle under the canopy the cooperative sits in.

Anatomy: canopy pattern (deep canopy green), circle name line, member count (mono), offline indicator slot.

| State | Treatment |
| --- | --- |
| default | A deep canopy green accent #0d4028 band with the canopy pattern at low contrast; the circle name in accentInk #eef6f0 and member count in jetbrains-mono. |
| hover | No change; the band is not interactive, so it stays still to keep the metaphor quiet. |
| focus | Not focusable; the band carries no controls, so no focus ring is drawn. |
| active | Not applicable; the band has no pressed state. |
| disabled | When the circle is closed, the band dims toward ink #08231a and the circle name reads 'Circle closed.' in muted #51645b. |
| loading | The canopy pattern fades in via the load moment at d-reveal 640ms while the circle name and count settle at d-enter 340ms. |
| empty | No circle yet: the band shows the canopy icon in accentInk #eef6f0 and 'No circle open.' in accentInk #eef6f0 at reduced weight. |
| error | If the circle cannot be read, a danger #a83325 line reads 'Could not open the circle on this device.' and the error moment plays at d-settle 220ms. |
| success | When the circle is confirmed open, the member count ticks in success #1f6d42 and the save moment plays at d-settle 220ms. |
| selected | Not applicable; the band is a single context, not a selectable item. |
| offline | The offline indicator slot shows a warning #7a4b00 chip reading 'On this device' with the canopy icon. |

## OfflineChip

The always-available marker that the product is offline first and its data lives on the device, so the analyst never waits on a connection.

Anatomy: offline word, canopy icon, colour role fill.

| State | Treatment |
| --- | --- |
| default | A small pill in warning #7a4b00 with the canopy icon and the word 'On this device' in accentInk #eef6f0. |
| hover | The pill's fill deepens one step; the word and icon stay still. |
| focus | When tappable (e.g. to open local storage info), a 2px focus #0d4028 ring appears; target is at least 44px. |
| active | Pressed, the pill fills solid warning #7a4b00 and the word inverts to accentInk #eef6f0. |
| disabled | Dimmed to muted #51645b when local storage is unavailable; the word reads 'No local storage.' in muted #51645b. |
| loading | A skeleton pill in surface #e2efe6 while local storage is checked on first load. |
| empty | Not applicable; the chip is always present to state the offline-first posture. |
| error | If local storage fails, the chip turns danger #a83325 and reads 'Local storage unavailable.' with the error moment at d-settle 220ms. |
| success | When local storage is confirmed, the chip briefly shows a success #1f6d42 check before settling back to warning #7a4b00. |
| selected | Not applicable; the chip is a status, not a selectable item. |
| offline | This is the chip's native state: it reads 'On this device' in warning #7a4b00 and confirms all data is held in IndexedDB. |

## LedgerRow

A single member's line in the umuryango ledger: their name, contribution, and standing, the unit the analyst reads and, if needed, opens.

Anatomy: member name, contribution amount (RWF, mono), standing status chip, expand control.

| State | Treatment |
| --- | --- |
| default | A row in ink #08231a on paper #eef6f0 with a thin line #c3d8cb rule; the contribution in jetbrains-mono and the status chip in its colour role. |
| hover | The row tints to surface #e2efe6; the expand control gains a focus-ready outline. |
| focus | Keyboard focus draws a 2px focus #0d4028 ring around the row; the row is at least 44px tall. |
| active | Pressed, the row expands to show the member's detail; the change moment plays at d-shift 480ms. |
| disabled | The row dims to muted #51645b and cannot expand; used when the circle is closed. |
| loading | A skeleton row in surface #e2efe6 while the member's data loads from IndexedDB. |
| empty | Not applicable at the row level; an empty ledger is handled by the UmuryangoLedger's empty state. |
| error | If the row's data is corrupt, a danger #a83325 marker appears and the error moment plays at d-settle 220ms. |
| success | When a contribution is recorded, the amount ticks up in success #1f6d42 and the save moment plays at d-settle 220ms. |
| selected | The trader under review carries an accent #0d4028 left rule so the analyst sees whose standing the circle is weighing. |
| offline | An offline chip in warning #7a4b00 at the row's edge; the row is fully readable and editable from IndexedDB. |

## ReasonField

The analyst's short note for why a standing was approved or declined, kept with the decision so the circle's reasoning is on the record.

Anatomy: reason label, reason text area, character count (mono), clear control.

| State | Treatment |
| --- | --- |
| default | A quiet text area on surface #e2efe6 with the label in muted #51645b and an empty character count in jetbrains-mono. |
| hover | The text area's line #c3d8cb underline deepens to accent #0d4028. |
| focus | A 2px focus #0d4028 ring surrounds the text area; the target is at least 44px. |
| active | While typing, the underline is solid accent #0d4028 and the character count updates in jetbrains-mono. |
| disabled | The text area dims to muted #51645b and is not editable; used after a decision is locked. |
| loading | A skeleton text area in surface #e2efe6 while a saved reason loads from IndexedDB. |
| empty | No reason yet: the field shows a muted #51645b placeholder 'Add a reason (optional).' in the candid voice. |
| error | If the reason exceeds the limit, the underline turns danger #a83325 and an inline message in danger #a83325 names the limit; the error moment plays at d-settle |
| success | When the reason is saved with the decision, a brief success #1f6d42 check appears and the save moment plays at d-settle 220ms. |
| selected | Not applicable; the field is not a selectable item. |
| offline | An offline chip in warning #7a4b00 reads 'On this device'; the reason is stored locally with no connection. |

## Status

Every status is a word, an icon and a colour, never colour alone.

| Status | Word | Icon | Colour role |
| --- | --- | --- | --- |
| Pending | Pending | `standing` | `--color-muted` |
| Approved | Approved | `decision` | `--color-success` |
| Declined | Declined | `decision` | `--color-danger` |
| Under Review | Under Review | `ledger` | `--color-warning` |
| On Device | On Device | `canopy` | `--color-accent` |
