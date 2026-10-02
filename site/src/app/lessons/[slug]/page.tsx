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
  const lesson = getLessonBySlug(slug);
  if (!lesson) {
    notFound();
  }

  const modules = formatModuleNames(lesson.module);

  return (
    <main className="page lesson-page">
      <p className="back-link">
        <Link href="/">← All lessons</Link>
      </p>
      <h1>{lesson.title}</h1>
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
    </main>
  );
}
