import Link from "next/link";

import { CurriculumIndex } from "@/components/curriculum-index";
import { LocalProgressTools } from "@/components/local-progress-tools";
import { ReviewQueue } from "@/components/review-queue";
import { ResumeLine } from "@/components/resume-progress";
import { getAllLessons, getCurriculumStages } from "@/lib/lessons";
import { getLessonSections } from "@/lib/lesson-sections";
import type { LessonProgressConfig } from "@/lib/learning-progress";

export default function Home() {
  const lessons = getAllLessons();
  const sequence = lessons.filter((lesson) => lesson.editorialState !== "reference");
  const progressConfigFor = (lesson: (typeof lessons)[number]): LessonProgressConfig => ({
    contentVersion: lesson.contentVersion,
    sectionIds: getLessonSections(lesson).map((section) => section.id),
    objectiveIds: lesson.objectiveIds,
  });
  const groups = getCurriculumStages().map((stage) => ({
    id: stage.id,
    title: stage.title,
    description: stage.description,
    lessons: stage.lessons.map((lesson) => ({
      slug: lesson.slug,
      title: lesson.title,
      summary: lesson.summary,
      editorialState: lesson.editorialState,
      contentReadiness: lesson.contentReadiness,
      estimatedMinutes: lesson.estimatedMinutes,
      outcomes: lesson.outcomes,
      progressConfig: progressConfigFor(lesson),
      prerequisites: lesson.prerequisites,
      position: lesson.editorialState === "reference"
        ? null
        : sequence.findIndex((item) => item.slug === lesson.slug) + 1,
    })),
  }));
  const resumeLessons = lessons.map((lesson) => ({
    slug: lesson.slug,
    title: lesson.title,
    sections: getLessonSections(lesson).map(({ id, title }) => ({ id, title })),
  }));
  const progressConfigs: Record<string, LessonProgressConfig> = Object.fromEntries(lessons.map((lesson) => [
    lesson.slug,
    progressConfigFor(lesson),
  ]));

  const start = sequence[0];
  return (
    <main id="main-content" className="home-page" tabIndex={-1}>
      <h1 id="home-title">Learn the idea. Then follow the steps.</h1>
      <p className="home-lead">Start with how to count the work an algorithm does. Each later lesson uses that count.</p>
      <ResumeLine lessons={resumeLessons} />
      <p className="home-actions">
        <Link className="button button-primary" href={`/lessons/${start.slug}`}>
          Start here <span aria-hidden="true">→</span>
        </Link>
        <Link className="readiness-link" href="/readiness">Check whether the Python examples will feel familiar <span aria-hidden="true">→</span></Link>
        <Link className="readiness-link" href="/reference">Search the glossary and compare Python tools <span aria-hidden="true">→</span></Link>
      </p>
      <section className="browse-section chapter-grid" aria-labelledby="browse-title">
        <h2 id="browse-title" className="sr-only">Course</h2>
        <CurriculumIndex groups={groups} />
      </section>
      <LocalProgressTools lessons={resumeLessons} progressConfigs={progressConfigs} />
      <ReviewQueue lessons={lessons.map((lesson) => ({
        slug: lesson.slug,
        title: lesson.title,
        outcomes: lesson.outcomes,
        config: progressConfigs[lesson.slug],
        practiceAvailable: lesson.exerciseIds.length > 0,
      }))} />
      <footer className="home-footer">
        <span>Bits and Bytes</span>
        <span>Learn one idea at a time.</span>
      </footer>
    </main>
  );
}
