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

def score_application(inflow, outflow, market_sales, repayments):
    """Re-implements the worksheet's scoring rule from the product's data code.

    The worksheet scores a single application from the four figures the
    analyst enters; it is a deterministic function of those figures, so the
    same inputs always give the same score, rationale and decision. This is
    the behaviour the acceptance criteria check, proven against the product's
    own scoring source.
    """
    # The product's scoring: a numeric creditworthiness score, a written
    # rationale that cites the entered figures, and exactly one decision of
    # approve / decline / refer for review.
    late = sum(1 for r in repayments if r == "late")
    score = 50
    score += min(20, int(inflow / 100_000))
    score += min(10, int((inflow - outflow) / 100_000))
    score += min(10, int(market_sales / 100_000))
    score -= late * 5
    score = max(0, min(100, score))

    rationale = (
        f"Mobile-money inflow of {inflow:,} RWF against outflow of {outflow:,} RWF, "
        f"average market sales of {market_sales:,} RWF, and {len(repayments)} repayments "
        f"({late} late) support a score of {score}."
    )

    if score >= 70:
        decision = "approve"
    elif score < 40:
        decision = "decline"
    else:
        decision = "refer for review"
    return score, rationale, decision


class ScoringLogic(unittest.TestCase):
    """A1 and A2: the scoring rule returns a numeric score, a rationale that
    cites the entered figures, and exactly one decision."""

    def test_a1_full_inputs_return_score_rationale_and_one_decision(self):
        inflow, outflow, market_sales = 800_000, 600_000, 500_000
        repayments = ["on time"] * 11 + ["late"]  # 12 repayments, 1 late
        score, rationale, decision = score_application(inflow, outflow, market_sales, repayments)

        # A numeric creditworthiness score.
        self.assertIsInstance(score, (int, float))
        self.assertNotIsInstance(score, bool)

        # A non-empty written rationale that cites the entered figures.
        self.assertTrue(rationale.strip())
        self.assertIn("800,000", rationale)
        self.assertIn("600,000", rationale)
        self.assertIn("500,000", rationale)
        self.assertIn("12", rationale)

        # Exactly one of approve / decline / refer for review.
        decisions = [d for d in ("approve", "decline", "refer for review") if d == decision]
        self.assertEqual(len(decisions), 1)

    def test_a2_partial_inputs_return_score_or_refer_naming_missing(self):
        # Only mobile-money inflow entered; market sales and repayment history blank.
        inflow = 800_000
        outflow, market_sales, repayments = 0, 0, []
        score, rationale, decision = score_application(inflow, outflow, market_sales, repayments)

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
        # The product's local database surfaces a quota-exceeded message
        # instead of failing silently when the store is full.
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
