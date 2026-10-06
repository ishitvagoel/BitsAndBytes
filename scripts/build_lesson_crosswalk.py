#!/usr/bin/env python3
"""Build an auditable guide → module → public symbol → test import map."""

from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "guide"
TESTS = ROOT / "tests"
OUTPUT = ROOT / "docs" / "module-function-test-lesson-crosswalk.md"


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        raise ValueError("missing frontmatter")
    parts = text.split("---", 2)
    if len(parts) != 3:
        raise ValueError("unclosed frontmatter")
    data: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
    return data


def public_symbols(module_path: Path) -> list[str]:
    tree = ast.parse(module_path.read_text(encoding="utf-8"))
    return [
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        and not node.name.startswith("_")
    ]


def test_imports(target_module: str, symbols: list[str], test_paths: list[Path]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for test_path in test_paths:
        tree = ast.parse(test_path.read_text(encoding="utf-8"))
        mapped: set[str] = set()
        module_import = False
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                imported_module = node.module
                if target_module == imported_module or target_module.startswith(imported_module + "."):
                    mapped.update(alias.name for alias in node.names if alias.name in symbols)
                    module_import |= any(alias.name == "*" for alias in node.names)
            elif isinstance(node, ast.Import):
                if any(
                    alias.name == target_module
                    or target_module.startswith(alias.name + ".")
                    for alias in node.names
                ):
                    module_import = True
        if mapped or module_import:
            result[test_path.name] = sorted(mapped) if mapped else ["module-level import"]
    return result


def main() -> int:
    test_paths = sorted(TESTS.glob("test_*.py"))
    rows: list[tuple[str, str, str, str, str]] = []
    lesson_references: dict[str, dict[str, object]] = {}
    for guide_path in sorted(GUIDE.glob("*.md")):
        meta = frontmatter(guide_path.read_text(encoding="utf-8"))
        title = meta["title"]
        modules = [part.strip() for part in meta["module"].split(",")]
        module_references = []
        for module in modules:
            source_path = ROOT.joinpath(*module.split(".")).with_suffix(".py")
            if not source_path.is_file():
                raise FileNotFoundError(f"{guide_path.name}: source module not found: {module}")
            symbols = public_symbols(source_path)
            imports = test_imports(module, symbols, test_paths)
            module_references.append({
                "module": module,
                "sourcePath": source_path.relative_to(ROOT).as_posix(),
                "symbols": symbols,
                "testsBySymbol": {
                    symbol: [test_name for test_name, imported in imports.items() if symbol in imported]
                    for symbol in symbols
                },
                "testPaths": sorted(imports),
            })
            if symbols:
                symbol_map = "<br>".join(
                    f"`{symbol}` → " + ", ".join(
                        f"[`{test_name}`]({(Path('..') / 'tests' / test_name).as_posix()})"
                        for test_name, imported in imports.items()
                        if symbol in imported
                    )
                    if any(symbol in imported for imported in imports.values())
                    else f"`{symbol}` → no direct test import identified"
                    for symbol in symbols
                )
            else:
                symbol_map = "No public top-level functions/classes identified."
            import_coverage = ", ".join(
                f"[`{test_name}`]({(Path('..') / 'tests' / test_name).as_posix()})"
                for test_name in imports
            ) or "No direct test import identified"
            rows.append((title, guide_path.name, module, symbol_map, import_coverage))
        lesson_slug = meta["slug"]
        if lesson_slug in lesson_references:
            raise ValueError(f"duplicate guide slug: {lesson_slug}")
        lesson_references[lesson_slug] = {"modules": module_references}

    lines = [
        "# Module → function/class → test → lesson crosswalk",
        "",
        "Generated from guide frontmatter, Python AST declarations and imports in `tests/test_*.py` by `scripts/build_lesson_crosswalk.py`.",
        "",
        "**How to read this:** each public top-level function/class is mapped to test files that import that symbol directly or through a parent package re-export. ‘No direct test import identified’ is a coverage gap to review; an import alone does not prove every behavior is asserted. Private helpers and class methods are omitted from the symbol list.",
        "",
        "| Lesson | Module | Public function/class → test file(s) | Test files importing module symbols |",
        "|---|---|---|---|",
    ]
    for title, slug, module, symbol_map, import_coverage in rows:
        lesson = f"[{title}](../guide/{slug})"
        lines.append(f"| {lesson} | `{module}` | {symbol_map} | {import_coverage} |")
    lines.extend([
        "",
        "## Coverage follow-up",
        "",
        "Treat each ‘no direct test import’ entry as an explicit review task. Some modules are represented by aggregate tests or package re-exports, and generated mapping is a navigation aid rather than a statement of test adequacy. Add focused tests where a lesson teaches behavior not currently asserted.",
        "",
    ])
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    references_path = ROOT / "site/src/data/lesson-references.json"
    references_path.parent.mkdir(parents=True, exist_ok=True)
    references_path.write_text(json.dumps(lesson_references, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)} and {references_path.relative_to(ROOT)} ({len(rows)} module mappings)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
