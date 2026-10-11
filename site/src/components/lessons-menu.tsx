"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useRef, useState } from "react";

type MenuLesson = {
  slug: string;
  title: string;
  stageTitle: string;
};

export function LessonsMenu({ lessons }: { lessons: MenuLesson[] }) {
  const pathname = usePathname();
  const currentSlug = pathname.split("/").at(-1) ?? "";
  const [open, setOpen] = useState(false);
  const closeRef = useRef<HTMLButtonElement>(null);
  const openRef = useRef<HTMLButtonElement>(null);
  const panelRef = useRef<HTMLDivElement>(null);
  const stages = lessons.reduce<Array<{ title: string; lessons: MenuLesson[] }>>((groups, lesson) => {
    const current = groups.at(-1);
    if (current && current.title === lesson.stageTitle) current.lessons.push(lesson);
    else groups.push({ title: lesson.stageTitle, lessons: [lesson] });
    return groups;
  }, []);

  useEffect(() => {
    if (!open) return;
    closeRef.current?.focus();
    panelRef.current?.querySelector<HTMLElement>("[aria-current='page']")?.scrollIntoView({ block: "center" });
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setOpen(false);
        openRef.current?.focus();
      }
      if (event.key !== "Tab" || !panelRef.current) return;
      const items = [...panelRef.current.querySelectorAll<HTMLElement>("button, a")];
      const first = items[0];
      const last = items.at(-1);
      if (!first || !last) return;
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open]);

  function close() {
    setOpen(false);
    openRef.current?.focus();
  }

  return (
    <>
      <button
        ref={openRef}
        className="lessons-menu-button"
        type="button"
        aria-expanded={open}
        aria-controls="lessons-menu-panel"
        onClick={() => setOpen(true)}
      >
        Lessons
      </button>
      {open && (
        <div className="lessons-scrim" onClick={close}>
          <div
            ref={panelRef}
            id="lessons-menu-panel"
            className="lessons-panel"
            role="dialog"
            aria-modal="true"
            aria-label="Lessons"
            onClick={(event) => event.stopPropagation()}
          >
            <button ref={closeRef} className="lessons-menu-button" type="button" onClick={close}>Close</button>
            <nav aria-label="Lessons">
              {stages.map((stage) => (
                <section key={stage.title}>
                  <h3>{stage.title}</h3>
                  <ol>
                    {stage.lessons.map((lesson) => (
                      <li key={lesson.slug}>
                        <Link
                          href={`/lessons/${lesson.slug}`}
                          aria-current={lesson.slug === currentSlug ? "page" : undefined}
                          onClick={close}
                        >
                          <span>{lessons.findIndex((item) => item.slug === lesson.slug) + 1}</span>
                          <span>{lesson.title}</span>
                        </Link>
                      </li>
                    ))}
                  </ol>
                </section>
              ))}
            </nav>
          </div>
        </div>
      )}
    </>
  );
}
