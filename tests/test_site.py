"""Frozen acceptance checks for every exported page in out/. Standard library only.

They run on what GitHub Pages serves: the static export (`npm run build`),
built with NEXT_BASE_PATH (the Pages project path, empty at the root) and
SITE_RELEASE (the commit). These tests belong to the project owner:
contributors, people or agents, must not edit them to make a change pass
(CODEOWNERS and the branch ruleset).
"""

import os
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "out"
BASE = os.environ.get("NEXT_BASE_PATH", "")
RELEASE = os.environ.get("SITE_RELEASE", "local")
# A task pull request into release/<n> (CREW_PARTIAL=1): a link to a page not
# built yet waits for it, by name; main and the release pull request are strict.
PARTIAL = os.environ.get("CREW_PARTIAL") == "1"


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags, self.attrs, self.title, self._in_title = [], [], "", False

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        self.attrs.append((tag, dict(attrs)))
        self._in_title = tag == "title"

    def handle_endtag(self, tag):
        self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def pages():
    found = sorted(OUT.rglob("*.html"))
    assert found, "out/ needs at least index.html: run `npm run build` first"
    for path in found:
        page = Page()
        page.feed(path.read_text(encoding="utf-8"))
        yield path, page


def _local(path, target):
    """The exported file a local link reaches, or None if it leaves the site."""
    target = target.split("#")[0].split("?")[0]
    if BASE and target == BASE:
        return OUT
    if target.startswith(BASE + "/") and not target.startswith("//"):
        return OUT / target[len(BASE) + 1 :]
    if target.startswith("/"):
        return None
    return path.parent / target


class SiteTests(unittest.TestCase):
    def test_every_page_declares_language_title_and_viewport(self):
        for path, page in pages():
            with self.subTest(page=path.name):
                html = dict(page.attrs)["html"]
                self.assertTrue(html.get("lang"))
                self.assertTrue(page.title.strip())
                metas = [a for t, a in page.attrs if t == "meta"]
                self.assertTrue(any(m.get("name") == "viewport" for m in metas))

    def test_every_page_has_one_h1_and_the_main_landmarks(self):
        for path, page in pages():
            with self.subTest(page=path.name):
                self.assertEqual(page.tags.count("h1"), 1)
                for landmark in ("header", "main", "footer"):
                    self.assertIn(landmark, page.tags)

    def test_images_have_alt_text_and_links_have_targets(self):
        for path, page in pages():
            for tag, attrs in page.attrs:
                with self.subTest(page=path.name, tag=tag):
                    if tag == "img":
                        self.assertIn("alt", attrs)
                    if tag == "a":
                        self.assertTrue(attrs.get("href"))

    def test_local_links_and_assets_resolve(self):
        # Links start at the base path (as Next.js writes them) or at the
        # page's folder; a path without .html reaches its page, as on Pages.
        for path, page in pages():
            for tag, attrs in page.attrs:
                target = attrs.get("href") or attrs.get("src")
                if not target or re.match(r"(https?:|mailto:|tel:|#)", target):
                    continue
                found = _local(path, target)
                with self.subTest(page=path.name, target=target):
                    self.assertIsNotNone(found)
                    resolves = (
                        found == OUT
                        or found.exists()
                        or found.with_name(found.name + ".html").is_file()
                    )
                    last = found.name
                    if not resolves and PARTIAL and ("." not in last or last.endswith(".html")):
                        self.skipTest("not built yet: " + target)
                    self.assertTrue(resolves)

    def test_scripts_are_only_the_sites_own_bundles(self):
        # Next.js ships its own script bundles; nothing loads from elsewhere.
        for path, page in pages():
            for tag, attrs in page.attrs:
                if tag == "script" and attrs.get("src"):
                    with self.subTest(page=path.name, src=attrs["src"]):
                        self.assertTrue(attrs["src"].startswith(BASE + "/_next/static/"))

    def test_no_active_content(self):
        # Nothing on a page sends anything anywhere: no event handlers, script
        # or data URLs, embedded documents, forms or redirects.
        for path, page in pages():
            for tag, attrs in page.attrs:
                with self.subTest(page=path.name, tag=tag):
                    self.assertNotIn(tag, ("iframe", "object", "embed", "form", "frame", "base"))
                    self.assertFalse([name for name in attrs if name.startswith("on")])
                    if tag == "meta":
                        self.assertNotEqual((attrs.get("http-equiv") or "").lower(), "refresh")
                    for name in ("href", "src", "action", "data", "formaction"):
                        value = re.sub(r"\s", "", attrs.get(name) or "").lower()
                        self.assertFalse(value.startswith(("javascript:", "data:", "vbscript:")))

    def test_the_release_marker_is_present(self):
        index = (OUT / "index.html").read_text(encoding="utf-8")
        self.assertIn(f'data-release="{RELEASE}"', index)


if __name__ == "__main__":
    unittest.main()
