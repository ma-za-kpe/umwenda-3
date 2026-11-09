# Handoff

## State

As of this commit, 0 of 1 tasks were done and the work was going task by task through pull requests into `release/1`.

## Publication

Trusted code publishes the site from `main` only after the release merges and CI on `main` is green, and tags a release only after the live site is verified. Whether it is published: see the latest GitHub Release (tag `release-<n>`) at https://github.com/ma-za-kpe/umwenda-3/releases and the verified-publication evidence on [#1](https://github.com/ma-za-kpe/umwenda-3/issues/1).

- Repository: https://github.com/ma-za-kpe/umwenda-3
- Site address: https://ma-za-kpe.github.io/umwenda-3/

## How to change content

The brief's facts live in `app/content.json`: change a value there and every page that shows it follows. Pages are under `app/`, the style is `app/globals.css` and the brand tokens are in `brand/tokens.css`.

Open a pull request; CI runs the frozen tests and the browser check on it.

## Follow-ups recorded as of this commit

None.
