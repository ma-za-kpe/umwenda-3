# Umwenda

Live site: https://ma-za-kpe.github.io/umwenda-3/

Built and published by Yard Crew from an approved brief. The pages are in
`app/`; your business content is in `app/content.json`.

## Changing content

Your business content is in one file, `app/content.json`: each entry is one fact
from your brief, exactly as the pages show it. The pages read it, so you
never edit HTML or code to change a price, a time or a sentence.

- Nothing yet: no page shows a brief fact word for word.

- Who it is for: Fintech and analytics teams and customers in Rwanda: not in the content file (the pages do not show it word for word); ask the crew to change it.
- StartupTribunal research reports: Traditional lending in Rwanda focuses almost entirely on tangible assets like land or buildings, shutting out the majority of citizens and small traders who lack formal collateral. This forces creditworthy people into high-interest informal lenders or blocks them from accessing capital needed for business growth, emergencies, or home improvement. The launch of EMMA signals that banks themselves acknowledge this broken system.: not in the content file (the pages do not show it word for word); ask the crew to change it.
- Research status: rejected by the StartupTribunal AI Tribunal, published with caveats.: not in the content file (the pages do not show it word for word); ask the crew to change it.
- Research by StartupTribunal: https://startuptribunal.com/catalog/rwandans-without-collateral-denied-bank-loans: not in the content file (the pages do not show it word for word); ask the crew to change it.

To change a value:

1. On GitHub, open `app/content.json`, choose Edit, and change only the text in
   quotes after the fact's name. Keep the quotes, and the comma where there
   is one.
2. Commit it to a new branch and open a pull request.
3. CI checks the pull request: it builds the site, runs the frozen tests on
   every page, and `tests/test_content.py` checks that the file is valid JSON
   and still holds every fact the pages read.
4. When CI is green, merge it into `main`, then ask the crew for a release
   (see Publishing). The live site changes only then.

Your approved brief is checked too: `tests/test_brief.py` holds the numbers
and item names of each fact. A new price or time changes your brief, so CI
stays red until that fact's entry in `FACTS` in `tests/test_brief.py` (yours,
under CODEOWNERS) states the new numbers as well: change both in the same pull
request. Rewording that keeps the numbers and item names needs only the
content file. Phone, email and map links are in the pages themselves; ask the
crew to change those.

### Rolling back

Each release is tagged at the commit it published (`release-1`, `release-2`,
...; see Releases on GitHub). To return the content to an earlier release,
restore the content file and the brief tests from its tag on a new branch:

```
git checkout -b restore-content
git checkout release-1 -- app/content.json tests/test_brief.py
git commit -m "Restore content from release-1"
git push -u origin restore-content
```

or choose Revert on the merged pull request on GitHub. Either way, open the
pull request, let CI check it, merge it and ask the crew for a release. A
one-step rollback that re-publishes an earlier build without a pull request
is not available yet.

### Design

- Colours and spacing: the design tokens in `app/globals.css` lines 1–54.

## Checks that protect your site

- `python -m unittest discover -s tests` runs the frozen tests, including
  `tests/test_brief.py`, which come from your approved brief.
- `pre-commit install` once, so the same pinned hooks as CI run on every commit.
- CI also checks the page in a real browser at phone and desktop sizes, with
  automated accessibility checks.
- `tests/` belongs to you (CODEOWNERS): nobody edits it to make a change pass.
  CI and tooling (`.github/`) changes are approved by the crew's platform
  review and must keep every action pinned, the tests running and every job.

## Publishing

GitHub Pages serves the `gh-pages` branch. Yard Crew's trusted release builds
`main`'s exact commit after every required check passes on it, publishes that
build to `gh-pages`, checks the live page and tags the release. A merge to
`main` by itself does not update the live site: ask the crew for a release.

## Approving content

Read every price, time and contact detail on the live page before telling
customers about it. The crew states only what your brief gives; anything new
needs your approval first.

## Custom domain

Add your domain under Settings, Pages, Custom domain, then point a DNS CNAME
record at the GitHub Pages address.

## Analytics

No analytics or trackers are installed, so the site collects nothing about
visitors. Adding any is a privacy decision for you to make.

## Maintenance

The site is static: no server, database or secrets to patch. Keep the pinned
tool versions current through reviewed pull requests.
