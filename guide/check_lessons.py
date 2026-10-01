#!/usr/bin/env python3
"""Validate guide lesson frontmatter and importable modules."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

REQUIRED_KEYS = ("title", "slug", "order", "status", "module")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        raise ValueError("missing YAML frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("unclosed YAML frontmatter")
    result: dict[str, str] = {}
    for line in parts[1].strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()
    return result


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    guide_dir = Path(__file__).resolve().parent
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    md_files = sorted(guide_dir.glob("*.md"))
    if not md_files:
        print("check_lessons: no lesson files found", file=sys.stderr)
        return 1

    orders: list[int] = []
    for path in md_files:
        text = path.read_text(encoding="utf-8")
        try:
            meta = parse_frontmatter(text)
        except ValueError as exc:
            print(f"check_lessons: {path.name}: {exc}", file=sys.stderr)
            return 1

        for key in REQUIRED_KEYS:
            if key not in meta:
                print(f"check_lessons: {path.name}: missing key '{key}'", file=sys.stderr)
                return 1

        if meta["status"] != "present":
            print(f"check_lessons: {path.name}: status must be 'present'", file=sys.stderr)
            return 1

        try:
            order = int(meta["order"])
        except ValueError:
            print(f"check_lessons: {path.name}: order must be an integer", file=sys.stderr)
            return 1
        orders.append(order)

        for mod in meta["module"].split(","):
            mod = mod.strip()
            if not mod:
                print(f"check_lessons: {path.name}: empty module name", file=sys.stderr)
                return 1
            try:
                importlib.import_module(mod)
            except Exception as exc:
                print(f"check_lessons: {path.name}: cannot import '{mod}': {exc}", file=sys.stderr)
                return 1

    if len(orders) != len(set(orders)):
        print("check_lessons: duplicate order values", file=sys.stderr)
        return 1

    count = len(md_files)
    print(f"check_lessons: ok ({count} lesson file(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
