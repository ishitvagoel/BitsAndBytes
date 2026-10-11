#!/usr/bin/env python3
"""Fail when a sequence lesson uses a term before the lesson that defines it."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURRICULUM = ROOT / "site/src/lib/curriculum.ts"
GUIDE = ROOT / "guide"

# Term pattern, defining slug. O matches big-O calls such as O(n), not the word "of".
TERMS: list[tuple[str, str, re.Pattern[str]]] = [
    ("Θ", "asymptotic-growth", re.compile("Θ")),
    ("O", "asymptotic-growth", re.compile(r"\bO\([^)]*\)")),
    ("invariant", "loop-invariants", re.compile(r"\binvariant\b", re.I)),
    ("amortized", "dynamic-array-growth", re.compile(r"\bamortized\b", re.I)),
    ("stable", "comparison-sorts", re.compile(r"\bstable\b", re.I)),
    ("load factor", "hash-chaining", re.compile(r"\bload factor\b", re.I)),
    ("complete tree", "heap-operations", re.compile(r"\bcomplete tree\b", re.I)),
]


def sequence() -> list[tuple[str, list[str]]]:
    text = CURRICULUM.read_text()
    stages = re.search(r"export const curriculumStages:[\s\S]*?\n\];", text)
    if stages is None:
        raise SystemExit("curriculum stages not found")
    body = stages.group(0).split('id: "reference"', 1)[0]
    ordered: list[str] = []
    for match in re.finditer(r"slugs:\s*\[([^\]]*)\]", body):
        ordered.extend(re.findall(r'"([a-z0-9-]+)"', match.group(1)))
    prerequisites: dict[str, list[str]] = {}
    for slug in ordered:
        block = re.search(rf'"{re.escape(slug)}": \{{[^{{}}]*prerequisites: \[([^\]]*)\]', text)
        if block is None:
            raise SystemExit(f"missing prerequisites for {slug}")
        prerequisites[slug] = re.findall(r'"([a-z0-9-]+)"', block.group(1))
    return [(slug, prerequisites[slug]) for slug in ordered]


def guide_body(slug: str) -> str:
    matches = [
        path
        for path in GUIDE.glob("*.md")
        if path.stem.partition("-")[0].isdigit() and path.stem.partition("-")[2] == slug
    ]
    if len(matches) != 1:
        raise SystemExit(f"expected one guide file for {slug}, found {matches}")
    parts = matches[0].read_text().split("---", 2)
    return parts[-1]


def main() -> int:
    rows = sequence()
    index = {slug: position for position, (slug, _) in enumerate(rows)}
    failed = False
    for slug, prerequisites in rows:
        body = guide_body(slug)
        visible = re.sub(r"```.*?```", lambda match: " " * len(match.group(0)), body, flags=re.S)
        for label, defining, pattern in TERMS:
            if slug == defining:
                continue
            if defining in prerequisites:
                continue
            if index[slug] > index[defining]:
                continue
            found = pattern.search(visible)
            if found:
                print(f"{slug}: uses {label!r} before {defining} ({found.group(0)!r})")
                failed = True
    if failed:
        return 1
    print("first use:")
    for label, defining, _pattern in TERMS:
        print(f"  {label} -> {defining}")
    print(f"  checked {len(rows)} sequence lessons")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
