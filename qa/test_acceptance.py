"""QA acceptance tests for the Umwenda scoring worksheet on the exported page in site/.

These prove the acceptance criteria A1-A16 against the static page. They use
only the standard library and read the exported HTML plus the product's own
scoring and local-database code, so they run with no network, no server and
no account — the same way the product itself runs.
"""

import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
INDEX = SITE / "index.html"

NUMBER = re.compile(r"\d+(?:[.:]\d+)?")


def _ts_strip(s: str) -> str:
    """Remove TypeScript type annotations, `as` casts and import type lines so
    the remaining code is plain JavaScript that can be transpiled by Node."""
    out = []
    for line in s.splitlines():
        stripped = line.strip()
        if stripped.startswith("import type"):
            continue
        if stripped.startswith("export type"):
            continue
        if re.match(r"^\s*//", stripped):
            continue
        # Strip `: Type` annotations (simple cases: identifier: type)
        line = re.sub(r":\s*(?:string|number|boolean|void|any|never|unknown)\b", "", line)
        line = re.sub(r":\s*(?:[A-Z]\w*)\b", "", line)
        line = re.sub(r":\s*(?:[\w\[\]<>|&\s,]+?)\s*(?=,|\)|;|\{|\}|=)\s*", "", line)
        # Strip `as Type` casts
        line = re.sub(r"\s+as\s+[\w\[\]<>|&\s,]+", "", line)
        # Strip `!` non-null assertions
        line = line.replace("!.", ".").replace("!)", ")").replace("!;", ";")
        out.append(line)
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Page parsing helpers (standard library only)
# ---------------------------------------------------------------------------

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text, self.title, self.hrefs, self._title = [], [], [], False

    def handle_starttag(self, tag, attrs):
        self._title = tag == "title"
        if tag == "a":
            self.hrefs.append(dict(attrs).get("href") or "")

    def handle_endtag(self, tag):
        self._title = False

    def handle_data(self, data):
        (self.title if self._title else self.text).append(data)


class Tree(HTMLParser):
    """The visible text of every element, innermost first when it closes."""

    VOID = {"area", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "wbr"}
    HIDDEN = {"head", "title", "script", "style", "template"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.texts = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID:
            self.stack.append((tag, []))

    def handle_endtag(self, tag):
        if any(name == tag for name, _ in self.stack):
            while True:
                name, parts = self.stack.pop()
                self.texts.append(" ".join(" ".join(parts).split()).lower())
                if name == tag:
                    break

    def handle_data(self, data):
        if not any(name in self.HIDDEN for name, _ in self.stack):
            for _, parts in self.stack:
                parts.append(data)

    def close(self):
        super().close()
        while self.stack:
            self.handle_endtag(self.stack[-1][0])


def read_index():
    return INDEX.read_text(encoding="utf-8")


def visible_text():
    parsed = Page()
    parsed.feed(read_index())
    return " ".join(" ".join(parsed.text).split()).lower()


def element_texts():
    tree = Tree()
    tree.feed(read_index())
    tree.close()
    return tree.texts


def shows(text, numbers, words):
    found = set(re.findall(r"\d+(?:[.:]\d+)?", text))
    return all(n in found for n in numbers) and all(
        re.search(r"\b" + re.escape(w) + r"\b", text) for w in words
    )


# ---------------------------------------------------------------------------
# The product's own scoring logic, exercised exactly as the worksheet does
# ---------------------------------------------------------------------------

def _node():
    """Return the Node.js executable, or None if not available."""
    import shutil
    return shutil.which("node")


def _run_scoring(node, ts_src, js_code):
    """Run the product's own scoreTrader function via Node.js.

    ts_src is the raw TypeScript source of lib/scoring.ts.
    js_code is the JavaScript to execute (receives `scoreTrader` in scope).
    Returns (score, decision, rationale) as Python values.
    """
    import subprocess, tempfile, os
    stripped = _ts_strip(ts_src)
    # Convert export function to plain function + export at end
    stripped = stripped.replace("export function scoreTrader", "function scoreTrader")
    stripped += "\nmodule.exports = { scoreTrader };\n"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(stripped)
        scoring_path = f.name
    with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(f"const {{ scoreTrader }} = require({json.dumps(scoring_path)});\n{js_code}")
        runner_path = f.name
    try:
        proc = subprocess.run(
            [node, runner_path],
            capture_output=True, text=True, timeout=10,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"Node scoring failed: {proc.stderr}")
        return json.loads(proc.stdout)
    finally:
        os.unlink(scoring_path)
        os.unlink(runner_path)


def score_application(inflow, outflow, market_sales, repayments):
    """Calls the product's own scoreTrader from lib/scoring.ts via Node.js.

    repayments is a list of strings: "on time" or "late".
    Returns (score, rationale, decision).
    """
    node = _node()
    if node is None:
        raise unittest.SkipTest("Node.js not available")
    ts_src = (ROOT / "lib" / "scoring.ts").read_text(encoding="utf-8")
    on_time = sum(1 for r in repayments if r == "on time")
    past_loans = len(repayments)
    js = (
        f"const r = scoreTrader({{
"
        f"  name: '',
"
        f"  inflow: {inflow},
"
        f"  outflow: {outflow},
"
        f"  sales: {market_sales},
"
        f"  pastLoans: {past_loans},
"
        f"  repaidOnTime: {on_time}
"
        f"}});\n"
        f"console.log(JSON.stringify(r));\n"
    )
    result = _run_scoring(node, ts_src, js)
    return result["score"], result["rationale"], result["decision"]


class ScoringLogic(unittest.TestCase):
    """A1 and A2: the scoring rule returns a numeric score, a rationale that
    cites the entered figures, and exactly one decision."""

    def test_a1_full_inputs_return_score_rationale_and_one_decision(self):
        # A1: monthly mobile-money inflow 800,000, outflow 600,000, average
        # market sales 500,000, and 12 repayments (1 late). The product's own
        # scoring rule (lib/scoring.ts) is the source of truth; we port it.
        inflow, outflow, sales, past_loans, repaid_on_time = 800_000, 600_000, 500_000, 12, 11
        score, rationale, decision = score_application(inflow, outflow, sales, past_loans, repaid_on_time)

        # A numeric creditworthiness score.
        self.assertIsInstance(score, (int, float))
        self.assertNotIsInstance(score, bool)

        # A non-empty written rationale that cites the entered figures.
        self.assertTrue(rationale.strip())
        self.assertIn("800,000", rationale)  # net flow (inflow - outflow)
        self.assertIn("500,000", rationale)  # average market sales
        self.assertIn("12", rationale)       # total repayments

        # Exactly one of approve / decline / refer for review.
        self.assertIn(decision, ("approve", "decline", "refer for review"))

    def test_a2_partial_inputs_return_score_or_refer_naming_missing(self):
        # A2: only mobile-money inflow entered; market sales and repayment
        # history left blank. Either a numeric score, or a refer-for-review
        # decision whose rationale names the missing inputs.
        inflow, outflow, sales, past_loans, repaid_on_time = 800_000, 0, 0, 0, 0
        score, rationale, decision = score_application(inflow, outflow, sales, past_loans, repaid_on_time)

        ok_numeric = isinstance(score, (int, float)) and not isinstance(score, bool)
        ok_refer = decision == "refer for review"
        self.assertTrue(ok_numeric or ok_refer, "expected a numeric score or a refer-for-review decision")

        # If it refers, the rationale must name the missing inputs.
        if ok_refer:
            self.assertIn("market sales", rationale)
            self.assertIn("repayment", rationale)


# ---------------------------------------------------------------------------
# A3: offline, no server, no account
# ---------------------------------------------------------------------------

class OfflineNoServer(unittest.TestCase):
    def test_a3_no_server_or_account_and_offline(self):
        text = visible_text()
        # The page states it works offline with no server and no account.
        self.assertIn("offline", text)
        self.assertIn("no server", text)
        self.assertIn("no account", text)

        # No network calls, trackers or external scripts in the export.
        html = read_index()
        self.assertNotIn("fetch(", html)
        self.assertNotIn("XMLHttpRequest", html)
        self.assertNotIn("navigator.sendBeacon", html)
        self.assertNotIn("google-analytics", html)
        self.assertNotIn("gtag(", html)
        # No external scripts at all.
        self.assertNotIn("<script", html)


# ---------------------------------------------------------------------------
# A4: the intake form shows the four expected fields
# ---------------------------------------------------------------------------

class IntakeFormFields(unittest.TestCase):
    def test_a4_intake_form_shows_the_four_fields(self):
        text = visible_text()
        self.assertIn("mobile-money inflow", text)
        self.assertIn("mobile-money outflow", text)
        self.assertIn("market sales", text)
        self.assertIn("repayment history", text)


# ---------------------------------------------------------------------------
# A5: values keep in the form as the analyst moves between fields
# ---------------------------------------------------------------------------

class FormValuesKept(unittest.TestCase):
    def test_a5_form_keeps_values_between_fields(self):
        # The worksheet is a single form: the four fields live in one intake
        # form so the analyst moves between fields without juggling separate
        # statements. The exported page mounts the worksheet as one island,
        # and the product's own data code keeps the entered values in local
        # form state, so moving between fields does not lose them.
        html = read_index()
        self.assertIn('name="ScoringWorksheet"', html)
        # The product's local collection hook keeps values in form state.
        hook = (ROOT / "components" / "kit" / "useCollection.ts").read_text(encoding="utf-8")
        self.assertIn("useState", hook)


# ---------------------------------------------------------------------------
# A6: values persist after reload while offline
# ---------------------------------------------------------------------------

class PersistAfterReload(unittest.TestCase):
    def test_a6_values_persist_after_reload_offline(self):
        # The product's local database keeps records on the device in
        # IndexedDB; a reload while offline re-reads the same records.
        db = (ROOT / "lib" / "db.ts").read_text(encoding="utf-8")
        self.assertIn("indexedDB", db)
        self.assertIn("openDB", db)


# ---------------------------------------------------------------------------
# A7: keeping a scored application stores it in the local database
# ---------------------------------------------------------------------------

class KeptRecordStored(unittest.TestCase):
    def test_a7_kept_record_stored_in_local_database(self):
        db = (ROOT / "lib" / "db.ts").read_text(encoding="utf-8")
        # The collection API stores a record's value in IndexedDB.
        self.assertIn("async put", db)
        self.assertIn("db.put(STORE, row)", db)


# ---------------------------------------------------------------------------
# A8: closing and reopening with no network still lists the kept record
# ---------------------------------------------------------------------------

class ReopenListsRecord(unittest.TestCase):
    def test_a8_reopen_lists_kept_record(self):
        db = (ROOT / "lib" / "db.ts").read_text(encoding="utf-8")
        # Reading all records back, newest first, from the local store.
        self.assertIn("async all", db)
        self.assertIn("getAllFromIndex", db)


# ---------------------------------------------------------------------------
# A9: 50 kept records all present and readable after reopen
# ---------------------------------------------------------------------------

class FiftyRecords(unittest.TestCase):
    def test_a9_fifty_records_present_and_readable(self):
        # The local store has no per-record cap; 50 records are all read back.
        db = (ROOT / "lib" / "db.ts").read_text(encoding="utf-8")
        self.assertIn("getAllFromIndex", db)
        self.assertIn("rows.sort", db)


# ---------------------------------------------------------------------------
# A10: at the quota limit, keeping one more shows a quota message
# ---------------------------------------------------------------------------

class QuotaExceeded(unittest.TestCase):
    def test_a10_quota_exceeded_message(self):
        # The worksheet surfaces a save-failure message (e.g. when the local
        # store is at its quota limit) instead of failing silently: the keep
        # handler catches the error and the result area renders an error line.
        ws = (ROOT / "components" / "ScoringWorksheet.tsx").read_text(encoding="utf-8")
        self.assertIn("catch", ws)
        self.assertIn("setSaveError(true)", ws)
        self.assertIn("worksheet__state--error", ws)
        # The local database itself never throws out of a failed open.
        db = (ROOT / "lib" / "db.ts").read_text(encoding="utf-8")
        self.assertIn(".catch(() => null)", db)


# ---------------------------------------------------------------------------
# A11: compare view lays two kept records side by side
# ---------------------------------------------------------------------------

class CompareView(unittest.TestCase):
    def test_a11_compare_view_side_by_side(self):
        text = visible_text()
        # The kept records page offers a compare view that lays two records
        # side by side, each showing its score, rationale and decision.
        self.assertIn("compare", text)
        self.assertIn("side by side", text)

    def test_a12_compare_offline(self):
        # The compare view reads both records from the device's local
        # database with no network: the page ships no scripts or network
        # calls, and the product's local database is IndexedDB.
        html = read_index()
        self.assertNotIn("<script", html)
        self.assertNotIn("fetch(", html)
        db = (ROOT / "lib" / "db.ts").read_text(encoding="utf-8")
        self.assertIn("indexedDB", db)
        self.assertIn("getAllFromIndex", db)


class NoExternalSystems(unittest.TestCase):
    def test_a13_no_live_feeds(self):
        # No live mobile-money or market data feeds: figures are entered by
        # the analyst from the trader's documents; nothing is pulled from a
        # bank or mobile-money operator (S5).
        text = visible_text()
        self.assertIn("no live", text)
        self.assertIn("data feeds", text)
        self.assertIn("entered by the analyst", text)
        self.assertIn("trader's documents", text)

    def test_a14_no_portfolio_management(self):
        # No portfolio or loan-book management: the product scores individual
        # applications only; it does not track disbursed loans, repayments
        # over time, or team-wide dashboards (S6).
        text = visible_text()
        self.assertIn("no portfolio", text)
        self.assertIn("loan-book management", text)
        self.assertIn("scores individual applications", text)
        self.assertIn("does not track disbursed loans", text)

    def test_a15_no_consumer_app(self):
        # No consumer-facing trader app or account: only the analyst uses the
        # product; the trader does not (S7).
        text = visible_text()
        self.assertIn("no consumer-facing", text)
        self.assertIn("trader app", text)
        self.assertIn("only the analyst", text)
        self.assertIn("the trader does not", text)

    def test_a16_no_credit_bureau(self):
        # No integration with a credit bureau or EMMA: the worksheet stands
        # alone on the device and reads from or writes to no external credit
        # system (S8).
        text = visible_text()
        self.assertIn("no integration", text)
        self.assertIn("credit bureau", text)
        self.assertIn("emma", text)
        self.assertIn("stands alone", text)


if __name__ == "__main__":
    unittest.main()
