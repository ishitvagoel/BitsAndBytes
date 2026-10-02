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
        {lessons.map((lesson) => (
          <li key={lesson.slug}>
            <Link href={`/lessons/${lesson.slug}`}>{lesson.title}</Link>
          </li>
        ))}
      </ol>
    </main>
  );
}
