import Link from "next/link";
import dynamic from "next/dynamic";
import { notFound } from "next/navigation";
import ReactMarkdown from "react-markdown";
import { isValidElement, type ReactNode } from "react";

import { CopyableCodeBlock } from "@/components/copyable-code-block";
import { LessonHeaderSlot } from "@/components/lesson-header-slot";
import type { TraceScenario } from "@/components/trace-bench";
import { ModuleList } from "@/components/module-list";
import { CompletionControl, ResumeTracker } from "@/components/resume-progress";
import binarySearchSource from "@/data/binary-search-source.json";
import exerciseFixtures from "@/data/exercises.json";
import lessonTraces from "@/data/lesson-traces.json";
import {
  formatModuleNames,
  getAllLessons,
  getLessonBySlug,
} from "@/lib/lessons";
import { getLessonSections } from "@/lib/lesson-sections";
import { referenceLessonFor } from "@/lib/curriculum";
import { getSections, headingId } from "@/lib/markdown-sections";
import { resolveLessonMarkdownHref } from "@/lib/markdown-links";
import type { LessonProgressConfig } from "@/lib/learning-progress";

const BinarySearchLab = dynamic(
  () => import("@/components/binary-search-lab").then((module) => module.BinarySearchLab),
  { loading: () => <p className="interaction-loading" role="status">The interactive trace is loading. The written explanation and source code below remain available.</p> },
);
const TraceBench = dynamic(
  () => import("@/components/trace-bench").then((module) => module.TraceBench),
  { loading: () => <p className="interaction-loading" role="status">The interactive trace is loading. The written explanation below remains available.</p> },
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
  const chunks = source.split(/\n(?=## )/);
  const markdownProps = { excerpts, lessonSlugs, repositoryRef, renderedHeadingId };
  return (
    <>
      {chunks.map((chunk, index) => {
        const callout = chunk.startsWith("## ");
        const body = <MarkdownBlocks key={`${index}-blocks`} source={chunk} {...markdownProps} />;
        return callout
          ? <section className="heading-callout" key={`${index}-${chunk.slice(0, 24)}`}>{body}</section>
          : <div key={`${index}-plain`}>{body}</div>;
      })}
    </>
  );
}

function MarkdownBlocks({
  source,
  excerpts,
  lessonSlugs,
  repositoryRef,
  renderedHeadingId,
}: {
  source: string;
  excerpts: Record<string, SourceCodeExcerpt>;
  lessonSlugs: ReadonlySet<string>;
  repositoryRef: string;
  renderedHeadingId: (children: ReactNode) => string;
}) {
  const blocks: ReactNode[] = [];
  let prose: string[] = [];
  let table: string[] = [];
  let key = 0;
  const flushProse = () => {
    if (!prose.some((line) => line.trim())) {
      prose = [];
      return;
    }
    blocks.push(
      <ReactMarkdown key={`prose-${key++}`} components={markdownComponents(excerpts, lessonSlugs, repositoryRef, renderedHeadingId)}>
        {prose.join("\n")}
      </ReactMarkdown>,
    );
    prose = [];
  };
  const flushTable = () => {
    if (!table.length) return;
    const rows = table.map((line) => line.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((cell) => cell.trim()));
    const isRule = (row: string[]) => row.every((cell) => /^:?-+:?$/.test(cell));
    const kept = rows.filter((row) => !isRule(row));
    const [header, ...body] = kept;
    blocks.push(
      <div className="table-scroll" key={`table-${key++}`}>
        <table>
          {header ? <thead><tr>{header.map((cell, index) => <th key={`${index}-${cell}`}>{cell}</th>)}</tr></thead> : null}
          <tbody>
            {body.map((row, rowIndex) => (
              <tr key={rowIndex}>{row.map((cell, index) => <td key={`${rowIndex}-${index}`}>{cell}</td>)}</tr>
            ))}
          </tbody>
        </table>
      </div>,
    );
    table = [];
  };
  for (const line of source.split("\n")) {
    if (line.trim().startsWith("|")) {
      flushProse();
      table.push(line);
    } else {
      flushTable();
      prose.push(line);
    }
  }
  flushProse();
  flushTable();
  return <>{blocks}</>;
}

function markdownComponents(
  excerpts: Record<string, SourceCodeExcerpt>,
  lessonSlugs: ReadonlySet<string>,
  repositoryRef: string,
  renderedHeadingId: (children: ReactNode) => string,
) {
  return {
    a: ({ href, children, ...props }: { href?: string; children?: ReactNode }) => {
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
    pre: ({ children }: { children?: ReactNode }) => {
      const block = codeBlockContent(children);
      return <CopyableCodeBlock code={block.code} language={block.language} />;
    },
    p: ({ children, ...props }: { children?: ReactNode }) => {
      const marker = /^\[\[source-excerpt:([a-z0-9-]+)\]\]$/.exec(headingText(children).trim());
      const excerpt = marker ? excerpts[marker[1]] : undefined;
      if (marker && excerpt) {
        return <p><a href="#binary-search-source">Follow the current Python source and highlighted lines in the trace above.</a></p>;
      }
      if (marker) throw new Error(`Missing source excerpt for ${marker[1]}`);
      return <p {...props}>{children}</p>;
    },
    h2: ({ children, ...props }: { children?: ReactNode }) => <h2 {...props} id={renderedHeadingId(children)}>{children}</h2>,
    h3: ({ children, ...props }: { children?: ReactNode }) => <h3 {...props} id={renderedHeadingId(children)}>{children}</h3>,
  };
}

function LessonSequence({
  previous,
  next,
  sticky = false,
}: {
  previous?: { slug: string; title: string };
  next?: { slug: string; title: string };
  sticky?: boolean;
}) {
  return (
    <nav className={sticky ? "lesson-nav lesson-nav-sticky" : "lesson-nav"} aria-label={sticky ? "Pinned lesson sequence" : "Lesson sequence"}>
      {previous ? (
        <Link className="lesson-nav-link lesson-nav-previous" href={`/lessons/${previous.slug}`}>
          <span className="lesson-nav-label">Previous</span>
          <span className="lesson-nav-title">{previous.title}</span>
        </Link>
      ) : (
        <span className="lesson-nav-end" aria-disabled="true">
          <span className="lesson-nav-label">Previous</span>
          <span className="lesson-nav-title">Start of the guide</span>
        </span>
      )}
      {next ? (
        <Link className="lesson-nav-link lesson-nav-next" href={`/lessons/${next.slug}`}>
          <span className="lesson-nav-label">Next</span>
          <span className="lesson-nav-title">{next.title}</span>
        </Link>
      ) : (
        <span className="lesson-nav-end" aria-disabled="true">
          <span className="lesson-nav-label">Next</span>
          <span className="lesson-nav-title">End of the guide</span>
        </span>
      )}
    </nav>
  );
}

export function generateStaticParams() {
  return getAllLessons().map((lesson) => ({ slug: lesson.slug }));
}

export async function generateMetadata({ params }: LessonPageProps) {
  const { slug } = await params;
  const lesson = getLessonBySlug(slug);
  if (!lesson) {
    return { title: "Lesson not found" };
  }
  return {
    title: `${lesson.title} | Bits and Bytes`,
    description: lesson.summary,
    openGraph: { title: `${lesson.title} | Bits and Bytes` },
  };
}

export default async function LessonPage({ params }: LessonPageProps) {
  const { slug } = await params;
  const lessons = getAllLessons();
  const lesson = getLessonBySlug(slug);
  if (!lesson) {
    notFound();
  }

  const repositoryRef = process.env.VERCEL_GIT_COMMIT_SHA ?? "master";
  const learningSequence = lessons.filter((item) => item.editorialState !== "reference");
  const position = learningSequence.findIndex((item) => item.slug === lesson.slug) + 1;
  const sections = getLessonSections(lesson);
  const progressConfig: LessonProgressConfig = {
    contentVersion: lesson.contentVersion,
    sectionIds: sections.map((section) => section.id),
    objectiveIds: lesson.objectiveIds,
  };
  const sourceExcerpt = lesson.slug === "binary-search"
    ? {
        ...binarySearchSource,
        ...(process.env.VERCEL_GIT_COMMIT_SHA ? { commit: process.env.VERCEL_GIT_COMMIT_SHA } : {}),
      }
    : undefined;
  const excerpts: Record<string, SourceCodeExcerpt> = sourceExcerpt ? { "binary-search": sourceExcerpt } : {};
  const lessonSlugs = new Set(lessons.map((item) => item.slug));
  const genericTrace = (lessonTraces as Record<string, TraceScenario[]>)[lesson.slug];
  const hasGenericTrace = Array.isArray(genericTrace) && genericTrace.length > 0;
  const hasWorkshopBench = Boolean(sourceExcerpt) || hasGenericTrace;
  const learnerBadge = lesson.editorialState === "reference" || lesson.contentReadiness === "reference"
    ? "Reference"
    : lesson.contentReadiness === "ready" || lesson.contentReadiness === "partial"
      ? "Full lesson"
      : "Overview";
  const markdownSections = sections.filter((section) => section.id !== "trace-section" && section.id !== "practice-section");
  const lessonContext = (
    <>
      {lesson.editorialState === "reference" ? (
        <p className="prerequisite-line">This page lists the library modules for {lesson.title}. The lesson is <Link href={`/lessons/${referenceLessonFor[lesson.slug]}`}>{lessons.find((item) => item.slug === referenceLessonFor[lesson.slug])?.title}</Link>.</p>
      ) : lesson.outcomes.length <= 2 ? (
        <p className="lesson-outcomes-line">You will learn to {lesson.outcomes.map((outcome) => outcome.charAt(0).toLowerCase() + outcome.slice(1)).join(" and ")}.</p>
      ) : lesson.outcomes.length <= 4 ? (
        <section className="lesson-outcomes lesson-page-outcomes" aria-labelledby="outcomes-title">
          <h2 id="outcomes-title">What you will learn</h2>
          <ul>{lesson.outcomes.map((outcome) => <li key={outcome}>{outcome}</li>)}</ul>
        </section>
      ) : (
        <details className="lesson-outcomes lesson-page-outcomes">
          <summary>What you will learn <span>{lesson.outcomes.length}</span></summary>
          <ul>{lesson.outcomes.map((outcome) => <li key={outcome}>{outcome}</li>)}</ul>
        </details>
      )}

      {lesson.editorialState !== "reference" && lesson.prerequisites.length > 0 && (
        <p className="prerequisite-line">Recommended first: {lesson.prerequisites.map((prerequisite, index) => (
          <span key={prerequisite.slug}>{index > 0 ? ", " : ""}<Link href={`/lessons/${prerequisite.slug}`}>{prerequisite.title}</Link></span>
        ))}.</p>
      )}

      {markdownSections.filter((section) => section.title !== "Practice and next step").length >= 5 && (
        <details className="contents-panel">
          <summary>On this page <span>{markdownSections.filter((section) => section.title !== "Practice and next step").length} sections</span></summary>
          <nav aria-label="On this page">
            <ol>
              {markdownSections.filter((section) => section.title !== "Practice and next step").map((section) => (
                <li className={section.level === 3 ? "contents-subsection" : undefined} key={`${section.id}-${section.title}`}>
                  <a href={`#${section.id}`}>{section.title}</a>
                </li>
              ))}
            </ol>
          </nav>
        </details>
      )}
    </>
  );

  return (
    <main id="main-content" className={hasWorkshopBench ? "lesson-layout lesson-layout-bench" : "lesson-layout"} tabIndex={-1}>
      <div className="lesson-main-column">
        <ResumeTracker slug={lesson.slug} sections={sections.map(({ id, title }) => ({ id, title }))} progressConfig={progressConfig} completeWithoutPractice={lesson.exerciseIds.length === 0} />
        <LessonHeaderSlot>
          <p className="header-lesson-position">
            {lesson.stageTitle}
            {position > 0 ? ` · ${position} of ${learningSequence.length}` : " · Reference"}
            {lesson.next ? <> · <Link href={`/lessons/${lesson.next.slug}`}>Next</Link></> : null}
          </p>
        </LessonHeaderSlot>
        <Link className="back-link" href="/">← Course home</Link>
        <p className="sr-only">{lesson.stageTitle} · {position > 0 ? `Lesson ${position} of ${learningSequence.length}` : "Reference"}</p>
        <h1 className="lesson-title">{lesson.title}</h1>
        <p className="lesson-subtitle">
          {lesson.summary}
        </p>
        <div className="lesson-readiness">
          <span className={`readiness-label readiness-${lesson.contentReadiness}`}>{learnerBadge}</span>
          <span>About {lesson.estimatedMinutes} min</span>
        </div>

        <div className="reading-card">
        {lessonContext}

        <article className="lesson-body">
          <Markdown source={lesson.content} excerpts={excerpts} lessonSlugs={lessonSlugs} repositoryRef={repositoryRef} />
          {!hasWorkshopBench && lesson.exerciseIds.length > 0 && <LessonPractice lessonSlug={lesson.slug} progressConfig={progressConfig} questions={exerciseFixtures.filter((exercise) => exercise.lessonSlug === lesson.slug)} />}
        </article>

        <details className="source-disclosure">
          <summary>Implementation and tests <span>Optional reference</span></summary>
          <ModuleList names={formatModuleNames(lesson.module)} />
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

        <CompletionControl slug={lesson.slug} progressConfig={progressConfig} />
        <LessonSequence previous={lesson.previous} next={lesson.next} />
        <LessonSequence previous={lesson.previous} next={lesson.next} sticky />
        </div>

        {hasWorkshopBench && (
          <div className="workshop-bench">
            <div className="workshop-trace">
              {sourceExcerpt ? (
                <BinarySearchLab sourceCode={sourceExcerpt.code} sourcePath={sourceExcerpt.sourcePath} sourceCommit={sourceExcerpt.commit} traceLines={sourceExcerpt.traceLines} />
              ) : (
                <TraceBench lessonSlug={lesson.slug} scenarios={genericTrace} />
              )}
            </div>
            <div className="workshop-check">
              <LessonPractice lessonSlug={lesson.slug} progressConfig={progressConfig} questions={exerciseFixtures.filter((exercise) => exercise.lessonSlug === lesson.slug)} />
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
