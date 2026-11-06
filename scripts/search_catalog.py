#!/usr/bin/env python3
"""Search local catalog; never fetch or execute repository content."""
import argparse
import json
from catalog_tools import ROOT, details, load_catalog, normalize


def search(data, query="", category=None, limit=5):
    tokens = normalize(query).split()
    names = {c["id"]: c["name"] for c in data["categories"]}
    if category and category not in names:
        raise ValueError("Unknown category: " + category)
    rows = []
    for r in data["repositories"]:
        if category and r["category"] != category:
            continue
        text = normalize(" ".join([r["full_name"], r["summary"], r["use_case"],
                                   *r["keywords"], *r["topics"], names[r["category"]],
                                   r.get("language") or "", r["kind"]]))
        if all(t in text for t in tokens):
            rows.append(details(r, data["meta"]))
    return rows[:limit]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("query", nargs="?", default="")
    p.add_argument("--catalog", default=ROOT / "catalog.json")
    p.add_argument("--category")
    p.add_argument("--limit", type=int, default=5)
    args = p.parse_args()
    if not 1 <= args.limit <= 50:
        p.error("--limit must be between 1 and 50")
    try:
        rows = search(load_catalog(args.catalog), args.query, args.category, args.limit)
    except ValueError as error:
        p.error(str(error))
    print(json.dumps(rows, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
