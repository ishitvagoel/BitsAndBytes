import assert from "node:assert/strict";
import {
  emptyLearningProgress,
  recordLessonVisit,
  recordObjectiveAttempt,
  validateLearningProgress,
  validateLearningProgressImport,
} from "../src/lib/learning-progress.ts";

const config = {
  "binary-search": {
    contentVersion: 1,
    sectionIds: ["trace"],
    objectiveIds: ["binary-search-justify-elimination"],
  },
};
const start = new Date("2026-10-06T12:00:00.000Z");

let progress = recordLessonVisit(emptyLearningProgress(), "binary-search", config["binary-search"], "trace", start);
assert.equal(progress.lessons["binary-search"].visitedAt, start.toISOString());
assert.equal(progress.lessons["binary-search"].lastSectionId, "trace");

progress = recordObjectiveAttempt(
  progress,
  "binary-search",
  config["binary-search"],
  "binary-search-justify-elimination",
  false,
  start,
);
let objective = progress.lessons["binary-search"].objectives["binary-search-justify-elimination"];
assert.equal(objective.attempts, 1);
assert.equal(objective.lastResult, "retry");
assert.equal(objective.nextReviewAt, "2026-10-07T12:00:00.000Z");
assert.equal(objective.reviewPassedAt, null);

const reviewTime = new Date("2026-10-07T12:00:00.000Z");
progress = recordObjectiveAttempt(
  progress,
  "binary-search",
  config["binary-search"],
  "binary-search-justify-elimination",
  true,
  reviewTime,
);
objective = progress.lessons["binary-search"].objectives["binary-search-justify-elimination"];
assert.equal(objective.attempts, 2);
assert.equal(objective.lastResult, "correct");
assert.equal(objective.reviewPassedAt, reviewTime.toISOString());
assert.equal(objective.nextReviewAt, "2026-10-14T12:00:00.000Z");

const changed = validateLearningProgress(progress, {
  "binary-search": { ...config["binary-search"], contentVersion: 2 },
});
assert.equal(changed.lessons["binary-search"].needsRecheck, true);
assert.equal(changed.lessons["binary-search"].objectives["binary-search-justify-elimination"].attempts, 2);
assert.deepEqual(validateLearningProgress({ schemaVersion: 99, lessons: {} }, config), emptyLearningProgress());

const updatedConfig = {
  "binary-search": {
    contentVersion: 2,
    sectionIds: ["trace", "practice-section"],
    objectiveIds: ["first", "second", "new-objective"],
  },
};
const allObjectivesAtVersionOne = { ...config["binary-search"], objectiveIds: updatedConfig["binary-search"].objectiveIds };
let updatedProgress = recordLessonVisit(emptyLearningProgress(), "binary-search", allObjectivesAtVersionOne, "trace", start);
updatedProgress = recordObjectiveAttempt(updatedProgress, "binary-search", allObjectivesAtVersionOne, "first", true, start);
updatedProgress = recordObjectiveAttempt(updatedProgress, "binary-search", allObjectivesAtVersionOne, "second", true, start);
let needsRecheck = validateLearningProgress(updatedProgress, updatedConfig);
assert.equal(needsRecheck.lessons["binary-search"].needsRecheck, true);
updatedProgress = recordObjectiveAttempt(needsRecheck, "binary-search", updatedConfig["binary-search"], "first", false, start);
needsRecheck = validateLearningProgress(updatedProgress, updatedConfig);
assert.equal(needsRecheck.lessons["binary-search"].needsRecheck, true, "one wrong response cannot clear other required objectives");
assert.equal(needsRecheck.lessons["binary-search"].objectives.first.attempts, 2);
updatedProgress = recordObjectiveAttempt(needsRecheck, "binary-search", updatedConfig["binary-search"], "second", true, start);
updatedProgress = recordObjectiveAttempt(updatedProgress, "binary-search", updatedConfig["binary-search"], "new-objective", true, start);
needsRecheck = validateLearningProgress(updatedProgress, updatedConfig);
assert.equal(needsRecheck.lessons["binary-search"].needsRecheck, false, "all current objectives must be checked before acknowledging the new version");
assert.equal(needsRecheck.lessons["binary-search"].contentVersion, 2);

assert.equal(validateLearningProgressImport({ schemaVersion: 99, lessons: {} }, config), null);
assert.equal(validateLearningProgressImport({ schemaVersion: 1, lessons: { "unknown-lesson": {} } }, config), null);
assert.equal(validateLearningProgressImport(updatedProgress, updatedConfig)?.lessons["binary-search"].contentVersion, 2);

console.log("learning progress schema, review scheduling and version recheck: ok");
