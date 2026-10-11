#!/usr/bin/env python3
"""Fail when a checkpoint answer is copied from the trace, or an objective has no exercise."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
traces = json.loads((ROOT / "site/src/data/lesson-traces.json").read_text())
exercises = json.loads((ROOT / "site/src/data/exercises.json").read_text())
curriculum = (ROOT / "site/src/lib/curriculum.ts").read_text()
objectives: dict[str, list[str]] = {}
for match in re.finditer(r'"([a-z0-9-]+)":\s*\[((?:"[a-z0-9-]+"(?:,\s*)?)*)\]', curriculum):
    slug, body = match.group(1), match.group(2)
    if slug not in traces:
        continue
    objectives[slug] = re.findall(r'"([a-z0-9-]+)"', body)

failed = False
for slug, scenes in traces.items():
    cells: set[str] = set()
    for scene in scenes:
        for frame in scene["frames"]:
            for entry in frame["state"]:
                cells.add(str(entry["value"]))
            for row in frame["rows"]:
                for cell in row["cells"]:
                    cells.add(str(cell["text"]))
    lesson_exercises = [item for item in exercises if item["lessonSlug"] == slug]
    covered = {item["objectiveId"] for item in lesson_exercises}
    for objective_id in objectives.get(slug, []):
        if objective_id not in covered:
            print(f"{slug}: objective {objective_id} has no exercise")
            failed = True
    for item in lesson_exercises:
        if item.get("kind") in {"fill-cell", "predict-output"}:
            continue
        label = next(option["label"] for option in item["options"] if option["id"] == item["answer"])
        if label in cells:
            print(f"{slug}: answer {label!r} is copied from the trace")
            failed = True

if failed:
    sys.exit(1)
print(f"checkpoints: {len(traces)} lessons, answers are not trace cells")
