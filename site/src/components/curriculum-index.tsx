"use client";

import Link from "next/link";
import { useMemo, useState, useSyncExternalStore } from "react";
import { useLastVisitedSlug } from "@/components/resume-progress";
import {
  LEARNING_PROGRESS_EVENT,
  LEARNING_PROGRESS_KEY,
  validateLearningProgress,
  type LessonProgressConfig,
} from "@/lib/learning-progress";

type CurriculumEntry = {
  slug: string;
  title: string;
  summary: string;
  editorialState: "pilot" | "guide" | "reference";
  contentReadiness: "ready" | "partial" | "summary" | "reference";
  estimatedMinutes: number;
  outcomes: string[];
  prerequisites: Array<{ slug: string; title: string }>;
  progressConfig: LessonProgressConfig;
  position: number | null;
};

type CurriculumGroup = {
  id: string;
  title: string;
  description: string;
  lessons: CurriculumEntry[];
};

const stateLabels = {
  pilot: "Interactive pilot",
  guide: "Guide",
  reference: "Reference",
} as const;

const readinessLabels = {
  ready: "Ready",
  partial: "Partially taught",
  summary: "Summary",
  reference: "Reference",
} as const;

function subscribeToLearningProgress(callback: () => void) {
  window.addEventListener("storage", callback);
  window.addEventListener(LEARNING_PROGRESS_EVENT, callback);
  return () => {
    window.removeEventListener("storage", callback);
    window.removeEventListener(LEARNING_PROGRESS_EVENT, callback);
  };
}

function getLearningProgressSnapshot() {
  try {
    return window.localStorage.getItem(LEARNING_PROGRESS_KEY) ?? "";
  } catch {
    return "";
  }
}

export function CurriculumIndex({ groups }: { groups: CurriculumGroup[] }) {
  const [query, setQuery] = useState("");
  const savedProgress = useSyncExternalStore(subscribeToLearningProgress, getLearningProgressSnapshot, () => "");
  const knownSlugs = useMemo(() => groups.flatMap((group) => group.lessons.map((lesson) => lesson.slug)), [groups]);
  const progressConfigs = useMemo(() => Object.fromEntries(groups.flatMap((group) => group.lessons.map((lesson) => [lesson.slug, lesson.progressConfig]))), [groups]);
  const personalProgress = useMemo(() => {
    try {
      return validateLearningProgress(JSON.parse(savedProgress || "null") as unknown, progressConfigs);
    } catch {
      return validateLearningProgress(null, progressConfigs);
    }
  }, [progressConfigs, savedProgress]);
  const lastVisitedSlug = useLastVisitedSlug(knownSlugs);
  const normalizedQuery = query.trim().toLocaleLowerCase("en");
  const filteredGroups = useMemo(() => groups.map((group) => ({
    ...group,
    lessons: group.lessons.filter((lesson) => {
      if (!normalizedQuery) return true;
      const searchable = [
        lesson.title,
        lesson.summary,
        ...lesson.outcomes,
        group.title,
        ...lesson.prerequisites.map((prerequisite) => prerequisite.title),
      ].join(" ").toLocaleLowerCase("en");
      return searchable.includes(normalizedQuery);
    }),
  })).filter((group) => group.lessons.length > 0), [groups, normalizedQuery]);
  const resultCount = filteredGroups.reduce((count, group) => count + group.lessons.length, 0);

  return (
    <div className="curriculum-browser">
      <div className="curriculum-search">
        <label htmlFor="curriculum-search-input">Search lessons</label>
        <div className="curriculum-search-control">
          <input
            id="curriculum-search-input"
            type="search"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Try “graphs” or “linked list”"
            autoComplete="off"
          />
          {query && <button className="curriculum-clear" type="button" onClick={() => setQuery("")}>Clear</button>}
        </div>
        <p className="curriculum-result-count" role="status" aria-live="polite">
          {normalizedQuery ? `${resultCount} ${resultCount === 1 ? "lesson" : "lessons"} found` : "Search titles, descriptions, stages, and recommended prerequisites."}
        </p>
      </div>

      {filteredGroups.length > 0 ? (
        <div className="curriculum-stages">
          {filteredGroups.map((group) => (
            <section className="curriculum-stage" key={group.id} aria-labelledby={`stage-${group.id}`}>
              <div className="curriculum-stage-heading">
                <h3 id={`stage-${group.id}`}>{group.title}</h3>
                <p>{group.description}</p>
              </div>
              <ol className="lesson-index">
                {group.lessons.map((lesson) => (
                  <li key={lesson.slug} className={`lesson-index-row${lesson.editorialState === "pilot" ? " lesson-index-featured" : ""}`}>
                    <span className="lesson-index-position" aria-hidden="true">{lesson.position === null ? "REF" : String(lesson.position).padStart(2, "0")}</span>
                    <div className="lesson-index-main">
                      <div className="lesson-index-title-line">
                        <Link href={`/lessons/${lesson.slug}`}>{lesson.title}</Link>
                        <span className={`editorial-badge editorial-${lesson.editorialState}`}>{stateLabels[lesson.editorialState]}</span>
                      </div>
                      <p>{lesson.summary}</p>
                      <div className="lesson-index-metadata">
                        <span>About {lesson.estimatedMinutes} min</span>
                        <span className={`readiness-label readiness-${lesson.contentReadiness}`}>{readinessLabels[lesson.contentReadiness]}</span>
                        {lastVisitedSlug === lesson.slug && <span className="personal-state-label">Last visited</span>}
                        {personalProgress.lessons[lesson.slug]?.visitedAt && lastVisitedSlug !== lesson.slug && <span className="personal-state-label">Visited</span>}
                        {personalProgress.lessons[lesson.slug] && Object.values(personalProgress.lessons[lesson.slug].objectives).some((attempt) => attempt.attempts > 0) && (
                          <span className="personal-state-label">Attempted {Object.values(personalProgress.lessons[lesson.slug].objectives).reduce((sum, attempt) => sum + attempt.attempts, 0)} practice responses</span>
                        )}
                        {personalProgress.lessons[lesson.slug] && Object.values(personalProgress.lessons[lesson.slug].objectives).some((attempt) =>
                          attempt.reviewPassedAt !== null && attempt.contentVersion === lesson.progressConfig.contentVersion && attempt.lastResult === "correct",
                        ) && (
                          <span className="personal-state-label">Review passed</span>
                        )}
                      </div>
                      <details className="lesson-outcomes">
                        <summary>Learning outcomes <span>{lesson.outcomes.length}</span></summary>
                        <ul>{lesson.outcomes.map((outcome) => <li key={outcome}>{outcome}</li>)}</ul>
                      </details>
                      {lesson.prerequisites.length > 0 && (
                        <p className="prerequisite-line">Recommended first: {lesson.prerequisites.map((prerequisite, index) => (
                          <span key={prerequisite.slug}>{index > 0 ? ", " : ""}<Link href={`/lessons/${prerequisite.slug}`}>{prerequisite.title}</Link></span>
                        ))}</p>
                      )}
                    </div>
                    <span className="lesson-index-arrow" aria-hidden="true">→</span>
                  </li>
                ))}
              </ol>
            </section>
          ))}
        </div>
      ) : (
        <p className="curriculum-empty">No lessons match “{query.trim()}”. Try another term or clear the search.</p>
      )}
    </div>
  );
}
