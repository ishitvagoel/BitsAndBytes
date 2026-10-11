#!/usr/bin/env python3
"""Import every package export and require public classes to be listed."""

import ast
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Node and frame helpers are implementation types, not lesson entry points.
ALLOW = {"SkipNode", "PersistentStackFrame", "LLRBNode"}
ROOT_REQUIRED = {
    "DynamicArray",
    "LinkedQueue",
    "LinkedDeque",
    "ChainingHashTable",
    "LinearProbingHashTable",
    "BinarySearchTree",
    "PriorityQueue",
    "Graph",
    "DisjointSet",
}

package_count = 0
class_count = 0
failed = False
for init in sorted((ROOT / "bitsandbytes").rglob("__init__.py")):
    package = ".".join(init.relative_to(ROOT).with_suffix("").parts)
    if package.endswith(".__init__"):
        package = package[: -len(".__init__")]
    module = importlib.import_module(package)
    exported = set(getattr(module, "__all__", []))
    for name in exported:
        getattr(module, name)
    package_count += 1
    if package == "bitsandbytes":
        missing = ROOT_REQUIRED - exported
        if missing:
            print(f"root package is missing {sorted(missing)}")
            sys.exit(1)
        continue
    for path in init.parent.glob("*.py"):
        if path.name == "__init__.py":
            continue
        tree = ast.parse(path.read_text())
        for node in tree.body:
            if not isinstance(node, ast.ClassDef) or node.name.startswith("_") or node.name in ALLOW:
                continue
            class_count += 1
            if node.name not in exported:
                print(f"{package} omits public class {node.name} from {path.name}")
                failed = True

if failed:
    sys.exit(1)
print(f"exports: {package_count} packages, {class_count} public classes")
