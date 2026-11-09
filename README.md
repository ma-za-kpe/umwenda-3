# Next.js site

A Next.js app exported as a static site and published to GitHub Pages by
Yard Crew's trusted delivery process. See `AGENTS.md` for how changes are
made and checked.

Scaffolded once with `create-next-app@16.4.0` (TypeScript, App Router, no
Tailwind, no linter, no `src/`), then pinned: `next` 16.4.1, `react` and
`react-dom` 19.3.0, `typescript` 5.9.3, `motion` 14.1.1, `idb` 8.0.4 and
twenty-seven OFL `@fontsource` faces 5.3.0, with
`package-lock.json`. The default tokens are neutral placeholders until the
design system writes `app/tokens.css` and `app/fonts.ts`.

```sh
npm ci --ignore-scripts
npm run build
python tests/site_view.py
python -m unittest discover -s tests
```

`trailingSlash` is off: `/menu` exports as `out/menu.html`, which Pages serves
for `/menu`, the same flat layout as the static template.
