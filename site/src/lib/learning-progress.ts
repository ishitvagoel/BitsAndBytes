export const LEARNING_PROGRESS_KEY = "bitsandbytes.learning-progress.v1";
export const LEARNING_PROGRESS_EVENT = `bitsandbytes:local-state:${LEARNING_PROGRESS_KEY}`;

export type ObjectiveAttempt = {
  attempts: number;
  contentVersion: number;
  lastAttemptAt: string;
  nextReviewAt: string;
  lastResult: "correct" | "retry";
  reviewPassedAt: string | null;
};

export type LessonProgressRecord = {
  contentVersion: number;
  lastSectionId: string | null;
  visitedAt: string;
  needsRecheck: boolean;
  objectives: Record<string, ObjectiveAttempt>;
};

export type LearningProgress = {
  schemaVersion: 1;
  lessons: Record<string, LessonProgressRecord>;
};

export type LessonProgressConfig = {
  contentVersion: number;
  sectionIds: string[];
  objectiveIds: string[];
};

export function emptyLearningProgress(): LearningProgress {
  return { schemaVersion: 1, lessons: {} };
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isTimestamp(value: unknown): value is string {
  return typeof value === "string" && Number.isFinite(Date.parse(value));
}

export function validateLearningProgress(value: unknown, config: Record<string, LessonProgressConfig>): LearningProgress {
  if (!isRecord(value) || value.schemaVersion !== 1 || !isRecord(value.lessons)) return emptyLearningProgress();
  const lessons: LearningProgress["lessons"] = {};
  for (const [slug, raw] of Object.entries(value.lessons)) {
    const current = config[slug];
    if (!current || !isRecord(raw)) continue;
    const contentVersion = raw.contentVersion;
    if (!Number.isInteger(contentVersion) || (contentVersion as number) < 1 || (contentVersion as number) > current.contentVersion) continue;
    const sectionId = raw.lastSectionId;
    const lastSectionId = typeof sectionId === "string" && current.sectionIds.includes(sectionId) ? sectionId : null;
    const visitedAt = isTimestamp(raw.visitedAt) ? raw.visitedAt : "";
    const objectives: LessonProgressRecord["objectives"] = {};
    if (isRecord(raw.objectives)) {
      for (const [objectiveId, attempt] of Object.entries(raw.objectives)) {
        if (!isRecord(attempt)) continue;
        const attemptContentVersion = attempt.contentVersion === undefined
          ? (contentVersion as number)
          : attempt.contentVersion;
        if (
          !Number.isInteger(attempt.attempts) || (attempt.attempts as number) < 1 ||
          !Number.isInteger(attemptContentVersion) || (attemptContentVersion as number) < 1 ||
          !isTimestamp(attempt.lastAttemptAt) || !isTimestamp(attempt.nextReviewAt) ||
          (attempt.lastResult !== "correct" && attempt.lastResult !== "retry") ||
          (attempt.reviewPassedAt !== null && !isTimestamp(attempt.reviewPassedAt))
        ) continue;
        objectives[objectiveId] = {
          attempts: attempt.attempts as number,
          contentVersion: attemptContentVersion as number,
          lastAttemptAt: attempt.lastAttemptAt,
          nextReviewAt: attempt.nextReviewAt,
          lastResult: attempt.lastResult,
          reviewPassedAt: attempt.reviewPassedAt as string | null,
        };
      }
    }
    const savedVersion = contentVersion as number;
    const allCurrentObjectivesChecked = current.objectiveIds.every(
      (objectiveId) => objectives[objectiveId]?.contentVersion === current.contentVersion,
    );
    lessons[slug] = {
      contentVersion: allCurrentObjectivesChecked ? current.contentVersion : savedVersion,
      lastSectionId,
      visitedAt,
      needsRecheck: !allCurrentObjectivesChecked && (savedVersion < current.contentVersion || raw.needsRecheck === true),
      objectives,
    };
  }
  return { schemaVersion: 1, lessons };
}

/** Reject an import instead of silently turning an unsupported record into empty progress. */
export function validateLearningProgressImport(
  value: unknown,
  config: Record<string, LessonProgressConfig>,
): LearningProgress | null {
  if (!isRecord(value) || value.schemaVersion !== 1 || !isRecord(value.lessons)) return null;
  for (const [slug, raw] of Object.entries(value.lessons)) {
    const current = config[slug];
    if (!current || !isRecord(raw)) return null;
    if (
      !Number.isInteger(raw.contentVersion) || (raw.contentVersion as number) < 1 ||
      (raw.contentVersion as number) > current.contentVersion ||
      typeof raw.visitedAt !== "string" || (raw.visitedAt !== "" && !isTimestamp(raw.visitedAt)) ||
      (raw.lastSectionId !== null && typeof raw.lastSectionId !== "string") ||
      (typeof raw.lastSectionId === "string" && !current.sectionIds.includes(raw.lastSectionId)) ||
      typeof raw.needsRecheck !== "boolean" || !isRecord(raw.objectives)
    ) return null;
    for (const [objectiveId, attempt] of Object.entries(raw.objectives)) {
      if (!current.objectiveIds.includes(objectiveId) || !isRecord(attempt)) return null;
      const version = attempt.contentVersion ?? raw.contentVersion;
      if (
        !Number.isInteger(attempt.attempts) || (attempt.attempts as number) < 1 ||
        !Number.isInteger(version) || (version as number) < 1 || (version as number) > current.contentVersion ||
        !isTimestamp(attempt.lastAttemptAt) || !isTimestamp(attempt.nextReviewAt) ||
        (attempt.lastResult !== "correct" && attempt.lastResult !== "retry") ||
        (attempt.reviewPassedAt !== null && !isTimestamp(attempt.reviewPassedAt))
      ) return null;
    }
  }
  return validateLearningProgress(value, config);
}

export function recordLessonVisit(
  progress: LearningProgress,
  slug: string,
  config: LessonProgressConfig,
  sectionId: string | null,
  now = new Date(),
): LearningProgress {
  const existing = progress.lessons[slug];
  const saved = existing ?? {
    contentVersion: config.contentVersion,
    lastSectionId: null,
    visitedAt: "",
    needsRecheck: false,
    objectives: {},
  };
  return {
    schemaVersion: 1,
    lessons: {
      ...progress.lessons,
      [slug]: {
        ...saved,
        lastSectionId: sectionId && config.sectionIds.includes(sectionId) ? sectionId : null,
        visitedAt: now.toISOString(),
        needsRecheck: saved.needsRecheck || saved.contentVersion < config.contentVersion,
      },
    },
  };
}

export function recordObjectiveAttempt(
  progress: LearningProgress,
  slug: string,
  config: LessonProgressConfig,
  objectiveId: string,
  correct: boolean,
  now = new Date(),
): LearningProgress {
  if (!config.objectiveIds.includes(objectiveId)) return progress;
  const existing = progress.lessons[slug] ?? {
    contentVersion: config.contentVersion,
    lastSectionId: null,
    visitedAt: now.toISOString(),
    needsRecheck: false,
    objectives: {},
  };
  const prior = existing.objectives[objectiveId];
  const hadDueReview = prior ? Date.parse(prior.nextReviewAt) <= now.getTime() : false;
  const nextReviewDays = correct ? (hadDueReview ? 7 : 3) : 1;
  const nextReviewAt = new Date(now.getTime() + nextReviewDays * 24 * 60 * 60 * 1000).toISOString();
  const objective: ObjectiveAttempt = {
    attempts: (prior?.attempts ?? 0) + 1,
    contentVersion: config.contentVersion,
    lastAttemptAt: now.toISOString(),
    nextReviewAt,
    lastResult: correct ? "correct" : "retry",
    reviewPassedAt: correct && hadDueReview ? now.toISOString() : prior?.reviewPassedAt ?? null,
  };
  const objectives = { ...existing.objectives, [objectiveId]: objective };
  const allCurrentObjectivesChecked = config.objectiveIds.every(
    (currentObjectiveId) => objectives[currentObjectiveId]?.contentVersion === config.contentVersion,
  );
  return {
    schemaVersion: 1,
    lessons: {
      ...progress.lessons,
      [slug]: {
        ...existing,
        contentVersion: allCurrentObjectivesChecked ? config.contentVersion : existing.contentVersion,
        needsRecheck: !allCurrentObjectivesChecked && (existing.needsRecheck || existing.contentVersion < config.contentVersion),
        visitedAt: existing.visitedAt || now.toISOString(),
        objectives,
      },
    },
  };
}
