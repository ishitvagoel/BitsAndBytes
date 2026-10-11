#!/usr/bin/env python3
"""Fail when a public function or method has no Cost heading."""

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "bitsandbytes"
missing: list[str] = []

def visit(path: Path, node: ast.AST, nested: bool) -> None:
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            public = not child.name.startswith("_") and child.name != "__init__"
            docstring = ast.get_docstring(child) or ""
            if public and not nested and "Cost\n----" not in docstring:
                missing.append(f"{path.relative_to(ROOT.parent)}:{child.lineno} {child.name}")
            visit(path, child, True)
        else:
            visit(path, child, nested)


for path in sorted(ROOT.rglob("*.py")):
    visit(path, ast.parse(path.read_text()), False)

if missing:
    print(f"cost docstrings: {len(missing)} missing")
    print("\n".join(missing))
    sys.exit(1)
print("cost docstrings: 0 missing")
