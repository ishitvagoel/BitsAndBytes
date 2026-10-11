#!/usr/bin/env python3
"""Run every fenced Python block in the guide and match blocks that declare their output."""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
checked = 0
for path in sorted((ROOT / "guide").glob("*.md")):
    text = path.read_text()
    for block in re.findall(r"```python\n(.*?)```", text, re.S):
        expected = None
        for line in block.splitlines():
            if line.startswith("# prints:"):
                expected = line.removeprefix("# prints:").strip()
        result = subprocess.run(
            [sys.executable, "-c", block],
            cwd=ROOT,
            env={**dict(**{k: v for k, v in __import__("os").environ.items()}), "PYTHONPATH": str(ROOT)},
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"{path.name}: block failed\n{result.stderr}")
            sys.exit(1)
        if expected is None:
            continue
        actual = result.stdout.strip()
        if actual != expected:
            print(f"{path.name}: expected {expected!r} but printed {actual!r}")
            sys.exit(1)
        checked += 1

print(f"lesson code: {checked} blocks ran")
