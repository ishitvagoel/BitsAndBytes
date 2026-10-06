"use client";

import Link from "next/link";
import { useEffect, useMemo, useRef, useSyncExternalStore } from "react";
import {
  LEARNING_PROGRESS_EVENT,
  LEARNING_PROGRESS_KEY,
  recordLessonVisit,
  validateLearningProgress,
  type LessonProgressConfig,
} from "@/lib/learning-progress";

const STORAGE_KEY = "bitsandbytes.resume.v1";
const RESUME_EVENT = "bitsandbytes:resume";

type ResumeRecord = {
  version: 1;
  slug: string;
  sectionId: string | null;
};

type ResumeLesson = {
  slug: string;
  title: string;
  sections: Array<{ id: string; title: string }>;
};

function readRecord(raw: string, lessons: ResumeLesson[]): { record: ResumeRecord; lesson: ResumeLesson; section?: { id: string; title: string } } | null {
  try {
    if (!raw) return null;
    const value: unknown = JSON.parse(raw);
    if (!value || typeof value !== "object") return null;
    const candidate = value as Partial<ResumeRecord>;
    if (candidate.version !== 1 || typeof candidate.slug !== "string") return null;
    const lesson = lessons.find((item) => item.slug === candidate.slug);
    if (!lesson) return null;
    const section = typeof candidate.sectionId === "string"
      ? lesson.sections.find((item) => item.id === candidate.sectionId)
      : undefined;
    const record: ResumeRecord = { version: 1, slug: lesson.slug, sectionId: section?.id ?? null };
    return { record, lesson, ...(section ? { section } : {}) };
  } catch {
    return null;
  }
}

function subscribeToResume(callback: () => void) {
  window.addEventListener("storage", callback);
  window.addEventListener(RESUME_EVENT, callback);
  return () => {
    window.removeEventListener("storage", callback);
    window.removeEventListener(RESUME_EVENT, callback);
  };
}

function getResumeSnapshot() {
  try {
    return window.localStorage.getItem(STORAGE_KEY) ?? "";
  } catch {
    return "";
  }
}

function getResumeServerSnapshot() {
  return "";
}

function saveRecord(slug: string, sectionId: string | null) {
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify({ version: 1, slug, sectionId } satisfies ResumeRecord));
    window.dispatchEvent(new Event(RESUME_EVENT));
  } catch {
    // The guide stays usable when browser storage is unavailable or full.
  }
}

export function ResumeTracker({
  slug,
  sections,
  progressConfigs,
}: {
  slug: string;
  sections: Array<{ id: string; title: string }>;
  progressConfigs: Record<string, LessonProgressConfig>;
}) {
  const activeSectionId = useRef<string | null>(null);
  useEffect(() => {
    const saveSection = (sectionId: string | null) => {
      activeSectionId.current = sectionId;
      saveRecord(slug, sectionId);
      try {
        const current = validateLearningProgress(
          JSON.parse(window.localStorage.getItem(LEARNING_PROGRESS_KEY) ?? "null") as unknown,
          progressConfigs,
        );
        const updated = recordLessonVisit(current, slug, progressConfigs[slug], sectionId);
        window.localStorage.setItem(LEARNING_PROGRESS_KEY, JSON.stringify(updated));
        window.dispatchEvent(new Event(LEARNING_PROGRESS_EVENT));
      } catch {
        // The page and its resume link stay usable when local storage is unavailable.
      }
    };

    const sectionForHash = () => {
      let hash = window.location.hash.slice(1);
      try { hash = decodeURIComponent(hash); } catch { hash = ""; }
      return sections.find((item) => item.id === hash)?.id ?? null;
    };
    const initialSection = sectionForHash() ?? sections[0]?.id ?? null;
    saveSection(initialSection);

    const observer = new IntersectionObserver((entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((first, second) => first.boundingClientRect.top - second.boundingClientRect.top)[0];
      const sectionId = visible?.target.id;
      if (sectionId && sections.some((item) => item.id === sectionId) && sectionId !== activeSectionId.current) {
        saveSection(sectionId);
      }
    }, { rootMargin: "-15% 0px -70% 0px", threshold: 0 });

    for (const section of sections) {
      const element = document.getElementById(section.id);
      if (element) observer.observe(element);
    }
    const onHashChange = () => {
      const sectionId = sectionForHash();
      if (sectionId) saveSection(sectionId);
    };
    window.addEventListener("hashchange", onHashChange);
    return () => {
      observer.disconnect();
      window.removeEventListener("hashchange", onHashChange);
    };
  }, [progressConfigs, slug, sections]);

  return null;
}

export function ResumeCard({ lessons }: { lessons: ResumeLesson[] }) {
  const raw = useSyncExternalStore(subscribeToResume, getResumeSnapshot, getResumeServerSnapshot);
  const resume = useMemo(() => readRecord(raw, lessons), [raw, lessons]);
  if (!resume) return null;
  const href = `/lessons/${resume.lesson.slug}${resume.section ? `#${encodeURIComponent(resume.section.id)}` : ""}`;

  return (
    <section className="resume-card" aria-labelledby="resume-title">
      <div>
        <p className="eyebrow">SAVED ON THIS DEVICE</p>
        <h2 id="resume-title">Pick up where you left off</h2>
        <p>{resume.lesson.title}{resume.section ? <span> · {resume.section.title}</span> : null}</p>
      </div>
      <Link className="button button-secondary resume-button" href={href}>
        Resume lesson <span aria-hidden="true">→</span>
      </Link>
    </section>
  );
}

export function useLastVisitedSlug(knownSlugs: string[]) {
  const raw = useSyncExternalStore(subscribeToResume, getResumeSnapshot, getResumeServerSnapshot);
  return useMemo(() => {
    try {
      const value: unknown = JSON.parse(raw);
      if (!value || typeof value !== "object") return null;
      const candidate = value as Partial<ResumeRecord>;
      return candidate.version === 1 && typeof candidate.slug === "string" && knownSlugs.includes(candidate.slug)
        ? candidate.slug
        : null;
    } catch {
      return null;
    }
  }, [knownSlugs, raw]);
}
