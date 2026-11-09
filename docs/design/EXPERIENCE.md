# Umwenda experience

## Information architecture

### `/`

Let the analyst record a collateral-less trader's standing, review the circle's ledger, and resolve one decision — all on this device, with no connection required. Primary task: Enter and save a trader's standing in place of land or a building, then review it in the Umuryango ledger.

| Section | Purpose | Layout | Components | Moment |
| --- | --- | --- | --- | --- |
| Standing entry | The analyst's first job: record who the trader is, what their standing is, and the amount the circle is weighing, in place of a parcel of land or a building. | split | StandingInput, ReasonField, StatusChip, OfflineChip | load |
| Circle ledger | Review the standings already entered on this device, in the order the circle keeps them, and open one to act on it. | table | UmuryangoLedger, LedgerRow, StandingRecord, StatusChip | change |
| Decision point | The one place the circle commits: resolve the selected standing as a yes, a no, or a hold, and record the reason. | band | DecisionPoint, ReasonField, StatusChip | decision |
| Canopy status | Quiet context: confirm the data is on this device and carry the research caveat, so the analyst knows what this tool is and is not. | band | CanopyBand, OfflineChip, StatusChip | none |

## Flows

- **Record a new standing**: Open the standing entry at the top of the page. → Enter the trader's name, their standing, and the amount the circle is weighing. → Add the reason this standing stands in for land or a building. → Save; the standing is written to this device and appears in the circle ledger. → Read the confirmation and the new row's status.
- **Review the circle ledger**: Scroll to the circle ledger to see the standings kept on this device. → Scan the rows for the standing to act on. → Open a row to read the full standing record. → Return to the ledger to choose the next standing.
- **Resolve a standing at the decision point**: Select the standing to resolve from the ledger. → Move to the decision point, the one gold place on the page. → Choose yes, no, or hold. → Record the reason for the decision. → Confirm; the standing's status changes and the circle is told.
- **Work with no connection**: Notice the offline chip in the entry panel. → Continue entering and saving standings; everything stays on this device. → Resolve decisions as usual; nothing waits on a network. → Return to the canopy status band to confirm the data is local.

## Screen states

| Screen | empty | loading | error | success |
| --- | --- | --- | --- | --- |
| Standing entry | No standing yet. Enter the trader's name, their standing, and the amount the circle is weighing. | Reading the last standing from this device… | That standing did not save. Check the name and the amount, then try again. | Standing saved to this device. It is now in the circle ledger. |
| Circle ledger | The circle ledger is empty on this device. Save a standing and it will appear here. | Opening the circle ledger from this device… | The ledger could not be read from this device. Your saved standings are still here; try again. | The circle ledger is open. Every standing here is kept on this device. |
| Decision point | Choose a standing from the ledger to resolve it here. | Bringing the standing to the decision point… | The decision did not record. Your choice is still here; try again. | Decision recorded. The standing now shows its new status in the circle ledger. |
| Canopy status | This device holds the circle's ledger. No connection is needed to enter or resolve a standing. | Checking this device's storage… | This device's storage could not be checked. Your standings are still on this device. | Everything here is on this device. Research by StartupTribunal, published with caveats. |

## Interactions

| Trigger | Response | Duration |
| --- | --- | --- |
| Page load | The entry panel, the ledger, the decision point, and the canopy band arrive one beat apart, then the empty or last standing settles into the entry fields. | `d-enter` |
| Save a standing | The save button settles, the new row enters the circle ledger, and a confirmation is announced. | `d-settle` |
| A field value changes | The affected field and its status chip shift to reflect the new value. | `d-settle` |
| Open a ledger row | The standing record reveals beside the ledger and the row is marked as selected. | `d-reveal` |
| Resolve at the decision point | The gold decision point commits, the standing's status changes, and the circle is told. | `d-burst` |
| A save or decision fails | The affected panel shakes once, the error is announced, and the entered values stay in place. | `d-settle` |
| Connection drops or returns | The offline chip shifts to show the device is working alone, and the canopy band confirms the data is local. | `d-shift` |
