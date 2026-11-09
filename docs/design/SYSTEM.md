# Umwenda design system: shape and depth (U1, U2)

The tokens live in `app/tokens.css` (and `brand/tokens.css`); pages use them only.

## Spacing

| Token | Value |
| --- | --- |
| `--space-1` | 0.5rem |
| `--space-2` | 1rem |
| `--space-3` | 1.5rem |
| `--space-4` | 2.5rem |
| `--space-5` | 4rem |
| `--space-6` | 6rem |

## Radius

| Token | Value |
| --- | --- |
| `--radius-r-sm` | 4px |
| `--radius-r-md` | 8px |
| `--radius-r-lg` | 14px |

## Elevation

| Token | Offset | Blur | Opacity |
| --- | --- | --- | --- |
| `--shadow-e-quiet` | 0px | 0px | 0 |
| `--shadow-e-ledger` | 2px | 6px | 0.08 |
| `--shadow-e-decision` | 4px | 12px | 0.14 |

## Widths and grid

- Content reaches 1120px (`--content-max`) in a 12-column grid from 960px, 6 columns from 640px and one column on a phone.
- Prose keeps a measure of 68ch (`--measure`).
- Nothing is wider than the viewport: the browser check fails any sideways scroll at 320px.

Type: Syne Variable for display, Manrope Variable for body and JetBrains Mono Variable for figures; see brand/BRAND.md.
