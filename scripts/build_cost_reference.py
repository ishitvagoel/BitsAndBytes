#!/usr/bin/env python3
"""Emit one reference row for each public function that states a Cost block."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "bitsandbytes"
GUIDE = ROOT / "guide"
CURRICULUM = ROOT / "site" / "src" / "lib" / "curriculum.ts"
OUTPUT = ROOT / "site" / "src" / "data" / "cost-reference.json"
BOUND = re.compile(r"(?:O|Θ|Ω)\((?:[^()]|\([^)]*\))*\)")


def lesson_order() -> tuple[list[str], set[str]]:
    text = CURRICULUM.read_text(encoding="utf-8")
    stages = re.search(r"export const curriculumStages:[\s\S]*?\n\];", text)
    if stages is None:
        raise SystemExit("curriculum stages not found")
    ordered: list[str] = []
    reference: set[str] = set()
    for match in re.finditer(
        r'id:\s*"([^"]+)"[\s\S]*?slugs:\s*\[([^\]]*)\]',
        stages.group(0),
    ):
        slugs = re.findall(r'"([a-z0-9-]+)"', match.group(2))
        ordered.extend(slugs)
        if match.group(1) == "reference":
            reference.update(slugs)
    return ordered, reference


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        raise SystemExit("guide file is missing front matter")
    parts = text.split("---", 2)
    data: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def lesson_index() -> dict[str, tuple[str, str]]:
    """Map a module name to the earliest sequence lesson that names it."""
    order, reference = lesson_order()
    rank = {slug: index for index, slug in enumerate(order)}
    chosen: dict[str, tuple[int, str, str]] = {}
    for path in sorted(GUIDE.glob("*.md")):
        meta = frontmatter(path.read_text(encoding="utf-8"))
        slug = meta.get("slug", "")
        title = meta.get("title", "")
        if slug not in rank:
            raise SystemExit(f"{path.name} slug {slug} is not in curriculum.ts")
        priority = rank[slug] + (len(order) if slug in reference else 0)
        for module in meta.get("module", "").split(","):
            name = module.strip()
            if not name:
                continue
            current = chosen.get(name)
            if current is None or priority < current[0]:
                chosen[name] = (priority, slug, title)
    return {module: (slug, title) for module, (_, slug, title) in chosen.items()}


def module_name(path: Path) -> str:
    parts = list(path.relative_to(LIBRARY).parts)
    if parts[-1] == "__init__.py":
        parts = parts[:-1]
    else:
        parts[-1] = parts[-1].removesuffix(".py")
    return "bitsandbytes" if not parts else "bitsandbytes." + ".".join(parts)


def is_public(name: str) -> bool:
    if name.startswith("__") and name.endswith("__"):
        return True
    return not name.startswith("_")


def cost_section(docstring: str) -> str:
    marker = docstring.find("Cost\n----")
    if marker < 0:
        return ""
    return docstring[marker + len("Cost\n----") :].strip()


TIME_BEFORE = re.compile(rf"({BOUND.pattern})\s+time\b", re.IGNORECASE)
TIME_AFTER = re.compile(rf"\btime(?:\s+is|\s+of)?\s+({BOUND.pattern})", re.IGNORECASE)


def first_time_bound(section: str) -> str:
    text = " ".join(section.split())
    for pattern in (TIME_BEFORE, TIME_AFTER):
        match = pattern.search(text)
        if match is not None:
            return match.group(1)
    match = BOUND.search(text)
    if match is not None:
        return match.group(0)
    clause = re.split(r"[,.]", text, maxsplit=1)[0].strip()
    if not clause:
        raise SystemExit(f"Cost block has no time bound: {section[:80]}")
    return clause


def memory_line(section: str) -> str:
    text = " ".join(section.split())
    for sentence in re.split(r"(?<=\.)\s+", text):
        if "memory" in sentence.lower():
            return sentence.strip()
    return "not stated"


def collect_rows(lessons: dict[str, tuple[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    missing: list[str] = []
    for path in sorted(LIBRARY.rglob("*.py")):
        module = module_name(path)
        tree = ast.parse(path.read_text(encoding="utf-8"))
        visit(tree, None, False, module, lessons, rows, missing)
    if missing:
        unique = sorted(set(missing))
        raise SystemExit("modules with Cost blocks and no lesson:\n" + "\n".join(unique))
    rows.sort(key=lambda row: (row["module"], row["name"]))
    return rows


def visit(
    node: ast.AST,
    class_name: str | None,
    nested: bool,
    module: str,
    lessons: dict[str, tuple[str, str]],
    rows: list[dict[str, str]],
    missing: list[str],
) -> None:
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.ClassDef):
            if nested:
                visit(child, class_name, True, module, lessons, rows, missing)
            else:
                visit(child, child.name, False, module, lessons, rows, missing)
            continue
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            section = cost_section(ast.get_docstring(child) or "")
            if not nested and is_public(child.name) and section:
                lesson = lessons.get(module)
                if lesson is None:
                    missing.append(module)
                else:
                    slug, title = lesson
                    label = child.name if class_name is None else f"{class_name}.{child.name}"
                    rows.append(
                        {
                            "module": module,
                            "name": label,
                            "time": first_time_bound(section),
                            "memory": memory_line(section),
                            "lessonSlug": slug,
                            "lessonTitle": title,
                        }
                    )
            visit(child, class_name, True, module, lessons, rows, missing)
            continue
        visit(child, class_name, nested, module, lessons, rows, missing)


def payload() -> dict[str, object]:
    rows = collect_rows(lesson_index())
    return {"count": len(rows), "rows": rows}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    document = payload()
    text = json.dumps(document, indent=2) + "\n"
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != text:
            raise SystemExit("cost reference is stale. Run python3 scripts/build_cost_reference.py")
        print(f"cost reference: {document['count']} rows")
        return
    OUTPUT.write_text(text, encoding="utf-8")
    print(f"cost reference: {document['count']} rows")


if __name__ == "__main__":
    try:
        main()
    except SystemExit as exc:
        if exc.code not in (None, 0):
            print(exc.code if isinstance(exc.code, str) else "cost reference failed", file=sys.stderr)
            sys.exit(1)
        raise
