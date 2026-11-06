import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
import re

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from catalog_tools import ROOT, details, load_catalog
from build_agent_site import build, validate_links, md
from search_catalog import search


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_catalog()

    def test_search_unicode_limit_and_unknowns(self):
        rows = search(self.data, "ＰＤＦ", "docs_office", 3)
        self.assertTrue(rows)
        self.assertLessEqual(len(rows), 3)
        self.assertTrue(all(r["category"] == "docs_office" for r in rows))
        self.assertEqual(search(self.data, "no-such-tool-812739"), [])
        with self.assertRaises(ValueError):
            search(self.data, category="nonexistent")
        self.assertTrue(all(r["checked_at"] is None and r["runtime_requirements"] is None
                            and r["test_status"] == "not_tested" for r in rows))

    def test_metadata_does_not_become_verification(self):
        for r in self.data["repositories"]:
            d = details(r, self.data["meta"])
            self.assertEqual(d["sources"][0]["basis"], r["confidence"])
            self.assertEqual(d["when_to_use"], r["use_case"])
            self.assertEqual(d["sources"][0]["readme_sha"], r.get("readme_sha"))

    def test_reject_duplicate_ids(self):
        data = copy.deepcopy(self.data)
        data["repositories"][1]["id"] = data["repositories"][0]["id"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "catalog.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(AssertionError, "duplicate repository id"):
                load_catalog(path)

    def test_build_navigation_determinism_and_stale_cleanup(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory) / "site"
            build(ROOT, out)
            first = {p.relative_to(out): p.read_bytes() for p in out.rglob("*") if p.is_file()}
            self.assertEqual(sum(str(p).startswith("repos/") for p in first), len(self.data["repositories"]))
            for c in self.data["categories"]:
                shard = json.loads((out / "categories" / (c["id"] + ".json")).read_text())
                self.assertEqual(len(shard["repositories"]), c["count"])
            page = (out / "index.html").read_text()
            self.assertIn('href="/star/llms.txt"', page)
            self.assertIn('rel="describedby"', page)
            source_scripts = re.findall(r"<script[\s\S]*?</script>", (ROOT / "index.html").read_text())
            self.assertEqual(source_scripts, re.findall(r"<script[\s\S]*?</script>", page))
            self.assertEqual((out / "catalog.json").read_bytes(), (ROOT / "catalog.json").read_bytes())
            self.assertEqual((out / "jhny-kor-starred.xlsx").read_bytes(), (ROOT / "jhny-kor-starred.xlsx").read_bytes())
            (out / "repos/stale.md").write_text("obsolete")
            build(ROOT, out)
            second = {p.relative_to(out): p.read_bytes() for p in out.rglob("*") if p.is_file()}
            self.assertEqual(first, second)
            (out / "categories/index.md").write_text("[broken](missing.md)")
            with self.assertRaisesRegex(AssertionError, "broken link"):
                validate_links(out)

    def test_output_guard_and_markdown_text(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(AssertionError, "unmarked"):
                build(ROOT, Path(directory))
        self.assertNotIn("<script>", md("<script>[click](javascript:alert(1))"))
        self.assertIn(r"\[click\]", md("[click]"))


if __name__ == "__main__":
    unittest.main()
