"""Shared, dependency-free catalog validation and normalization."""
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://jhny-kor.github.io/star/"
FIELDS = ("when_not_to_use", "integration_modes", "runtime_requirements",
          "network_requirements", "inputs", "outputs")


def normalize(value):
    return unicodedata.normalize("NFKC", str(value)).casefold()


def load_catalog(path=ROOT / "catalog.json"):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    categories = data["categories"]
    ids = [c["id"] for c in categories]
    assert len(ids) == len(set(ids)), "duplicate category"
    assert all(re.fullmatch(r"[a-z0-9_]+", c) for c in ids), "unsafe category"
    repos = data["repositories"]
    assert len({r["id"] for r in repos}) == len(repos), "duplicate repository id"
    assert len({r["full_name"].casefold() for r in repos}) == len(repos), "duplicate name"
    for r in repos:
        assert re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", r["full_name"]), "unsafe name"
        assert all(p not in (".", "..") for p in r["full_name"].split("/")), "unsafe path"
        assert r["category"] in ids, "unknown category"
        assert r["url"] == "https://github.com/" + r["full_name"], "unexpected URL"
        assert r["readme_url"].startswith(r["url"] + "/"), "unexpected README URL"
        assert r["confidence"] in ("readme", "metadata", "uncertain"), "unknown confidence"
    assert data["meta"]["total_repositories"] == len(repos), "wrong total"
    for c in categories:
        assert c["count"] == sum(r["category"] == c["id"] for r in repos), "wrong category count"
    return data


def details(repo, meta):
    result = dict(repo)
    result.update({field: None for field in FIELDS})
    result.update(when_to_use=repo["use_case"], checked_at=None,
                  test_status="not_tested", collected_at=meta["as_of_kst"],
                  sources=[{"url": repo["readme_url"], "readme_sha": repo.get("readme_sha"),
                            "basis": repo["confidence"]}],
                  detail_url=SITE + "repos/" + repo["full_name"] + ".md")
    return result
