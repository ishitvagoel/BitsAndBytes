import type { Metadata } from "next";
import Link from "next/link";

import { LessonsMenu } from "@/components/lessons-menu";
import { getAllLessons } from "@/lib/lessons";

import "./globals.css";

export const metadata: Metadata = {
  title: "Bits and Bytes",
  description: "Lesson guide for the Bits and Bytes curriculum",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  const menuLessons = getAllLessons()
    .filter((lesson) => lesson.editorialState !== "reference")
    .map((lesson) => ({ slug: lesson.slug, title: lesson.title, stageTitle: lesson.stageTitle }));

  return (
    <html lang="en">
      <body>
        <div className="site-shell">
          <a className="skip-link" href="#main-content">Skip to content</a>
          <header className="site-header">
            <Link href="/">Bits and Bytes</Link>
            <div id="header-slot" />
            <LessonsMenu lessons={menuLessons} />
          </header>
          {children}
        </div>
      </body>
    </html>
  );
}
