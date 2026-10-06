import Link from "next/link";

import { getAllLessons } from "@/lib/lessons";

export default function Home() {
  const lessons = getAllLessons();

  return (
    <main className="page">
      <h1>Lessons</h1>
      <p className="lede">
        Twenty-two lessons from the Bits and Bytes guide, in curriculum order.
      </p>
      <ol className="lesson-index">
        {lessons.map((lesson, index) => (
          <li key={lesson.slug} className="lesson-index-row">
            <span className="lesson-index-position" aria-hidden="true">
              {index + 1}.
            </span>
            <div className="lesson-index-main">
              <Link href={`/lessons/${lesson.slug}`}>{lesson.title}</Link>
              <span className={`status-badge status-${lesson.status}`}>{lesson.status}</span>
            </div>
          </li>
        ))}
      </ol>
    </main>
  );
}
