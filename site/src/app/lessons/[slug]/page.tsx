import Link from "next/link";
import { notFound } from "next/navigation";
import ReactMarkdown from "react-markdown";

import {
  formatModuleNames,
  getAllLessons,
  getLessonBySlug,
} from "@/lib/lessons";

type LessonPageProps = {
  params: Promise<{ slug: string }>;
};

export function generateStaticParams() {
  return getAllLessons().map((lesson) => ({ slug: lesson.slug }));
}

export async function generateMetadata({ params }: LessonPageProps) {
  const { slug } = await params;
  const lesson = getLessonBySlug(slug);
  if (!lesson) {
    return { title: "Lesson not found" };
  }
  return { title: lesson.title };
}

export default async function LessonPage({ params }: LessonPageProps) {
  const { slug } = await params;
  const lessons = getAllLessons();
  const lesson = getLessonBySlug(slug);
  if (!lesson) {
    notFound();
  }

  const modules = formatModuleNames(lesson.module);
  const position = lessons.findIndex((item) => item.slug === lesson.slug) + 1;
  const total = lessons.length;

  return (
    <main className="page lesson-page">
      <p className="back-link">
        <Link href="/">← All lessons</Link>
      </p>
      <p className="lesson-progress" aria-label="Position in curriculum">
        Lesson {position} of {total}
      </p>
      <h1>{lesson.title}</h1>
      <p className="lesson-status-line">
        Status:{" "}
        <span className={`status-badge status-${lesson.status}`}>{lesson.status}</span>
      </p>
      <section className="module-list" aria-label="Python modules">
        <h2>Modules</h2>
        <ul>
          {modules.map((name) => (
            <li key={name}>
              <code>{name}</code>
            </li>
          ))}
        </ul>
      </section>
      <article className="lesson-body">
        <ReactMarkdown>{lesson.content}</ReactMarkdown>
      </article>
      <nav className="lesson-nav" aria-label="Lesson sequence">
        {lesson.previous ? (
          <Link className="lesson-nav-link lesson-nav-previous" href={`/lessons/${lesson.previous.slug}`}>
            <span className="lesson-nav-label">Previous</span>
            <span className="lesson-nav-title">{lesson.previous.title}</span>
          </Link>
        ) : (
          <span className="lesson-nav-spacer" />
        )}
        {lesson.next ? (
          <Link className="lesson-nav-link lesson-nav-next" href={`/lessons/${lesson.next.slug}`}>
            <span className="lesson-nav-label">Next</span>
            <span className="lesson-nav-title">{lesson.next.title}</span>
          </Link>
        ) : (
          <span className="lesson-nav-spacer" />
        )}
      </nav>
    </main>
  );
}
