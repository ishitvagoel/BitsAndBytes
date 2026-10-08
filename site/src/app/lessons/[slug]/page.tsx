import Link from "next/link";
import dynamic from "next/dynamic";
import { notFound, redirect } from "next/navigation";
import ReactMarkdown from "react-markdown";
import { isValidElement, type ReactNode } from "react";

import { CopyableCodeBlock } from "@/components/copyable-code-block";
import { LessonCourseNav, MobileLessonMenu } from "@/components/lesson-course-nav";
import { ResumeLine, ResumeTracker } from "@/components/resume-progress";
import binarySearchSource from "@/data/binary-search-source.json";
import lessonSlugAliases from "@/data/lesson-slug-aliases.json";
import {
  getAllLessons,
  getLessonBySlug,
} from "@/lib/lessons";
import { getLessonSections } from "@/lib/lesson-sections";
import { getSections, headingId } from "@/lib/markdown-sections";
import { resolveLessonMarkdownHref } from "@/lib/markdown-links";
import type { LessonProgressConfig } from "@/lib/learning-progress";

const BinarySearchLab = dynamic(
  () => import("@/components/binary-search-lab").then((module) => module.BinarySearchLab),
  { loading: () => <p className="interaction-loading" role="status">The interactive trace is loading. The written explanation and source code below remain available.</p> },
);
const LessonPractice = dynamic(
  () => import("@/components/binary-search-lab").then((module) => module.LessonPractice),
  { loading: () => <p className="interaction-loading" role="status">Practice feedback is loading. The lesson explanation remains available above.</p> },
);

type LessonPageProps = {
  params: Promise<{ slug: string }>;
};

function headingText(value: ReactNode): string {
  if (typeof value === "string" || typeof value === "number") return String(value);
  if (Array.isArray(value)) return value.map(headingText).join("");
  if (isValidElement<{ children?: ReactNode }>(value)) return headingText(value.props.children);
  return "";
}

function codeBlockContent(value: ReactNode): { code: string; language?: string } {
  if (typeof value === "string" || typeof value === "number") return { code: String(value) };
  if (Array.isArray(value)) {
    const parts = value.map(codeBlockContent);
    return { code: parts.map((part) => part.code).join(""), language: parts.find((part) => part.language)?.language };
  }
  if (isValidElement<{ children?: ReactNode; className?: string }>(value)) {
    const language = /(?:^|\s)language-([\w-]+)/.exec(value.props.className ?? "")?.[1];
    const child = codeBlockContent(value.props.children);
    return { code: child.code, language: language ?? child.language };
  }
  return { code: "" };
}

type SourceCodeExcerpt = {
  sourcePath: string;
  code: string;
  traceLines: Record<string, number[]>;
  commit?: string;
};

function Markdown({
  source,
  excerpts = {},
  lessonSlugs,
  repositoryRef,
}: {
  source: string;
  excerpts?: Record<string, SourceCodeExcerpt>;
  lessonSlugs: ReadonlySet<string>;
  repositoryRef: string;
}) {
  const sections = getSections(source);
  let nextSection = 0;
  const renderedHeadingId = (children: ReactNode) => {
    const section = sections[nextSection++];
    return section?.id ?? headingId(headingText(children));
  };
  return (
    <ReactMarkdown
      components={{
        a: ({ href, children, ...props }) => {
          if (!href) return <a {...props}>{children}</a>;
          const lessonHref = resolveLessonMarkdownHref(href, lessonSlugs);
          if (lessonHref) return <Link href={lessonHref}>{children}</Link>;

          const sourcePath = /^\.\.\/(bitsandbytes|tests)\/(.+)$/.exec(href);
          if (sourcePath) {
            const repositoryPath = `${sourcePath[1]}/${sourcePath[2]}`;
            return (
              <a href={`https://github.com/ishitvagoel/BitsAndBytes/blob/${repositoryRef}/${repositoryPath}`} target="_blank" rel="noreferrer" {...props}>
                {children}<span className="sr-only"> (opens repository source in a new tab)</span>
              </a>
            );
          }

          const repositoryMasterLink = href.replace(
            "https://github.com/ishitvagoel/BitsAndBytes/blob/master/",
            `https://github.com/ishitvagoel/BitsAndBytes/blob/${repositoryRef}/`,
          );
          return <a href={repositoryMasterLink} {...props}>{children}</a>;
        },
        pre: ({ children }) => {
          const block = codeBlockContent(children);
          return <CopyableCodeBlock code={block.code} language={block.language} />;
        },
        p: ({ children, ...props }) => {
          const marker = /^\[\[source-excerpt:([a-z0-9-]+)\]\]$/.exec(headingText(children).trim());
          const excerpt = marker ? excerpts[marker[1]] : undefined;
          if (marker && excerpt) {
            return <p><a href="#binary-search-source">Follow the current Python source and highlighted lines in the trace above.</a></p>;
          }
          if (marker) throw new Error(`Missing source excerpt for ${marker[1]}`);
          return <p {...props}>{children}</p>;
        },
        h2: ({ children, ...props }) => <h2 {...props} id={renderedHeadingId(children)}>{children}</h2>,
        h3: ({ children, ...props }) => <h3 {...props} id={renderedHeadingId(children)}>{children}</h3>,
      }}
    >
      {source}
    </ReactMarkdown>
  );
}

export function generateStaticParams() {
  return Object.keys(lessonSlugAliases).map((slug) => ({ slug }));
}

export async function generateMetadata({ params }: LessonPageProps) {
  const { slug } = await params;
  const canonicalSlug = lessonSlugAliases[slug as keyof typeof lessonSlugAliases] ?? slug;
  const lesson = getLessonBySlug(canonicalSlug);
  if (!lesson) {
    return { title: "Lesson not found" };
  }
  return { title: `${lesson.title} | Bits and Bytes` };
}

export default async function LessonPage({ params }: LessonPageProps) {
  const { slug } = await params;
  const canonicalSlug = lessonSlugAliases[slug as keyof typeof lessonSlugAliases] ?? slug;
  if (canonicalSlug !== slug) redirect(`/lessons/${canonicalSlug}`);
  const lessons = getAllLessons();
  const lesson = getLessonBySlug(canonicalSlug);
  if (!lesson) {
    notFound();
  }

  const repositoryRef = process.env.VERCEL_GIT_COMMIT_SHA ?? "master";
  const learningSequence = lessons.filter((item) => item.editorialState !== "reference");
  const position = learningSequence.findIndex((item) => item.slug === lesson.slug) + 1;
  const sections = getLessonSections(lesson);
  const resumeLessons = lessons.map((item) => ({
    slug: item.slug,
    title: item.title,
    sections: getLessonSections(item).map(({ id, title }) => ({ id, title })),
  }));
  const progressConfigs: Record<string, LessonProgressConfig> = Object.fromEntries(lessons.map((item) => [
    item.slug,
    {
      contentVersion: item.contentVersion,
      sectionIds: getLessonSections(item).map((section) => section.id),
      objectiveIds: item.objectiveIds,
    },
  ]));
  const courseLinks = learningSequence.map((item) => ({
    slug: item.slug,
    title: item.title,
    stageTitle: item.stageTitle,
    editorialState: item.editorialState,
  }));
  const sourceExcerpt = lesson.slug === "binary-search"
    ? {
        ...binarySearchSource,
        ...(process.env.VERCEL_GIT_COMMIT_SHA ? { commit: process.env.VERCEL_GIT_COMMIT_SHA } : {}),
      }
    : undefined;
  const excerpts: Record<string, SourceCodeExcerpt> = sourceExcerpt ? { "binary-search": sourceExcerpt } : {};
  const lessonSlugs = new Set(lessons.map((item) => item.slug));
  const binarySearchParts = lesson.slug === "binary-search"
    ? lesson.content.split("## The idea: keep only possible answers")
    : [];

  return (
    <main id="main-content" className="lesson-layout" tabIndex={-1}>
      <div className="lesson-main-column">
        <ResumeTracker slug={lesson.slug} sections={sections.map(({ id, title }) => ({ id, title }))} progressConfigs={progressConfigs} />
        <ResumeLine lessons={resumeLessons} />
        <Link className="back-link" href="/">← Course home</Link>
        <MobileLessonMenu lessons={courseLinks} currentSlug={lesson.slug} />
        <p className="lesson-kicker">{lesson.stageTitle.toUpperCase()} <span aria-hidden="true">/</span> {position > 0 ? `LESSON ${position} OF ${learningSequence.length}` : "REFERENCE"}</p>
        <h1 className="lesson-title">{lesson.title}</h1>
        <p className="lesson-subtitle">
          {lesson.summary}
        </p>
        <div className="lesson-readiness">
          <span className={`editorial-badge editorial-${lesson.editorialState}`}>{lesson.editorialState === "pilot" ? "Interactive pilot" : lesson.editorialState === "reference" ? "Reference" : "Guide"}</span>
          <span className={`readiness-label readiness-${lesson.contentReadiness}`}>{lesson.contentReadiness === "ready" ? "Ready" : lesson.contentReadiness === "partial" ? "Partially taught" : lesson.contentReadiness === "summary" ? "Summary only" : "Reference"}</span>
          <span>About {lesson.estimatedMinutes} min</span>
        </div>

        <details className="lesson-outcomes lesson-page-outcomes">
          <summary>What you will learn <span>{lesson.outcomes.length}</span></summary>
          <ul>{lesson.outcomes.map((outcome) => <li key={outcome}>{outcome}</li>)}</ul>
        </details>

        {lesson.prerequisites.length > 0 && (
          <section className="prerequisite-card" aria-labelledby="prerequisite-title">
            <h2 id="prerequisite-title">Recommended first</h2>
            <p>These topics introduce ideas used here. They are recommendations; you can continue directly.</p>
            <ul>
              {lesson.prerequisites.map((prerequisite) => (
                <li key={prerequisite.slug}><Link href={`/lessons/${prerequisite.slug}`}>{prerequisite.title}</Link></li>
              ))}
            </ul>
          </section>
        )}

        {sections.length > 0 && (
          <details className="contents-panel">
            <summary>On this page <span>{sections.length} sections</span></summary>
            <nav aria-label="On this page">
              <ol>
                {sections.map((section) => (
                  <li className={section.level === 3 ? "contents-subsection" : undefined} key={`${section.id}-${section.title}`}>
                    <a href={`#${section.id}`}>{section.title}</a>
                  </li>
                ))}
              </ol>
            </nav>
          </details>
        )}

        <article className="lesson-body">
          {lesson.slug === "binary-search" && binarySearchParts.length > 1 ? (
            <>
              <Markdown source={binarySearchParts[0]} excerpts={excerpts} lessonSlugs={lessonSlugs} repositoryRef={repositoryRef} />
              {sourceExcerpt && <BinarySearchLab sourceCode={sourceExcerpt.code} sourcePath={sourceExcerpt.sourcePath} sourceCommit={sourceExcerpt.commit} traceLines={sourceExcerpt.traceLines} />}
              <Markdown source={`## The idea: keep only possible answers${binarySearchParts.slice(1).join("## The idea: keep only possible answers")}`} excerpts={excerpts} lessonSlugs={lessonSlugs} repositoryRef={repositoryRef} />
              <LessonPractice lessonSlug={lesson.slug} progressConfigs={progressConfigs} />
            </>
          ) : (
            <>
              <Markdown source={lesson.content} excerpts={excerpts} lessonSlugs={lessonSlugs} repositoryRef={repositoryRef} />
              {lesson.exerciseIds.length > 0 && <LessonPractice lessonSlug={lesson.slug} progressConfigs={progressConfigs} />}
            </>
          )}
        </article>

        <details className="source-disclosure">
          <summary>Implementation and tests <span>Optional reference</span></summary>
          <p>Use these references to compare the explanation with repository code and tests. A test link means it imports a lesson symbol; it does not by itself claim complete behavior coverage.</p>
          <ul>
            {lesson.sourceReferences.map((reference) => {
              const testEntries = reference.testPaths.map((testPath) => ({
                path: testPath,
                symbols: Object.entries(reference.testsBySymbol)
                  .filter(([, paths]) => paths.includes(testPath))
                  .map(([symbol]) => symbol),
              }));
              return (
                <li key={reference.module}>
                  <a href={`https://github.com/ishitvagoel/BitsAndBytes/blob/${repositoryRef}/${reference.sourcePath}`} target="_blank" rel="noreferrer">
                    <code>{reference.module}</code> source <span className="sr-only">(opens in a new tab)</span>
                  </a>
                  {reference.symbols.length > 0 && <span> · Symbols: <code>{reference.symbols.join(", ")}</code></span>}
                  {testEntries.length > 0 ? (
                    <ul>
                      {testEntries.map((entry) => (
                        <li key={entry.path}>
                          <a href={`https://github.com/ishitvagoel/BitsAndBytes/blob/${repositoryRef}/tests/${entry.path}`} target="_blank" rel="noreferrer">{entry.path}<span className="sr-only"> (opens in a new tab)</span></a>
                          {entry.symbols.length > 0 && <span> imports {entry.symbols.join(", ")}</span>}
                        </li>
                      ))}
                    </ul>
                  ) : <p>No direct test import was identified for this module.</p>}
                </li>
              );
            })}
          </ul>
        </details>

        <nav className="lesson-nav" aria-label="Lesson sequence">
          {lesson.previous ? (
            <Link className="lesson-nav-link lesson-nav-previous" href={`/lessons/${lesson.previous.slug}`}>
              <span className="lesson-nav-label">Previous lesson</span>
              <span className="lesson-nav-title">{lesson.previous.title}</span>
            </Link>
          ) : <span />}
          {lesson.next ? (
            <Link className="lesson-nav-link lesson-nav-next" href={`/lessons/${lesson.next.slug}`}>
              <span className="lesson-nav-label">Next lesson</span>
              <span className="lesson-nav-title">{lesson.next.title}</span>
            </Link>
          ) : <span />}
        </nav>
      </div>

      <aside className="lesson-aside" aria-label="Lesson details">
        <details className="course-rail-disclosure" open>
          <summary>Course lessons</summary>
          <LessonCourseNav lessons={courseLinks} currentSlug={lesson.slug} />
        </details>
        <div className="aside-card">
          <p className="eyebrow">In this lesson</p>
          <p>{lesson.slug === "binary-search" ? "Trace a search, reason about boundaries, and check your understanding." : lesson.title}</p>
          <a href={`#${sections[0]?.id ?? ""}`}>Back to lesson start ↑</a>
        </div>
        <div className="aside-card aside-next">
          <p className="eyebrow">Keep going</p>
          {lesson.next ? (
            <Link href={`/lessons/${lesson.next.slug}`}>{lesson.next.title} <span aria-hidden="true">→</span></Link>
          ) : <Link href="/">Browse the course guide <span aria-hidden="true">→</span></Link>}
        </div>
      </aside>
    </main>
  );
}
