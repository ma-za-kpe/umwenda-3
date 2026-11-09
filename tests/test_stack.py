"""Frozen check of the stack allowlist on the repository's own files. Standard library only.

The product is offline first and ships nothing it did not build: no network
calls, trackers, external scripts, fonts or images, no server code and no
dependency the platform did not pin. `tests/stack_policy.py` states each
rule and the fix; Yard Crew's trusted build runs the same file before
`next build`. These tests belong to the project owner: contributors, people
or agents, must not edit them to make a change pass (CODEOWNERS).
"""

import json
import unittest
from pathlib import Path

import stack_policy

ROOT = Path(__file__).resolve().parents[1]


class StackTests(unittest.TestCase):
    def test_the_crew_code_keeps_to_the_stack(self):
        files = stack_policy.repository(ROOT)
        lock = json.loads((ROOT / "package-lock.json").read_text(encoding="utf-8"))
        pinned = {
            name: lock["packages"][""].get(kind, {}).get(name)
            for kind in ("dependencies", "devDependencies")
            for name in lock["packages"][""].get(kind, {})
        }
        found = stack_policy.violations(files, pinned)
        self.assertEqual(found, [], "\n".join(found))


if __name__ == "__main__":
    unittest.main()
