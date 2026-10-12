#!/usr/bin/env python3
"""Fail on cut-off sentences in sequence lessons."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "guide"
CURRICULUM = (ROOT / "site/src/lib/curriculum.ts").read_text()
stages = re.search(r"export const curriculumStages:[\s\S]*?\n\];", CURRICULUM)
if stages is None:
    raise SystemExit("curriculum stages not found")
sequence: set[str] = set()
for match in re.finditer(r"id:\s*\"([^\"]+)\"[\s\S]*?slugs:\s*\[([^\]]*)\]", stages.group(0)):
    if match.group(1) == "reference":
        continue
    sequence.update(re.findall(r'"([a-z0-9-]+)"', match.group(2)))

VERBS = ("is", "are", "was", "has", "have", "does", "do", "can", "moves", "returns", "holds")
ALLOW = {"Order matters."}
STARTERS = ("Because ", "Which ", "Then ", "So ", "Θ(", "O(")
failures: list[str] = []
checked = 0


def sentences(text: str) -> list[str]:
    found: list[str] = []
    fenced = False
    for line in text.splitlines():
        if line.startswith("```"):
            fenced = not fenced
            continue
        if fenced or not line.strip() or line[0] in "|*#-" or line.strip().startswith("[[") or re.match(r"^\d+\.", line.strip()):
            continue
        for sentence in re.split(r"(?<=[.?!])\s+", line.strip()):
            sentence = sentence.strip()
            if sentence:
                found.append(sentence)
    return found


for path in sorted(GUIDE.glob("*.md")):
    raw = path.read_text()
    parts = raw.split("---", 2)
    if len(parts) < 3:
        continue
    slug_match = re.search(r"^slug:\s*(\S+)", parts[1], re.M)
    if slug_match is None or slug_match.group(1) not in sequence:
        continue
    body = parts[2]
    seen: set[str] = set()
    for sentence in sentences(body):
        checked += 1
        words = sentence.split()
        if sentence in seen:
            failures.append(f"{path.name}: duplicate sentence: {sentence[:80]}")
        seen.add(sentence)
        if "' s" in sentence:
            failures.append(f"{path.name}: spaced apostrophe: {sentence[:80]}")
        if re.match(r"^[A-Z][a-z]+_[A-Za-z0-9_]+", sentence):
            failures.append(f"{path.name}: identifier sentence: {sentence[:80]}")
        first = words[0] if words else ""
        english_fragment = {"because", "which", "then", "so", "and", "but", "the", "a", "an", "it", "this", "that", "when", "if"}
        if first[:1].islower() and first.lower().strip(".,") in english_fragment:
            failures.append(f"{path.name}: lowercase sentence: {sentence[:80]}")
        if len(words) <= 2 and sentence not in ALLOW:
            failures.append(f"{path.name}: short sentence: {sentence}")
        if sentence.startswith(STARTERS) and not any(re.search(rf"\b{verb}\b", sentence) for verb in VERBS):
            failures.append(f"{path.name}: fragment: {sentence[:80]}")
    cost = re.search(r"## What it costs\n+([\s\S]*?)(?=\n## |\Z)", body)
    if cost and slug_match.group(1) not in {"binary-search", "binary-search-on-answer", "input-size-and-operation-counts"}:
        block = cost.group(1)
        if "Θ" not in block and "O(" not in block:
            failures.append(f"{path.name}: cost section has no bound")
        if "memory" not in block.lower() and "space" not in block.lower():
            failures.append(f"{path.name}: cost section does not mention memory")

if failures:
    print("\n".join(failures[:40]))
    print(f"prose: {checked} sentences checked, {len(failures)} failures")
    sys.exit(1)
print(f"prose: {checked} sentences checked, 0 failures")
