import fs from "fs";
import path from "path";
import lessonReferences from "@/data/lesson-references.json";
import { curriculumDetails, curriculumLessons, curriculumObjectiveIds, curriculumStages, type EditorialState } from "@/lib/curriculum";

const REQUIRED_KEYS = ["title", "slug", "order", "status", "module"] as const;

type LessonFileMeta = {
  title: string;
  slug: string;
  order: number;
  status: string;
  module: string;
};

export type LessonSourceReference = {
  module: string;
  sourcePath: string;
  symbols: string[];
  testsBySymbol: Record<string, string[]>;
  testPaths: string[];
};

const sourceTestManifest = lessonReferences as unknown as Record<string, { modules: LessonSourceReference[] }>;

export type LessonMeta = LessonFileMeta & {
  id: string;
  summary: string;
  editorialState: EditorialState;
  stageId: string;
  stageTitle: string;
  prerequisites: Array<Pick<LessonMeta, "slug" | "title">>;
  contentVersion: number;
  contentReadiness: "ready" | "partial" | "summary" | "reference";
  estimatedMinutes: number;
  outcomes: string[];
  objectiveIds: string[];
  traceIds: string[];
  exerciseIds: string[];
  sourceReferences: LessonSourceReference[];
};

type LessonCore = LessonFileMeta & {
  content: string;
};

export type Lesson = LessonCore & Pick<LessonMeta, "id" | "summary" | "editorialState" | "stageId" | "stageTitle" | "prerequisites" | "contentVersion" | "contentReadiness" | "estimatedMinutes" | "outcomes" | "objectiveIds" | "traceIds" | "exerciseIds" | "sourceReferences"> & {
  previous?: LessonMeta;
  next?: LessonMeta;
};

export type LessonStage = {
  id: string;
  title: string;
  description: string;
  lessons: Lesson[];
};

let lessonsCache: Lesson[] | null = null;

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

function parseLessonFile(filePath: string): LessonCore {
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

function metadata(lesson: LessonCore, stageId: string, stageTitle: string): LessonMeta {
  const curriculum = curriculumLessons[lesson.slug];
  const detail = curriculumDetails[lesson.slug];
  const objectiveIds = curriculumObjectiveIds[lesson.slug];
  const references = sourceTestManifest[lesson.slug]?.modules;
  if (!curriculum) throw new Error(`Missing curriculum metadata for ${lesson.slug}`);
  if (!detail) throw new Error(`Missing curriculum details for ${lesson.slug}`);
  if (!objectiveIds || objectiveIds.length !== detail.outcomes.length) throw new Error(`Learning objective IDs do not match outcomes for ${lesson.slug}`);
  if (!references) throw new Error(`Missing source/test references for ${lesson.slug}`);
  const words = lesson.content.trim().split(/\s+/).filter(Boolean).length;
  const derivedMinutes = Math.max(
    2,
    Math.round(words / 180) + detail.exerciseIds.length * 2 + (detail.traceIds.length > 0 ? 3 : 0),
  );
  return {
    title: lesson.title,
    slug: lesson.slug,
    order: lesson.order,
    status: lesson.status,
    module: lesson.module,
    id: curriculum.id,
    summary: curriculum.summary,
    editorialState: curriculum.editorialState,
    stageId,
    stageTitle,
    prerequisites: curriculum.prerequisites.map((slug) => {
      const prerequisite = lessonTitles.get(slug);
      if (!prerequisite) throw new Error(`${lesson.slug} has unknown prerequisite ${slug}`);
      return { slug, title: prerequisite };
    }),
    ...detail,
    estimatedMinutes: derivedMinutes,
    objectiveIds,
    sourceReferences: references,
  };
}

function attachAdjacentLessons(lessons: LessonCore[], stageBySlug: Map<string, { id: string; title: string }>): Lesson[] {
  const learningSequence = lessons.filter((lesson) => curriculumLessons[lesson.slug].editorialState !== "reference");
  return lessons.map((lesson) => {
    const stage = stageBySlug.get(lesson.slug);
    if (!stage) throw new Error(`Missing curriculum stage for ${lesson.slug}`);
    const sequenceIndex = learningSequence.findIndex((item) => item.slug === lesson.slug);
    const previous = sequenceIndex > 0 ? learningSequence[sequenceIndex - 1] : undefined;
    const next = sequenceIndex >= 0 && sequenceIndex < learningSequence.length - 1
      ? learningSequence[sequenceIndex + 1]
      : undefined;
    return {
      ...lesson,
      ...metadata(lesson, stage.id, stage.title),
      ...(previous ? { previous: metadata(previous, stageBySlug.get(previous.slug)!.id, stageBySlug.get(previous.slug)!.title) } : {}),
      ...(next ? { next: metadata(next, stageBySlug.get(next.slug)!.id, stageBySlug.get(next.slug)!.title) } : {}),
    };
  });
}

const lessonTitles = new Map<string, string>();

function validateCurriculum(lessons: LessonCore[]): Map<string, { id: string; title: string }> {
  const bySlug = new Map(lessons.map((lesson) => [lesson.slug, lesson]));
  if (bySlug.size !== lessons.length) throw new Error("Duplicate lesson slugs in guide files");
  const orders = new Set<number>();
  for (const lesson of lessons) {
    if (orders.has(lesson.order)) throw new Error(`Duplicate frontmatter order ${lesson.order}`);
    orders.add(lesson.order);
  }
  lessonTitles.clear();
  for (const lesson of lessons) lessonTitles.set(lesson.slug, lesson.title);

  const stageBySlug = new Map<string, { id: string; title: string }>();
  const ids = new Set<string>();
  const traceIds = new Set<string>();
  const exerciseIds = new Set<string>();
  const objectiveIds = new Set<string>();
  for (const stage of curriculumStages) {
    for (const slug of stage.slugs) {
      if (stageBySlug.has(slug)) throw new Error(`Lesson ${slug} appears in multiple curriculum stages`);
      if (!bySlug.has(slug)) throw new Error(`Curriculum stage ${stage.id} references unknown lesson ${slug}`);
      stageBySlug.set(slug, { id: stage.id, title: stage.title });
    }
  }
  for (const slug of bySlug.keys()) {
    const sourceLesson = bySlug.get(slug)!;
    if (!stageBySlug.has(slug)) throw new Error(`Lesson ${slug} is missing a curriculum stage`);
    const meta = curriculumLessons[slug];
    const detail = curriculumDetails[slug];
    const references = sourceTestManifest[slug]?.modules;
    if (!meta) throw new Error(`Lesson ${slug} is missing curriculum metadata`);
    if (ids.has(meta.id)) throw new Error(`Duplicate curriculum lesson ID ${meta.id}`);
    ids.add(meta.id);
    if (!meta.summary.trim()) throw new Error(`Lesson ${slug} is missing a summary`);
    if (!detail) throw new Error(`Lesson ${slug} is missing content details`);
    if (!references) throw new Error(`Lesson ${slug} is missing source/test reference data`);
    const expectedModules = sourceLesson.module.split(",").map((part) => part.trim());
    if (references.length !== expectedModules.length || expectedModules.some((module, index) => references[index]?.module !== module)) {
      throw new Error(`Lesson ${slug} has source references that do not match its module frontmatter`);
    }
    for (const reference of references) {
      if (!reference.sourcePath.endsWith(".py")) throw new Error(`${slug} has a source reference without a Python path`);
      if (reference.testPaths.some((testPath) => !/^test_[\w-]+\.py$/.test(testPath))) throw new Error(`${slug} has an invalid test reference`);
    }
    if (!Number.isInteger(detail.contentVersion) || detail.contentVersion < 1) throw new Error(`Lesson ${slug} has an invalid content version`);
    if (!Number.isInteger(detail.estimatedMinutes) || detail.estimatedMinutes < 1) throw new Error(`Lesson ${slug} has an invalid estimated duration`);
    if (detail.outcomes.length === 0 || detail.outcomes.some((outcome) => !outcome.trim())) throw new Error(`Lesson ${slug} needs learner-visible outcomes`);
    const lessonObjectives = curriculumObjectiveIds[slug];
    if (!lessonObjectives || lessonObjectives.length !== detail.outcomes.length) throw new Error(`Lesson ${slug} needs one stable ID for each objective`);
    for (const objectiveId of lessonObjectives) {
      if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(objectiveId) || objectiveIds.has(objectiveId)) throw new Error(`Invalid or duplicate objective ID ${objectiveId}`);
      objectiveIds.add(objectiveId);
    }
    if (meta.editorialState === "pilot" && detail.contentReadiness !== "ready") throw new Error(`${slug} pilot status and content readiness disagree`);
    if (meta.editorialState === "reference" && detail.contentReadiness !== "reference") throw new Error(`${slug} reference status and content readiness disagree`);
    for (const traceId of detail.traceIds) {
      if (traceIds.has(traceId)) throw new Error(`Duplicate trace ID ${traceId}`);
      traceIds.add(traceId);
    }
    for (const exerciseId of detail.exerciseIds) {
      if (exerciseIds.has(exerciseId)) throw new Error(`Duplicate exercise ID ${exerciseId}`);
      exerciseIds.add(exerciseId);
    }
  }
  for (const slug of Object.keys(curriculumLessons)) {
    if (!bySlug.has(slug)) throw new Error(`Curriculum metadata references unknown lesson ${slug}`);
  }
  for (const slug of Object.keys(curriculumDetails)) {
    if (!bySlug.has(slug)) throw new Error(`Curriculum details reference unknown lesson ${slug}`);
  }
  for (const slug of Object.keys(curriculumObjectiveIds)) {
    if (!bySlug.has(slug)) throw new Error(`Objective IDs reference unknown lesson ${slug}`);
  }
  for (const slug of Object.keys(sourceTestManifest)) {
    if (!bySlug.has(slug)) throw new Error(`Source/test references point to unknown lesson ${slug}`);
  }

  const visiting = new Set<string>();
  const visited = new Set<string>();
  const visit = (slug: string) => {
    if (visiting.has(slug)) throw new Error(`Prerequisite cycle includes ${slug}`);
    if (visited.has(slug)) return;
    visiting.add(slug);
    for (const prerequisite of curriculumLessons[slug].prerequisites) {
      if (!bySlug.has(prerequisite)) throw new Error(`${slug} has unknown prerequisite ${prerequisite}`);
      visit(prerequisite);
    }
    visiting.delete(slug);
    visited.add(slug);
  };
  for (const slug of bySlug.keys()) visit(slug);
  return stageBySlug;
}

export function getAllLessons(): Lesson[] {
  if (lessonsCache) return lessonsCache;
  const guideDir = getGuideDir();
  const files = fs
    .readdirSync(guideDir)
    .filter((name) => name.endsWith(".md"))
    .sort();

  const lessons = files.map((name) => parseLessonFile(path.join(guideDir, name)));
  const stageBySlug = validateCurriculum(lessons);
  const bySlug = new Map(lessons.map((lesson) => [lesson.slug, lesson]));
  const orderedLessons = curriculumStages.flatMap((stage) => stage.slugs.map((slug) => bySlug.get(slug)!));
  lessonsCache = attachAdjacentLessons(orderedLessons, stageBySlug);
  return lessonsCache;
}

export function getCurriculumStages(): LessonStage[] {
  const lessons = getAllLessons();
  const bySlug = new Map(lessons.map((lesson) => [lesson.slug, lesson]));
  return curriculumStages.map((stage) => ({
    ...stage,
    lessons: stage.slugs.map((slug) => bySlug.get(slug)!),
  }));
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
