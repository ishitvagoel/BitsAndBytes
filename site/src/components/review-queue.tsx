"use client";

import Link from "next/link";
import { useMemo } from "react";
import { useLocalJsonState } from "@/lib/use-local-json-state";
import {
  LEARNING_PROGRESS_KEY,
  validateLearningProgress,
  type LessonProgressConfig,
} from "@/lib/learning-progress";

type LessonReviewInfo = {
  slug: string;
  title: string;
  outcomes: string[];
  prompts: Record<string, string>;
  config: LessonProgressConfig;
  practiceAvailable: boolean;
};

export function ReviewQueue({ lessons }: { lessons: LessonReviewInfo[] }) {
  const [raw] = useLocalJsonState(LEARNING_PROGRESS_KEY, null, (value: unknown) => value);
  const configs = useMemo(() => Object.fromEntries(lessons.map((lesson) => [lesson.slug, lesson.config])), [lessons]);
  const progress = useMemo(() => {
    try {
      return validateLearningProgress(raw, configs);
    } catch {
      return validateLearningProgress(null, configs);
    }
  }, [configs, raw]);
  const due = useMemo(() => lessons.flatMap((lesson) => {
    if (!lesson.practiceAvailable) return [];
    const record = progress.lessons[lesson.slug];
    if (!record) return [];
    const objectiveIds = record.needsRecheck
      ? lesson.config.objectiveIds.filter((objectiveId) =>
          record.objectives[objectiveId]?.contentVersion !== lesson.config.contentVersion,
        )
      : Object.entries(record.objectives)
        .filter(([, attempt]) => Date.parse(attempt.nextReviewAt) <= Date.now())
        .map(([objectiveId]) => objectiveId);
    return [...new Set(objectiveIds)].map((objectiveId) => {
      const objectiveIndex = lesson.config.objectiveIds.indexOf(objectiveId);
      if (objectiveIndex < 0) return null;
      return {
        key: `${lesson.slug}-${objectiveId}`,
        slug: lesson.slug,
        title: lesson.title,
        outcome: lesson.outcomes[objectiveIndex],
        prompt: lesson.prompts[objectiveId] || lesson.outcomes[objectiveIndex],
        recheck: record.needsRecheck && record.objectives[objectiveId]?.contentVersion !== lesson.config.contentVersion,
        attempted: Boolean(record.objectives[objectiveId]),
      };
    }).filter((item): item is NonNullable<typeof item> => item !== null);
  }), [lessons, progress]);

  const hasAttempt = lessons.some((lesson) => {
    const record = progress.lessons[lesson.slug];
    return record && Object.values(record.objectives).some((attempt) => attempt.attempts > 0);
  });
  if (!due.length && !hasAttempt) return null;

  return (
    <section className="review-queue" aria-labelledby="review-queue-title">
      <p className="eyebrow">SPACED REVIEW · SAVED ON THIS DEVICE</p>
      <h2 id="review-queue-title">Review due</h2>
      {due.length ? (
        <ul>
          {due.map((item) => (
            <li key={item.key}>
              <div><strong>{item.title}</strong><span>{item.prompt}</span></div>
              <Link className="button button-secondary" href={`/lessons/${item.slug}?reviewObjective=${encodeURIComponent(item.key.slice(item.slug.length + 1))}#practice-section`}>
                {item.recheck ? "Recheck updated lesson" : item.attempted ? "Review objective" : "Revisit objective"}
              </Link>
            </li>
          ))}
        </ul>
      ) : <p>No objectives are due. Answer a practice question to schedule an optional revisit.</p>}
      <p className="review-queue-note">Review dates are reminders for another try, not a mastery score. They stay in this browser.</p>
    </section>
  );
}
