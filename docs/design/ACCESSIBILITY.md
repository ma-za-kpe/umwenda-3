# Umwenda accessibility (U6)

- Targets are at least 44px in both directions (`--target-min`).
- Focus: Every focusable control shows a 2px focus ring in the locked focus colour #0d4028 with a 2px offset, always visible on the deep canopy green surface and never removed on hover.
- Live regions: A polite live region announces save, error, change, and decision outcomes in the product's voice; the decision point also uses an assertive announcement so a committed decision is never missed.
- All interactive targets — save, resolve, ledger rows, and the offline chip — are at least 44px tall and wide.
- The decision point is the only gold element on the page; it is also labelled in text, so the decision is never carried by colour alone.
- Status chips pair a colour with a word (saved, empty, error, decided) so meaning does not depend on the palette.
- Under reduced motion, nothing moves and nothing is hidden: the load sequence renders fully and every state is visible at once.
- The ledger table keeps a caption and a data-label per row so it reads correctly when read row by row.
- Keyboard order follows the job: entry fields, then the ledger, then the decision point, then the canopy status.
- Error text is tied to the field that failed and announced, so the analyst is not left guessing what to fix.
- No content is gated behind a connection; the offline chip and canopy band state plainly that the data is on this device.
- axe (WCAG 2.1 AA) is clean on every page, at phone and desktop widths, in both themes; the frozen browser check enforces it.
- 30 of 46 measured pairs are fit for body text; the rest are listed in brand/BRAND.md with their limits.
