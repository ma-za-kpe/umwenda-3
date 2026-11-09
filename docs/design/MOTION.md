# Umwenda motion (U3)

Motion explains change; it never decorates. One orchestrated moment greets the visitor, every other motion answers something they did.

| Token | Duration |
| --- | --- |
| `--motion-d-settle` | 220ms |
| `--motion-d-enter` | 340ms |
| `--motion-d-shift` | 480ms |
| `--motion-d-reveal` | 640ms |
| `--motion-d-burst` | 900ms |

| Token | Curve |
| --- | --- |
| `--ease-e-canopy` | cubic-bezier(0.22, 0.61, 0.36, 1) |
| `--ease-e-ledger` | cubic-bezier(0.4, 0, 0.2, 1) |
| `--ease-e-decision` | cubic-bezier(0.16, 0.84, 0.44, 1) |

## Moments

| Moment | Motion | Duration | Easing |
| --- | --- | --- | --- |
| load | canopy band, ledger row, standing field and decision point settle in as a staggered sequence | `d-enter` | `e-canopy` |
| save | the entered standing row confirms with a brief success tint and a quiet settle | `d-settle` | `e-ledger` |
| change | a standing value shifts and the affected ledger rows reflow in place | `d-shift` | `e-ledger` |
| decision | the single sun-gold decision point lifts and reveals its consequence | `d-reveal` | `e-decision` |
| burst | many changes arriving at once collapse into one grouped summary that settles | `d-burst` | `e-canopy` |
| error | an invalid standing flags with a danger tint and a short settle | `d-settle` | `e-ledger` |

## The load moment

In order, 90ms apart (`--reveal-step`, `components/kit/Reveal.tsx`): canopy band → ledger row → standing field → decision point.

- Reduced motion: Under reduced motion the full layout is shown at once with no staged movement and nothing hidden.
- Without JavaScript: Without JavaScript the page says the ledger needs JavaScript to enter a standing and keeps the canopy band and a plain note visible.
- Bursts: When many changes arrive at once they collapse into a single grouped summary that settles in one beat rather than animating each row.
- Focus: Focus is always a visible 2px accent outline on every interactive target, and every target is at least 44px.
