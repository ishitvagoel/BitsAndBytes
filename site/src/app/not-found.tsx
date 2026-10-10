import Link from "next/link";

import { getAllLessons } from "@/lib/lessons";

export default function NotFound() {
  const lessonCount = getAllLessons().filter((lesson) => lesson.editorialState !== "reference").length;

  return (
    <main id="main-content" className="not-found-page" tabIndex={-1}>
      <h1>That lesson is not in the guide.</h1>
      <p>The {lessonCount} lessons are listed on the home page.</p>
      <Link className="button button-primary" href="/">All lessons</Link>
    </main>
  );
}
