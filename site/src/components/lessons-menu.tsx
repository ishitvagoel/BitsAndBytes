"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

type MenuLesson = {
  slug: string;
  title: string;
  stageTitle: string;
};

export function LessonsMenu({ lessons }: { lessons: MenuLesson[] }) {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (!open) return;
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") setOpen(false);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open]);

  return (
    <>
      <button
        className="lessons-menu-button"
        type="button"
        aria-expanded={open}
        aria-controls="lessons-menu-panel"
        onClick={() => setOpen((value) => !value)}
      >
        Lessons
      </button>
      {open && (
        <div className="lessons-scrim" onClick={() => setOpen(false)}>
          <nav id="lessons-menu-panel" className="lessons-panel" aria-label="Lessons" onClick={(event) => event.stopPropagation()}>
            <ol>
              {lessons.map((lesson, index) => (
                <li key={lesson.slug}>
                  <Link href={`/lessons/${lesson.slug}`} onClick={() => setOpen(false)}>
                    <span>{index + 1}</span>
                    <span>{lesson.title}</span>
                    <span>{lesson.stageTitle}</span>
                  </Link>
                </li>
              ))}
            </ol>
          </nav>
        </div>
      )}
    </>
  );
}
