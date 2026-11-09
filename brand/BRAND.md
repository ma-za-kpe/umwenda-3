# Umwenda brand

Theme: **Umuryango Credit Circle**. The cooperative (umuryango) credit-circle ledger and the Rwandan forest canopy the cooperative sits under. The analyst sits in the circle, entering a trader's standing in place of a parcel of land or a building.

Boldness, spent in one place: The identity's colour and the canopy metaphor: a deep canopy green as the dominant surface and a single sun-gold accent for the one decision point. Every other surface stays quiet so that the green-to

## Essence (B1)

| Tagline | Promise | Personality |
| --- | --- | --- |
| Your standing, entered here, stands for the land. | Umwenda lets a Rwandan fintech analyst score a collateral-less trader on what the person can show, and let a trader see their standing without a parcel to pledge. | candid, steady, grounded, unshowy, direct |

| It is | It is not |
| --- | --- |
| A working tool where an analyst enters a trader's standing | A marketing site that promises approval |
| A ledger that reads like a circle, not a dashboard | A dashboard of charts that flatters the analyst |
| Honest about what the data shows and does not | A loan broker or a lender |
| Built for the analyst's hands and the trader's patience | A product that hides what the research could not prove |

The decision, with the directions rejected, is in [DECISION.md](DECISION.md).

## Colour (B4)

24 primitives and 11 semantic roles in two themes; use the roles, never a primitive directly.

| Primitive | Value |
| --- | --- |
| `canopy` | #12422a |
| `canopy-deep` | #0c3320 |
| `canopy-soft` | #1c5236 |
| `paper` | #eef6f0 |
| `paper-soft` | #e2efe6 |
| `paper-deep` | #d6e8dc |
| `ink` | #08231a |
| `ink-soft` | #51645b |
| `ink-dark` | #eef6f0 |
| `ink-soft-dark` | #9db8a9 |
| `line` | #c3d8cb |
| `line-dark` | #2c5a41 |
| `accent` | #0d4028 |
| `accent-dark` | #e7c04e |
| `accent-ink` | #eef6f0 |
| `accent-ink-dark` | #12301f |
| `focus` | #0d4028 |
| `focus-dark` | #f1cf6a |
| `success` | #1f6d42 |
| `success-dark` | #86d39c |
| `warning` | #7a4b00 |
| `warning-dark` | #f1cf6a |
| `danger` | #a83325 |
| `danger-dark` | #f2938c |

| Role | Light | Dark |
| --- | --- | --- |
| `--color-ink` | #08231a | #eef6f0 |
| `--color-paper` | #eef6f0 | #12422a |
| `--color-surface` | #e2efe6 | #0c3320 |
| `--color-muted` | #51645b | #9db8a9 |
| `--color-line` | #c3d8cb | #2c5a41 |
| `--color-accent` | #0d4028 | #e7c04e |
| `--color-accentInk` | #eef6f0 | #12301f |
| `--color-focus` | #0d4028 | #f1cf6a |
| `--color-success` | #1f6d42 | #86d39c |
| `--color-warning` | #7a4b00 | #f1cf6a |
| `--color-danger` | #a83325 | #f2938c |

Every text role on every surface is measured in `contrast.json` (WCAG 2.x), and the crew repository's tests recompute it. These pairs are not for body text:

| Pair | Contrast | Use |
| --- | --- | --- |
| light: ink on accent | 1.41:1 | never |
| light: muted on accent | 1.87:1 | never |
| light: accentInk on paper | 1.00:1 | never |
| light: accentInk on surface | 1.08:1 | never |
| light: success on accent | 1.87:1 | never |
| light: warning on accent | 1.59:1 | never |
| light: danger on accent | 1.78:1 | never |
| light: focus on accent | 1.00:1 | never |
| dark: ink on accent | 1.58:1 | never |
| dark: muted on accent | 1.22:1 | never |
| dark: accentInk on paper | 1.25:1 | never |
| dark: accentInk on surface | 1.03:1 | never |
| dark: success on accent | 1.02:1 | never |
| dark: warning on accent | 1.15:1 | never |
| dark: danger on accent | 1.29:1 | never |
| dark: focus on accent | 1.15:1 | never |

Statuses never rely on colour alone: each has a word and an icon (docs/design/COMPONENTS.md), and success, warning and danger differ in lightness, so they read in greyscale.

## Type (B5)

| Role | Face | Package | Licence |
| --- | --- | --- | --- |
| display | Syne Variable | @fontsource-variable/syne | SIL Open Font License 1.1 (OFL-1.1), self-hosted from the pinned @fontsource package |
| body | Manrope Variable | @fontsource-variable/manrope | SIL Open Font License 1.1 (OFL-1.1), self-hosted from the pinned @fontsource package |
| mono | JetBrains Mono Variable | @fontsource-variable/jetbrains-mono | SIL Open Font License 1.1 (OFL-1.1), self-hosted from the pinned @fontsource package |

Why this type fits: Syne gives the circle name a grounded, hand-set weight on the deep green; Manrope stays even and legible under a tinted dark surface for the analyst's working copy; JetBrains Mono keeps member counts,

| Token | Min | Max |
| --- | --- | --- |
| `--text-xs` | 12px | 12px |
| `--text-sm` | 14px | 14px |
| `--text-base` | 16px | 16px |
| `--text-lg` | 18px | 18px |
| `--text-xl` | 22px | 22px |
| `--text-2xl` | 28px | 28px |
| `--text-3xl` | 36px | 36px |
| `--text-4xl` | 48px | 48px |

- Display (Syne) is reserved for the circle name, section titles and the single decision heading; never for body copy or numbers.
- Body (Manrope) carries all working copy, labels and form text at base 16px or larger.
- Mono (JetBrains Mono) is used only for member counts, amounts, standing codes and ledger figures; never for prose.
- Keep display weight high (700-800) and body weight mid (400-600) so the two faces stay visibly different.
- Line-height: 1.15 for display, 1.5 for body, 1.4 for mono.
- Do not set amounts in the display face; a figure in Syne reads as decoration, not data.

## Logo (B3)

A single canopy arc (a shallow dome) spans the top, drawn as a thick green stroke. Beneath it a horizontal ledger baseline runs across the lower third. Seven small member ticks stand on the baseline, evenly spaced, in ink green; the centre,

The mark sits on a 64-unit grid. Keep clear space of a quarter of its width on every side; never show it under 16px (favicon) or the lockup under 120px wide.

| File | Use |
| --- | --- |
| `logo/mark.svg` | the mark on paper; the favicon |
| `logo/mark-on-dark.svg` | the mark on the ink background |
| `logo/mark-mono.svg` | one colour: stamps, embossing, small sizes |
| `logo/mark-state-success.svg` | the mark in the success state |
| `logo/wordmark.svg` | the name alone |
| `logo/lockup.svg`, `logo/lockup-on-dark.svg` | mark and name together |

Don't:

- Do not replace the canopy arc with a leaf, a sprout or any plant glyph.
- Do not turn the member ticks into a ring of people or a handshake.
- Do not add a second accent colour; the gold node is the only non-green element.
- Do not outline the gold node or give it a shadow; it must read as a flat decision point.
- Do not set the wordmark in the display face at a light weight; it must stay bold and lowercase.
- Do not scale the mark below 16px; the ticks and node merge and the circle is lost.

## Iconography

Outline icons on a 24 grid, 2px strokes, rounded corners, in `icons/ui/`: `circle`, `standing`, `members`, `amount`, `decision`, `ledger`, `canopy`.

## Pattern (B8)

`patterns/canopy-ledger.svg` tiles seamlessly. Use only for quiet headers, empty states and section dividers at low opacity; never on primary controls, buttons or text backgrounds, and never at full opacity where it competes with the canopy green.

## Voice (B6)

1. **Speak like the person in the circle, not like a bank.** — This trader's standing is the question we answer.
2. **Name the trader's position, not their deficit.** — No land, no building — the standing stands on its own.
3. **Show the number the way it is entered, not rounded for comfort.** — Standing: 4 of 6 marks, updated 12 Oct.
4. **Say what the tool does; do not say what the bank will do.** — Enter the standing. Do not promise the loan.
5. **Keep the research caveat where the claim is made.** — Built from StartupTribunal research, published with caveats.
6. **Short. The analyst is mid-entry; the sentence should not be longer than the line they are filling.** — Next.
7. **One accent, one decision point. The gold colour is the 'next' action, nothing else.** — The only gold button on the page is the one that moves the circle forward.

| Use | Avoid |
| --- | --- |
| standing | score |
| circle | credit score |
| entered | risk |
| show | default |
| mark | approve |
| the person | deny |
| the trader | guarantee |

Banned words: “seamless”, “unlock”, “empower”, “elevate”, “next-gen”, “revolutionize”, “world-class”, “effortless”, “harness the power”, “game-changer”.

Copy for every product state:

| State | Copy |
| --- | --- |
| empty | No standing entered yet. Start with the person, not the form. |
| loading | Counting the marks in the circle. |
| error | The standing did not save. Check the line and enter it again. |
| success | Standing entered for the circle. |
| offline | You are off the line. The standing waits for the next connection. |

## Not this product (D21)

- The centred purple-to-blue fintech hero that every lender already wears
- Three identical feature cards with emoji icons and the same padding
- The 'handshake with a chart' stock photo that says trust without saying anything
- A glassmorphism panel floating over a blurred green blob
- The paired 'Get started / Learn more' CTA buttons that read as a landing page, not a tool
- A dashboard of charts before the analyst has entered a single standing
- A logo that is a generic leaf or a generic circle of people
- a centred hero with a purple-to-blue gradient
- three identical feature cards with emoji icons
- Inter or Roboto with no type contrast
- glassmorphism panels on a blurred blob background
- stock 'Get started' and 'Learn more' buttons side by side

Never in copy: “seamless”, “revolutionize”, “revolutionise”, “unlock”, “empower”, “next-gen”, “cutting-edge”, “game-changer”, “game changing”, “elevate”, “synergy”, “supercharge”, “leverage”, “world-class”, “effortless”, “unleash”, “harness the power”, “in today's”, “look no further”, “one-stop”.
