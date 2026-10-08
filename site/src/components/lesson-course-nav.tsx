import Link from "next/link";

export type CourseLink = {
  slug: string;
  title: string;
  stageTitle: string;
  editorialState: string;
};

function chapterHeadingId(title: string) {
  const slug = title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  return `course-chapter-${slug}`;
}

export function CoursePlace({
  lessons,
  currentSlug,
  currentTitle,
  currentStage,
}: {
  lessons: CourseLink[];
  currentSlug: string;
  currentTitle: string;
  currentStage: string;
}) {
  const chapters: Array<{ title: string; lessons: CourseLink[] }> = [];
  for (const lesson of lessons) {
    const chapter = chapters[chapters.length - 1];
    if (!chapter || chapter.title !== lesson.stageTitle) {
      chapters.push({ title: lesson.stageTitle, lessons: [lesson] });
    } else {
      chapter.lessons.push(lesson);
    }
  }

  return (
    <section className="course-place" aria-labelledby="course-place-title">
      <div className="course-place-heading">
        <h2 id="course-place-title">Course place</h2>
        <p>{currentStage} · {currentTitle}</p>
      </div>
      <div className="course-place-chapters">
        {chapters.map((chapter) => {
          const headingId = chapterHeadingId(chapter.title);
          return (
            <section className="course-chapter" aria-labelledby={headingId} key={chapter.title}>
              <h3 id={headingId}>{chapter.title}</h3>
              <ol>
                {chapter.lessons.map((item) => (
                  <li key={item.slug} className={item.slug === currentSlug ? "course-place-current" : undefined}>
                    <Link href={`/lessons/${item.slug}`} aria-current={item.slug === currentSlug ? "page" : undefined}>
                      {item.title}
                    </Link>
                  </li>
                ))}
              </ol>
            </section>
          );
        })}
      </div>
    </section>
  );
}
