"""Frozen check of the design system's measured contrast (#233 U1). Standard library only.

The design system documents every text colour on every surface, in both
themes, in `brand/contrast.json`, and the pages take their colours from
`app/tokens.css`. This recomputes each ratio (WCAG 2.x) from the tokens the
pages really use, so a token edited by hand cannot keep a stale, flattering
table, and every pair the system requires still meets its bar. Before the
design system is written (no brand/contrast.json) there is nothing to check.
These tests belong to the project owner: contributors, people or agents, must
not edit them to make a change pass (CODEOWNERS).
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "brand" / "contrast.json"
TOKENS = ROOT / "app" / "tokens.css"


def luminance(colour):
    def channel(part):
        c = int(part, 16) / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (channel(colour[i : i + 2]) for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    high, low = sorted((luminance(a), luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def themes(css):
    """{"light": {role: hex}, "dark": {role: hex}} from the tokens' colour roles."""
    dark_at = css.find("prefers-color-scheme: dark")
    found = {"light": {}, "dark": {}}
    for match in re.finditer(r"--color-([a-z-]+):\s*(#[0-9a-fA-F]{6})\s*;", css):
        theme = "dark" if 0 <= dark_at < match.start() else "light"
        role = re.sub(r"-([a-z])", lambda m: m.group(1).upper(), match.group(1))
        found[theme][role] = match.group(2).lower()
    return found


class DesignTests(unittest.TestCase):
    def test_every_documented_ratio_recomputes_from_the_tokens(self):
        if not TABLE.is_file():
            self.skipTest("no design system yet: brand/contrast.json is written with it")
        table = json.loads(TABLE.read_text(encoding="utf-8"))
        colours = themes(TOKENS.read_text(encoding="utf-8"))
        self.assertEqual({p["theme"] for p in table["pairs"]}, {"light", "dark"})
        for pair in table["pairs"]:
            where = f"{pair['theme']}: {pair['text']} on {pair['on']}"
            with self.subTest(pair=where):
                fg = colours[pair["theme"]].get(pair["text"])
                bg = colours[pair["theme"]].get(pair["on"])
                self.assertEqual((fg, bg), (pair["fg"], pair["bg"]), f"{where}: tokens.css differs")
                self.assertEqual(
                    round(contrast(fg, bg), 2), pair["ratio"], f"{where}: ratio is stale"
                )

    def test_every_required_pair_meets_its_bar_in_both_themes(self):
        if not TABLE.is_file():
            self.skipTest("no design system yet: brand/contrast.json is written with it")
        table = json.loads(TABLE.read_text(encoding="utf-8"))
        colours = themes(TOKENS.read_text(encoding="utf-8"))
        for text, on, need in table["required"]:
            for theme in ("light", "dark"):
                with self.subTest(pair=f"{theme}: {text} on {on}"):
                    ratio = contrast(colours[theme][text], colours[theme][on])
                    self.assertGreaterEqual(ratio, need, f"{theme}: {text} on {on} needs {need}:1")


if __name__ == "__main__":
    unittest.main()
