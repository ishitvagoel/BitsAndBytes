import Link from "next/link";

import { CurriculumIndex } from "@/components/curriculum-index";
import { LocalProgressTools } from "@/components/local-progress-tools";
import { ReviewQueue } from "@/components/review-queue";
import { ResumeCard } from "@/components/resume-progress";
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
  const pilot = lessons.find((lesson) => lesson.slug === "binary-search");
  const resumeLessons = lessons.map((lesson) => ({
    slug: lesson.slug,
    title: lesson.title,
    sections: getLessonSections(lesson).map(({ id, title }) => ({ id, title })),
  }));
  const progressConfigs: Record<string, LessonProgressConfig> = Object.fromEntries(lessons.map((lesson) => [
    lesson.slug,
    progressConfigFor(lesson),
  ]));

  return (
    <main id="main-content" className="home-page" tabIndex={-1}>
      <section className="home-hero" aria-labelledby="home-title">
        <p className="eyebrow">BITS AND BYTES · ALGORITHMS, MADE UNDERSTANDABLE</p>
        <h1 id="home-title">Learn the idea.<br /><span>Then follow the steps.</span></h1>
        <p className="home-lede">
          A practical guide to data structures and algorithms. Start with the pilot lesson, work through an example, and build your own explanation of why it works.
        </p>
        <Link className="readiness-link" href="/readiness">Check whether the Python examples will feel familiar <span aria-hidden="true">→</span></Link>
        <Link className="readiness-link reference-home-link" href="/reference">Search the glossary and compare Python tools <span aria-hidden="true">→</span></Link>
      </section>

      <ResumeCard lessons={resumeLessons} />
      <LocalProgressTools lessons={resumeLessons} progressConfigs={progressConfigs} />
      <ReviewQueue lessons={lessons.map((lesson) => ({
        slug: lesson.slug,
        title: lesson.title,
        outcomes: lesson.outcomes,
        config: progressConfigs[lesson.slug],
        practiceAvailable: lesson.exerciseIds.length > 0,
      }))} />

      {pilot && (
        <section className="start-card" aria-labelledby="start-title">
          <div className="start-card-copy">
            <p className="eyebrow">START HERE <span className="pilot-badge">LEARNING PILOT</span></p>
            <h2 id="start-title">Search a sorted list, one half at a time</h2>
            <p>See why each comparison rules out indexes, trace present and missing values, and practice the off-by-one cases.</p>
            <ul className="outcome-list">
              <li>Step through a real binary search</li>
              <li>Understand duplicates and boundaries</li>
              <li>Compare search and insertion costs</li>
            </ul>
            <Link className="button button-primary start-button" href={`/lessons/${pilot.slug}`}>
              Start the lesson <span aria-hidden="true">→</span>
            </Link>
            <span className="time-note">About 15 minutes · Basic Python helpful</span>
          </div>
          <div className="start-visual" aria-hidden="true">
            <span className="visual-caption">FIND 7</span>
            <div className="visual-values">
              {[1, 3, 5, 7, 9].map((value) => (
                <span key={value} className={value === 5 ? "value-checked" : value === 7 ? "value-found" : ""}>{value}</span>
              ))}
            </div>
            <span className="visual-note">middle → compare → narrow</span>
          </div>
        </section>
      )}

      <section className="browse-section" aria-labelledby="browse-title">
        <div className="browse-heading">
          <div>
            <p className="eyebrow">THE GUIDE</p>
            <h2 id="browse-title">Explore all lessons</h2>
          </div>
          <span className="lesson-count">{lessons.length} lessons</span>
        </div>
        <p className="curriculum-note">Recommended order helps build ideas step by step. Every lesson stays open, so you can jump to any topic.</p>
        <CurriculumIndex groups={groups} />
      </section>
      <footer className="home-footer">
        <span>Bits and Bytes</span>
        <span>Learn one idea at a time.</span>
      </footer>
    </main>
  );
}
