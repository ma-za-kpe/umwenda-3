"""Frozen check of the owner's content file, app/content.json. Standard library only.

The pages read the business facts from `app/content.json` (`{facts.F1}`), so
the owner changes a price or a sentence there, never in the code. This check
fails a change that breaks the file: it must be one JSON object of fact ids
(F1, F2, ...) to one-line text, hold every fact a page reads, and still show
the numbers and item names the approved brief's tests (`tests/test_brief.py`)
hold for each fact. A phone, email or map link a page builds from a fact
still has somewhere to go: a number to dial, an address to mail, a place to
search. These tests belong to the project owner: contributors,
people or agents, must not edit them to make a change pass (CODEOWNERS).
"""

import ast
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "app" / "content.json"
BRIEF = ROOT / "tests" / "test_brief.py"
FACT = re.compile(r"F[1-9][0-9]?")
READ = re.compile(r"\bfacts\.(F[1-9][0-9]?)\b")
# The contact links a page builds from a fact: `"tel:" + facts.F3...`.
LINK = re.compile(
    r'"(tel|mailto|https://www\.google\.com/maps/search/)[^"]*" \+ [^{}]*?\bfacts\.(F[1-9][0-9]?)\b'
)
EMAIL = re.compile(r"[A-Za-z0-9_.+-]+@[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)+")


def read_by_pages():
    """{fact id: [files]}: every fact a route or component reads."""
    found = {}
    for folder in ("app", "components"):
        for path in sorted((ROOT / folder).rglob("*.tsx")):
            for fid in READ.findall(path.read_text(encoding="utf-8")):
                found.setdefault(fid, []).append(path.relative_to(ROOT).as_posix())
    return found


def links_by_pages():
    """{(kind, fact id): [files]}: every contact link a route or component builds."""
    found = {}
    for folder in ("app", "components"):
        for path in sorted((ROOT / folder).rglob("*.tsx")):
            for kind, fid in LINK.findall(path.read_text(encoding="utf-8")):
                found.setdefault((kind, fid), []).append(path.relative_to(ROOT).as_posix())
    return found


def brief_facts():
    """FACTS from the brief's tests, {id: (numbers, item words)}, read, never run."""
    if not BRIEF.is_file():
        return {}
    for node in ast.parse(BRIEF.read_text(encoding="utf-8")).body:
        if isinstance(node, ast.Assign) and [getattr(t, "id", None) for t in node.targets] == [
            "FACTS"
        ]:
            return ast.literal_eval(node.value)
    return {}


def shows(text, numbers, words):
    """The text shows every whole number and every word ("8" is not "3.80")."""
    found = set(re.findall(r"\d+(?:[.:]\d+)?", text))
    return all(n in found for n in numbers) and all(
        re.search(r"\b" + re.escape(w) + r"\b", text) for w in words
    )


class ContentTests(unittest.TestCase):
    def content(self):
        if not CONTENT.is_file():
            return None
        try:
            return json.loads(CONTENT.read_text(encoding="utf-8"))
        except ValueError as error:
            self.fail(f"app/content.json is not valid JSON: {error}")

    def test_the_content_file_is_one_object_of_fact_ids_to_text(self):
        content = self.content()
        if content is None:
            return
        self.assertIsInstance(content, dict, "app/content.json must be one JSON object")
        for fid, value in content.items():
            with self.subTest(fact=fid):
                self.assertTrue(FACT.fullmatch(fid), "a fact's name is F1, F2, ...")
                self.assertIsInstance(value, str, "a fact's value is text in quotes")
                self.assertTrue(value.strip(), "a fact's value must not be empty")
                self.assertTrue(value.isprintable(), "a fact's value is one line of text")

    def test_every_fact_a_page_reads_is_present(self):
        read = read_by_pages()
        content = self.content()
        for fid, files in read.items():
            with self.subTest(fact=fid):
                self.assertIsInstance(content, dict, "the pages read app/content.json")
                self.assertIn(fid, content, f"{fid} is read by {', '.join(files)}")

    def test_each_fact_still_shows_what_the_brief_checks(self):
        content = self.content()
        if not isinstance(content, dict):
            return
        for fid, (numbers, words) in brief_facts().items():
            value = content.get(fid)
            if not isinstance(value, str):
                continue  # not lifted, or reported by the checks above
            with self.subTest(fact=fid):
                self.assertTrue(
                    shows(value.lower(), numbers, words),
                    f"{fid} must still show {' '.join(numbers + words)}, as tests/test_brief.py"
                    " holds it: change both together",
                )

    def test_each_contact_link_still_goes_somewhere(self):
        content = self.content()
        if not isinstance(content, dict):
            return
        for (kind, fid), files in links_by_pages().items():
            value = content.get(fid)
            if not isinstance(value, str):
                continue  # reported by the checks above
            where = f"{fid} makes the link in {', '.join(files)}"
            with self.subTest(fact=fid, link=kind):
                if kind == "tel":
                    self.assertRegex(value, r"[0-9]", f"{where}: it needs a phone number")
                elif kind == "mailto":
                    self.assertRegex(value, EMAIL, f"{where}: it needs an email address")
                else:
                    place = value[value.find(":") + 1 :].strip()
                    self.assertTrue(place, f"{where}: it needs an address")


if __name__ == "__main__":
    unittest.main()
