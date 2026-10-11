"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { useLocalJsonState } from "@/lib/use-local-json-state";
import { useLastVisitedSlug } from "@/components/resume-progress";
import {
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
  matchedHeading?: string;
};

type SearchEntry = {
  slug: string;
  title: string;
  headings: string[];
  code: string[];
  body: string;
  reference: boolean;
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
  ready: "Full lesson",
  partial: "Full lesson",
  summary: "Overview",
  reference: "Reference",
} as const;

export function CurriculumIndex({ groups }: { groups: CurriculumGroup[] }) {
  const [query, setQuery] = useState("");
  const [openedStages, setOpenedStages] = useState<Record<string, boolean>>({});
  const [searchIndex, setSearchIndex] = useState<SearchEntry[] | null>(null);
  const [savedProgress] = useLocalJsonState(LEARNING_PROGRESS_KEY, null, (value: unknown) => value);
  const knownSlugs = useMemo(() => groups.flatMap((group) => group.lessons.map((lesson) => lesson.slug)), [groups]);
  const progressConfigs = useMemo(() => Object.fromEntries(groups.flatMap((group) => group.lessons.map((lesson) => [lesson.slug, lesson.progressConfig]))), [groups]);
  const personalProgress = useMemo(() => {
    try {
      return validateLearningProgress(savedProgress, progressConfigs);
    } catch {
      return validateLearningProgress(null, progressConfigs);
    }
  }, [progressConfigs, savedProgress]);
  const lastVisitedSlug = useLastVisitedSlug(knownSlugs);
  const normalizedQuery = query.trim().toLocaleLowerCase("en");
  useEffect(() => {
    if (normalizedQuery.length < 2 || searchIndex) return;
    let cancelled = false;
    fetch("/search-index.json")
      .then((response) => response.json())
      .then((value: SearchEntry[]) => { if (!cancelled) setSearchIndex(value); })
      .catch(() => { if (!cancelled) setSearchIndex([]); });
    return () => { cancelled = true; };
  }, [normalizedQuery, searchIndex]);
  const indexed = useMemo(() => new Map((searchIndex ?? []).map((entry) => [entry.slug, entry])), [searchIndex]);
  const filteredGroups = useMemo(() => {
    if (normalizedQuery.length >= 2 && searchIndex) {
      const ranked = groups.flatMap((group) => group.lessons.flatMap((lesson) => {
        const entry = indexed.get(lesson.slug);
        const titleHit = entry ? entry.title.includes(normalizedQuery) : lesson.title.toLocaleLowerCase("en").includes(normalizedQuery);
        const heading = entry?.headings.find((item) => item.includes(normalizedQuery));
        const bodyHit = entry ? entry.body.includes(normalizedQuery) || entry.code.some((item) => item.includes(normalizedQuery)) : false;
        const score = titleHit ? 3 : heading ? 2 : bodyHit ? 1 : 0;
        return score === 0 ? [] : [{ lesson, score: score - (entry?.reference ? 0.5 : 0), heading }];
      })).sort((left, right) => right.score - left.score || left.lesson.title.localeCompare(right.lesson.title));
      return ranked.length === 0 ? [] : [{
        id: "search",
        title: "Matches",
        description: "",
        lessons: ranked.map((item) => ({ ...item.lesson, matchedHeading: item.heading })),
      }];
    }
    return groups.map((group) => ({
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
  })).filter((group) => group.lessons.length > 0);
  }, [groups, indexed, normalizedQuery, searchIndex]);
  const resultCount = filteredGroups.reduce((count, group) => count + group.lessons.length, 0);
  const sequence = groups.flatMap((group) => group.lessons.filter((lesson) => lesson.editorialState !== "reference"));
  const completed = sequence
    .filter((lesson) => personalProgress.lessons[lesson.slug]?.completedAt)
    .sort((left, right) => (personalProgress.lessons[right.slug]?.completedAt ?? "").localeCompare(personalProgress.lessons[left.slug]?.completedAt ?? ""));
  const latest = completed[0];
  const latestIndex = latest ? sequence.findIndex((lesson) => lesson.slug === latest.slug) : -1;
  const continueLesson = latest
    ? sequence.slice(latestIndex + 1).find((lesson) => !personalProgress.lessons[lesson.slug]?.completedAt)
      ?? sequence.find((lesson) => !personalProgress.lessons[lesson.slug]?.completedAt)
    : undefined;
  const searching = normalizedQuery.length > 0;

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
        <p className="curriculum-result-count" role="status" aria-live={searching ? "polite" : "off"}>
          {searching ? `${resultCount} ${resultCount === 1 ? "lesson" : "lessons"} found` : "Search titles, descriptions, stages, and recommended prerequisites."}
        </p>
      </div>
      {continueLesson && (
        <p className="continue-card">
          <Link className="button button-primary" href={`/lessons/${continueLesson.slug}`}>Continue with {continueLesson.title}</Link>
        </p>
      )}

      {filteredGroups.length > 0 ? (
        <div className={`curriculum-stages${searching ? " is-searching" : ""}`}>
          {filteredGroups.map((group) => {
            const countable = group.lessons.filter((lesson) => lesson.editorialState !== "reference");
            const doneCount = countable.filter((lesson) => personalProgress.lessons[lesson.slug]?.completedAt).length;
            const defaultOpen = group.id === groups[0]?.id || group.lessons.some((lesson) => lesson.slug === lastVisitedSlug);
            const expanded = openedStages[group.id] ?? defaultOpen;
            const hiddenCount = Math.max(0, group.lessons.length - 4);
            return (
            <section className={`curriculum-stage${group.lessons.some((lesson) => lesson.slug === lastVisitedSlug) ? " is-current" : ""}${expanded ? " is-expanded" : ""}`} key={group.id} aria-labelledby={`stage-${group.id}`}>
              <div className="curriculum-stage-heading">
                <h3 id={`stage-${group.id}`}>{group.title}{countable.length > 0 ? ` · ${doneCount} of ${countable.length} done` : ""}</h3>
                <p>{group.description}</p>
              </div>
              <ol className="lesson-index">
                {group.lessons.map((lesson) => (
                  <li key={lesson.slug} className={`lesson-index-row${lesson.editorialState === "pilot" ? " lesson-index-featured" : ""}${lastVisitedSlug === lesson.slug ? " is-current" : ""}`}>
                    <span className="lesson-index-position" aria-hidden="true">{lesson.position === null ? "REF" : String(lesson.position).padStart(2, "0")}</span>
                    <div className="lesson-index-main">
                      <div className="lesson-index-title-line">
                        <Link href={`/lessons/${lesson.slug}`}>{lesson.title}</Link>
                        {lesson.matchedHeading && <span className="search-hit">{lesson.matchedHeading}</span>}
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
              {hiddenCount > 0 && (
                <button className="stage-more" type="button" onClick={() => setOpenedStages((current) => ({ ...current, [group.id]: !expanded }))}>
                  {expanded ? "Show fewer" : `Show ${hiddenCount} more`}
                </button>
              )}
            </section>
            );
          })}
        </div>
      ) : (
        <p className="curriculum-empty">No lessons match “{query.trim()}”. Try another term or clear the search.</p>
      )}
    </div>
  );
}
