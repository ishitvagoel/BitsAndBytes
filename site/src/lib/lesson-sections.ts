import type { Lesson } from "@/lib/lessons";
import { getSections, type LessonSection } from "@/lib/markdown-sections";

export function getLessonSections(lesson: Pick<Lesson, "slug" | "content" | "exerciseIds">): LessonSection[] {
  const sections = getSections(lesson.content);
  const withTrace = [...sections];
  if (lesson.slug === "binary-search") {
    const ideaIndex = sections.findIndex((section) => section.title === "The idea: keep only possible answers");
    withTrace.splice(ideaIndex < 0 ? 0 : ideaIndex, 0, {
      id: "trace-section",
      title: "Interactive trace",
      level: 2,
    });
  }
  if (lesson.exerciseIds.length > 0) withTrace.push({ id: "practice-section", title: "Check your understanding", level: 2 });
  return withTrace;
}
