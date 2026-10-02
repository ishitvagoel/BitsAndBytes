import fs from "fs";
import path from "path";

const REQUIRED_KEYS = ["title", "slug", "order", "status", "module"] as const;

export type LessonMeta = {
  title: string;
  slug: string;
  order: number;
  status: string;
  module: string;
};

export type Lesson = LessonMeta & {
  content: string;
};

function getGuideDir(): string {
  return path.join(process.cwd(), "..", "guide");
}

/** Python-style `str.split(sep, maxsplit)` (JS `split` limit differs). */
function splitWithMaxSplits(text: string, separator: string, maxSplits: number): string[] {
  const parts: string[] = [];
  let remaining = text;
  for (let i = 0; i < maxSplits; i++) {
    const index = remaining.indexOf(separator);
    if (index === -1) {
      parts.push(remaining);
      return parts;
    }
    parts.push(remaining.slice(0, index));
    remaining = remaining.slice(index + separator.length);
  }
  parts.push(remaining);
  return parts;
}

/** Matches guide/check_lessons.py — simple key: value lines, not full YAML. */
function parseFrontmatter(text: string): { meta: Record<string, string>; body: string } {
  if (!text.startsWith("---")) {
    throw new Error("missing YAML frontmatter");
  }
  const parts = splitWithMaxSplits(text, "---", 2);
  if (parts.length < 3) {
    throw new Error("unclosed YAML frontmatter");
  }

  const frontmatterBlock = parts[1];
  const body = parts[2].replace(/^\n/, "");

  const meta: Record<string, string> = {};
  for (const line of frontmatterBlock.trim().split("\n")) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) {
      continue;
    }
    const colonIndex = trimmed.indexOf(":");
    if (colonIndex === -1) {
      throw new Error(`invalid frontmatter line: ${trimmed}`);
    }
    const key = trimmed.slice(0, colonIndex).trim();
    const value = trimmed.slice(colonIndex + 1).trim();
    meta[key] = value;
  }

  return { meta, body };
}

function parseLessonFile(filePath: string): Lesson {
  const raw = fs.readFileSync(filePath, "utf-8");
  const { meta, body } = parseFrontmatter(raw);

  for (const key of REQUIRED_KEYS) {
    if (!meta[key]) {
      throw new Error(`${path.basename(filePath)}: missing frontmatter key "${key}"`);
    }
  }

  const order = Number(meta.order);
  if (!Number.isInteger(order)) {
    throw new Error(`${path.basename(filePath)}: order must be an integer`);
  }

  return {
    title: meta.title,
    slug: meta.slug,
    order,
    status: meta.status,
    module: meta.module,
    content: body.trim(),
  };
}

export function getAllLessons(): Lesson[] {
  const guideDir = getGuideDir();
  const files = fs
    .readdirSync(guideDir)
    .filter((name) => name.endsWith(".md"))
    .sort();

  const lessons = files.map((name) => parseLessonFile(path.join(guideDir, name)));
  lessons.sort((a, b) => a.order - b.order);
  return lessons;
}

export function getLessonBySlug(slug: string): Lesson | undefined {
  return getAllLessons().find((lesson) => lesson.slug === slug);
}

export function formatModuleNames(moduleField: string): string[] {
  return moduleField
    .split(",")
    .map((part) => part.trim())
    .filter(Boolean);
}
