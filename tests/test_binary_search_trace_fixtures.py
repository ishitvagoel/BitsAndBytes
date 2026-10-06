"""Keep the interactive website frames derived from the Python behavior."""

from __future__ import annotations

import json
from itertools import combinations_with_replacement
from pathlib import Path

from bitsandbytes.search.binary_search import binary_search, binary_search_trace
from scripts.build_binary_search_traces import build_source_excerpt

ROOT = Path(__file__).resolve().parents[1]


def test_website_trace_fixtures_match_python_trace_and_search() -> None:
    scenarios = json.loads((ROOT / "site/src/data/binary-search-traces.json").read_text(encoding="utf-8"))
    for scenario in scenarios:
        result, frames = binary_search_trace(scenario["values"], scenario["target"])
        assert result == scenario["result"]
        assert result == binary_search(scenario["values"], scenario["target"])
        assert frames == scenario["frames"]


def test_website_source_excerpt_and_highlights_match_marked_python_source() -> None:
    source_fixture = json.loads((ROOT / "site/src/data/binary-search-source.json").read_text(encoding="utf-8"))
    expected_source = build_source_excerpt()
    assert source_fixture == expected_source
    code_line_count = len(source_fixture["code"].splitlines())
    assert all(0 <= line < code_line_count for lines in source_fixture["traceLines"].values() for line in lines)
    scenarios = json.loads((ROOT / "site/src/data/binary-search-traces.json").read_text(encoding="utf-8"))
    assert all(frame["codeStep"] in source_fixture["traceLines"] for item in scenarios for frame in item["frames"])


def test_trace_separates_comparison_from_range_narrowing() -> None:
    result, frames = binary_search_trace([1, 3, 5, 7, 9], 7)
    assert result == 3
    compare = next(index for index, frame in enumerate(frames) if frame["codeStep"] == "compare-left")
    compared, narrowed = frames[compare], frames[compare + 1]
    assert compared["left"] == 0
    assert compared["right"] == 4
    assert compared["middle"] == 2
    assert compared["inspected"] == 2
    assert narrowed["codeStep"] == "narrow-left"
    assert (narrowed["left"], narrowed["right"]) == (3, 4)


def test_small_sorted_inputs_keep_trace_ranges_and_results_consistent() -> None:
    for length in range(7):
        for values in combinations_with_replacement(range(-1, 3), length):
            for target in range(-2, 4):
                result, frames = binary_search_trace(values, target)
                assert result == binary_search(values, target)
                assert frames[0]["codeStep"] == "initialize"
                assert frames[-1]["result"] in {"found", "missing"}
                for index, frame in enumerate(frames):
                    if frame["codeStep"] not in {"compare-left", "compare-right"}:
                        continue
                    assert frame["left"] <= frame["middle"] <= frame["right"]
                    narrowed = frames[index + 1]
                    assert narrowed["inspected"] == frame["middle"]
                    assert narrowed["left"] <= narrowed["right"] or narrowed["result"] == "continue"
                    if frame["codeStep"] == "compare-left":
                        assert narrowed["codeStep"] == "narrow-left"
                        assert narrowed["left"] == frame["middle"] + 1
                        assert narrowed["right"] == frame["right"]
                    else:
                        assert narrowed["codeStep"] == "narrow-right"
                        assert narrowed["left"] == frame["left"]
                        assert narrowed["right"] == frame["middle"] - 1
