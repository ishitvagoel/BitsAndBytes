#!/usr/bin/env python3
"""Generate the website's interactive binary-search traces from Python cases."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bitsandbytes.search.binary_search import binary_search_trace


def build() -> list[dict[str, object]]:
    inputs = json.loads((ROOT / "tests/fixtures/binary_search_scenarios.json").read_text(encoding="utf-8"))
    scenarios = []
    for item in inputs:
        result, frames = binary_search_trace(item["values"], item["target"])
        scenarios.append({**item, "result": result, "frames": frames})
    return scenarios


def build_source_excerpt() -> dict[str, object]:
    source_path = ROOT / "bitsandbytes/search/binary_search.py"
    lines = source_path.read_text(encoding="utf-8").splitlines()
    start_marker = "# BEGIN LEARNING EXCERPT: binary-search"
    end_marker = "# END LEARNING EXCERPT: binary-search"
    starts = [index for index, line in enumerate(lines) if line.strip() == start_marker]
    ends = [index for index, line in enumerate(lines) if line.strip() == end_marker]
    if len(starts) != 1 or len(ends) != 1 or ends[0] <= starts[0]:
        raise ValueError("Binary-search source excerpt markers must appear exactly once and in order")

    code_lines: list[str] = []
    trace_lines: dict[str, list[int]] = {}
    current_step: str | None = None
    for line in lines[starts[0] + 1 : ends[0]]:
        marker = line.strip()
        if marker.startswith("# TRACE:"):
            current_step = marker.removeprefix("# TRACE:")
            if not current_step or current_step in trace_lines:
                raise ValueError(f"Invalid or repeated trace marker: {marker}")
            trace_lines[current_step] = []
            continue
        code_lines.append(line)
        if current_step and line.strip():
            trace_lines[current_step].append(len(code_lines) - 1)

    required_steps = {"initialize", "compare-left", "narrow-left", "compare-right", "narrow-right", "return-match", "return-absent"}
    if not code_lines or required_steps - trace_lines.keys() or any(not trace_lines[step] for step in required_steps):
        raise ValueError("Source excerpt is empty or missing a required trace-line mapping")
    return {
        "sourcePath": "bitsandbytes/search/binary_search.py",
        "code": "\n".join(code_lines).strip(),
        "traceLines": trace_lines,
    }


def main() -> int:
    output_dir = ROOT / "site/src/data"
    output_dir.mkdir(parents=True, exist_ok=True)
    traces_path = output_dir / "binary-search-traces.json"
    source_path = output_dir / "binary-search-source.json"
    traces_path.write_text(json.dumps(build(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    source_path.write_text(json.dumps(build_source_excerpt(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {traces_path.relative_to(ROOT)} and {source_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
