# Working on this site

This repository was created and is published by Yard Crew's trusted delivery
code. It is a Next.js app (App Router, TypeScript) exported as a static site
for GitHub Pages. People and agents who change it follow the same rules.

- **What the crew writes.** Pages, layouts and components under `app/` and
  `components/`, the product's own data code under `lib/` (beside the kit's
  `lib/db.ts`), styles (`app/globals.css`, CSS modules, `styles/`) and
  static files in `public/`. Keep colours, sizes and spacing in the design
  tokens at the top of `app/globals.css`.
- **The stack (owner decision D2).** Real React: server components for the
  page, client islands (`"use client"`) for interactive features under
  `components/`, the pinned motion library (`motion/mini` for small
  enter and exit animations, `motion/react` for springs, gestures or
  layout animation), self-hosted
  faces from the pinned `@fontsource` packages (`app/fonts.ts`) and SVG
  artwork in `public/` or inline. `components/kit/` holds the orchestrated
  load moment (`Reveal`), a local collection hook and an example island.
  `tests/stack_policy.py` is the allowlist: no network calls, trackers,
  external scripts, fonts or images, no server code and no new dependency.
- **Offline first (owner decision D1).** The product's data lives on this
  device in IndexedDB through `lib/db.ts`; nothing needs a connection.
- **Design system.** Every colour, size, space, radius and duration comes
  from `app/tokens.css`, written by the design system with `brand/` and
  `docs/design/`; `tests/test_design.py` recomputes its contrast table.
  Desktop content reaches at least 960px on the 12-column grid.
- **Content in one place.** The brief's facts the pages show (prices, hours,
  contact, copy) are in `app/content.json`, and pages read them as
  `{facts.F1}`, never as copied text, so the owner changes a value without
  touching code. `tests/test_content.py` checks the file on every change.
- **What is frozen.** `tests/` belongs to the owner (CODEOWNERS): never edit
  it to make a change pass. `.github/`, `next.config.ts`, `package.json`,
  `package-lock.json` and `tsconfig.json` are platform files: a change needs
  the platform review's approval, keeps every version exact (no `^`, `~` or
  `latest`) and keeps the lockfile in step.
- **Static export only.** `output: "export"`: no API routes, server actions,
  middleware, `next/image` optimisation, cookies or runtime environment.
  Everything in the export is public. No keys, trackers or third-party
  scripts.
- **Built by trusted code.** `npm ci` and `npm run build` run in a pinned
  container with no network for the build. The base path (`NEXT_BASE_PATH`)
  and release marker (`SITE_RELEASE`) are set by the build, never by page
  code. Use `next/link` for links so the base path applies.
- **Test first.** The frozen tests run on the exported HTML in `out/`:
  `npm run build && python tests/site_view.py && python -m unittest discover -s tests`.
  `tests/test_brief.py`, when present, is generated from the approved brief
  and fails until the pages meet it.
- **Checked in a real browser.** CI also runs `tests/browser/qa.mjs` on the
  export at phone and desktop sizes: no overflow, keyboard focus, reduced
  motion and no axe WCAG 2.1 AA violations, plus the quality floors in
  `tests/browser/budget.json`: desktop content spans at least 960px, the
  Chromium performance budget, the pinned Lighthouse's floors on every page
  (performance at least 90 and accessibility 100, on the desktop and the
  mobile preset, with no network), a load moment when motion is allowed,
  and an approved visual baseline per page once one is committed under
  `tests/browser/baseline/`. The check serves the site as GitHub Pages does
  (`tests/browser/serve.mjs`: gzip, Pages' cache headers).
- **Fast on a phone.** The mobile floor is a mid-range phone on slow 4G.
  The largest content paints at once: the load moment (`Reveal`) moves
  blocks but never hides them, so never fade or hide the hero. Import a
  library only in the island that needs it, and the lightest that does
  the job (`motion/mini` is about 2 KB; `motion/react` about 37 KB), so a
  page without one ships none. Give every image its `width` and `height`, keep
  it near the size it shows at, prefer SVG, WebP or AVIF, and mark images
  below the fold `loading="lazy"`.
- **Accessible by default.** One `h1` per page, header, main and footer
  landmarks, alt text, visible focus, sufficient contrast, reduced-motion
  support.
- **Clean up after yourself.** No `node_modules`, `.next`, `out` or `site`
  in Git; keep files small.
- **Evidence over claims.** A change is done when the tests pass and the
  published page shows its release marker. The crew's trusted release
  publishes `main` after its checks pass (a merge alone does not), and a
  release counts only once the live page shows it.

## Map

- `docs/PRD.md`: the product: personas, the core feature, the MVP and its non-goals.
- `docs/ARCHITECTURE.md`: pages, content model, decisions and non-functional needs.
- `brand/`: the brand kit: logo system, palette, type, voice and tokens.
- `docs/design/`: the design system: tokens, motion, components and experience.
- `crew/plan.json`: the feature list; `passes` is set by trusted checks only.
- `PROGRESS.md`: where the work stands, the open sprint and the recent commits.
- `docs/PLAN.md`: the tasks and their pull requests.

## Start here

Every role, every time, before any change:

1. Read `PROGRESS.md`: where the work stands, the open sprint and the recent commits.
2. Read `crew/plan.json`: every feature, its status and whether it passes.
3. Read the recent commits in `PROGRESS.md` before you change anything.
4. Run the checks before you change anything, so you know what already fails.
5. Work on the open sprint's features only; set their status with `update_plan`.
