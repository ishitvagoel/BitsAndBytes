import Link from "next/link";

export type CourseLink = {
  slug: string;
  title: string;
  stageTitle: string;
  editorialState: string;
};

export function LessonCourseNav({ lessons, currentSlug }: { lessons: CourseLink[]; currentSlug: string }) {
  return (
    <nav className="course-rail" aria-label="Course lessons">
      <ol>
        {lessons.map((item, index) => (
          <li key={item.slug} className={item.slug === currentSlug ? "course-rail-current" : undefined}>
            <Link href={`/lessons/${item.slug}`} aria-current={item.slug === currentSlug ? "page" : undefined}>
              <span className="course-rail-number">{index + 1}</span>
              <span><span className="course-rail-title">{item.title}</span><span className="course-rail-stage">{item.stageTitle}</span></span>
            </Link>
          </li>
        ))}
      </ol>
    </nav>
  );
}

export function MobileLessonMenu({ lessons, currentSlug }: { lessons: CourseLink[]; currentSlug: string }) {
  return (
    <details className="mobile-course-menu">
      <summary>Course lessons <span>{lessons.length} topics</span></summary>
      <LessonCourseNav lessons={lessons} currentSlug={currentSlug} />
    </details>
  );
}
