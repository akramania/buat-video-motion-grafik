#!/usr/bin/env python3
"""Find direction recipes in the four researched style collections; does not render."""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
COLLECTION_DIR = ROOT / "assets" / "style_collections"
COLLECTIONS = ("bang-motion", "vox-explainer", "huashu-art-motion", "claude-drawing")
REQUIRED = ("id", "name", "origin", "source_url", "source_section", "visual", "motion", "use_case", "prompt")


def read_collections(selected: str | None = None) -> list[dict]:
    result = []
    for name in COLLECTIONS:
        if selected and selected != name:
            continue
        data = json.loads((COLLECTION_DIR / f"{name}.json").read_text(encoding="utf-8"))
        if data.get("collection_id") != name:
            raise ValueError(f"Collection ID does not match file: {name}")
        result.append(data)
    return result


def flatten(collections: list[dict]) -> list[dict]:
    result = []
    for collection in collections:
        for style in collection.get("styles", []):
            result.append({**style, "collection_id": collection["collection_id"]})
    return result


def stats(collections: list[dict]) -> dict:
    result = []
    for collection in collections:
        entries = collection.get("styles", [])
        result.append({
            "collection_id": collection["collection_id"],
            "collection_name": collection.get("collection_name", collection["collection_id"]),
            "recipe_count": len(entries),
            "by_origin": dict(Counter(s.get("origin", "unknown") for s in entries)),
            "by_group": dict(Counter(s.get("group", "style") for s in entries)),
        })
    return {"kind": "direction-recipes-not-render-presets", "total_recipes": sum(c["recipe_count"] for c in result), "collections": result}


def validate(collections: list[dict]) -> dict:
    errors = []
    seen = set()
    for collection in collections:
        cid = collection.get("collection_id", "unknown")
        if not collection.get("reviewed_on"):
            errors.append(f"{cid}: missing reviewed_on")
        if not collection.get("sources"):
            errors.append(f"{cid}: missing sources")
        if not collection.get("styles"):
            errors.append(f"{cid}: empty style collection")
        for style in collection.get("styles", []):
            sid = style.get("id", "<missing>")
            if sid in seen:
                errors.append(f"Duplicate style ID: {sid}")
            seen.add(sid)
            for field in REQUIRED:
                if not style.get(field):
                    errors.append(f"{sid}: missing {field}")
            if style.get("origin") not in {"native-source", "original-adaptation"}:
                errors.append(f"{sid}: invalid origin")
            if not str(style.get("source_url", "")).startswith("https://"):
                errors.append(f"{sid}: invalid source_url")
    return {"valid": not errors, "recipe_count": len(seen), "errors": errors}


def print_json(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("stats", "list", "search", "show", "validate"), nargs="?", default="stats")
    parser.add_argument("query", nargs="?", help="Search terms or one style ID")
    parser.add_argument("--collection", choices=COLLECTIONS)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be positive")
    if args.command in {"search", "show"} and not args.query:
        parser.error(f"{args.command} needs a query")
    try:
        collections = read_collections(args.collection)
        if args.command == "validate":
            report = validate(collections)
            print_json(report)
            return 0 if report["valid"] else 1
        if args.command == "stats":
            print_json(stats(collections))
            return 0
        entries = flatten(collections)
        if args.command == "show":
            matches = [s for s in entries if s["id"].casefold() == args.query.casefold()]
            if not matches:
                print(f"Style not found: {args.query}", file=sys.stderr)
                return 1
            print_json(matches[0])
            return 0
        if args.command == "search":
            words = args.query.casefold().split()
            entries = [s for s in entries if all(w in json.dumps(s, ensure_ascii=False).casefold() for w in words)]
        visible = entries[:args.limit]
        if args.json:
            print_json({"matched": len(entries), "shown": len(visible), "styles": visible})
        else:
            for style in visible:
                print(f"{style['id']} | {style['collection_id']} | {style['name']} | {style['origin']}")
            print(f"Shown {len(visible)} of {len(entries)} recipes. These are direction recipes, not renderer IDs.")
        return 0
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f"Cannot read style collections: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
