"use client";

import { useRef, useState, useSyncExternalStore } from "react";
import traceFixtures from "@/data/binary-search-traces.json";
import exerciseFixtures from "@/data/exercises.json";
import { practiceStorageKey } from "@/lib/practice-storage";
import {
  LEARNING_PROGRESS_EVENT,
  LEARNING_PROGRESS_KEY,
  emptyLearningProgress,
  validateLearningProgress,
  validateLearningProgressImport,
  type LearningProgress,
  type LessonProgressConfig,
} from "@/lib/learning-progress";

const RESUME_KEY = "bitsandbytes.resume.v1";
const TRACE_KEY = "bitsandbytes.binary-search-trace.v1";
const LEARNING_KEY = LEARNING_PROGRESS_KEY;

type Lesson = { slug: string; sections: Array<{ id: string }> };
type StoredBundle = {
  schemaVersion: 1;
  exportedAt: string;
  resume: { version: 1; slug: string; sectionId: string | null } | null;
  trace: { scenarioId: string; frameIndex: number } | null;
  practice: Record<string, { selected: string; checked: boolean; hintIndex?: number }>;
  learning: LearningProgress;
};

const traces = traceFixtures as Array<{ id: string; frames: unknown[] }>;
const exercises = exerciseFixtures as Array<{ lessonSlug: string; storageId: string; options: Array<{ id: string }>; hints?: string[] }>;
const practiceSlugs = [...new Set(exercises.map((exercise) => exercise.lessonSlug))];

function readCurrent(progressConfigs: Record<string, LessonProgressConfig>): StoredBundle {
  const parse = (key: string) => {
    try {
      return JSON.parse(window.localStorage.getItem(key) ?? "null") as unknown;
    } catch {
      return null;
    }
  };
  const resume = parse(RESUME_KEY);
  const trace = parse(TRACE_KEY);
  const practice: StoredBundle["practice"] = {};
  for (const slug of practiceSlugs) {
    const saved = parse(practiceStorageKey(slug));
    if (saved && typeof saved === "object" && !Array.isArray(saved)) {
      Object.assign(practice, saved);
    }
  }
  return {
    schemaVersion: 1,
    exportedAt: new Date().toISOString(),
    resume: resume && typeof resume === "object" ? resume as StoredBundle["resume"] : null,
    trace: trace && typeof trace === "object" ? trace as StoredBundle["trace"] : null,
    practice: practice && typeof practice === "object" && !Array.isArray(practice)
      ? practice as StoredBundle["practice"]
      : {},
    learning: validateLearningProgress(parse(LEARNING_KEY), progressConfigs),
  };
}

function validateBundle(value: unknown, lessons: Lesson[], progressConfigs: Record<string, LessonProgressConfig>): StoredBundle | null {
  if (!value || typeof value !== "object" || Array.isArray(value)) return null;
  const candidate = value as Partial<StoredBundle>;
  if (candidate.schemaVersion !== 1 || !candidate.practice || typeof candidate.practice !== "object" || Array.isArray(candidate.practice)) return null;

  let resume: StoredBundle["resume"] = null;
  if (candidate.resume !== null && candidate.resume !== undefined) {
    const saved = candidate.resume as Partial<NonNullable<StoredBundle["resume"]>>;
    const lesson = lessons.find((item) => item.slug === saved.slug);
    if (saved.version !== 1 || !lesson || (saved.sectionId !== null && typeof saved.sectionId !== "string")) return null;
    if (saved.sectionId && !lesson.sections.some((section) => section.id === saved.sectionId)) return null;
    resume = { version: 1, slug: lesson.slug, sectionId: saved.sectionId ?? null };
  }

  let trace: StoredBundle["trace"] = null;
  if (candidate.trace !== null && candidate.trace !== undefined) {
    const saved = candidate.trace as Partial<NonNullable<StoredBundle["trace"]>>;
    const scenario = traces.find((item) => item.id === saved.scenarioId);
    if (!scenario || !Number.isInteger(saved.frameIndex) || (saved.frameIndex as number) < 0 || (saved.frameIndex as number) >= scenario.frames.length) return null;
    trace = { scenarioId: scenario.id, frameIndex: saved.frameIndex as number };
  }

  const practice: StoredBundle["practice"] = {};
  for (const exercise of exercises) {
    const saved = candidate.practice[exercise.storageId];
    if (saved === undefined) continue;
    if (!saved || typeof saved !== "object" || typeof saved.selected !== "string" || typeof saved.checked !== "boolean") return null;
    if (saved.selected && !exercise.options.some((option) => option.id === saved.selected)) return null;
    if (!saved.selected && saved.checked) return null;
    const hintIndex = saved.hintIndex ?? 0;
    if (!Number.isInteger(hintIndex) || hintIndex < 0 || hintIndex > (exercise.hints?.length ?? 0)) return null;
    practice[exercise.storageId] = { selected: saved.selected, checked: saved.checked, hintIndex };
  }
  if (Object.keys(candidate.practice).some((id) => !exercises.some((exercise) => exercise.storageId === id))) return null;
  const learning = validateLearningProgressImport(candidate.learning, progressConfigs);
  if (!learning) return null;
  return { schemaVersion: 1, exportedAt: typeof candidate.exportedAt === "string" ? candidate.exportedAt : "", resume, trace, practice, learning };
}

function notifyLocalState(key: string) {
  window.dispatchEvent(new Event(`bitsandbytes:local-state:${key}`));
}

export function LocalProgressTools({
  lessons,
  progressConfigs,
}: {
  lessons: Lesson[];
  progressConfigs: Record<string, LessonProgressConfig>;
}) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [status, setStatus] = useState("");

  function exportProgress() {
    try {
      const data = JSON.stringify(readCurrent(progressConfigs), null, 2);
      const url = URL.createObjectURL(new Blob([data], { type: "application/json" }));
      const link = document.createElement("a");
      link.href = url;
      link.download = "bitsandbytes-learning-progress.json";
      link.click();
      URL.revokeObjectURL(url);
      setStatus("Progress exported to a JSON file on this device.");
    } catch {
      setStatus("Progress could not be exported in this browser.");
    }
  }

  async function importProgress(file?: File) {
    if (!file) return;
    try {
      const parsed: unknown = JSON.parse(await file.text());
      const bundle = validateBundle(parsed, lessons, progressConfigs);
      if (!bundle) throw new Error("This file does not match the supported progress format.");
      const defaultTrace = { scenarioId: traces[0].id, frameIndex: 0 };
      const practiceBySlug = new Map<string, StoredBundle["practice"]>();
      for (const slug of practiceSlugs) practiceBySlug.set(slug, {});
      for (const [storageId, saved] of Object.entries(bundle.practice)) {
        const owner = exercises.find((exercise) => exercise.storageId === storageId);
        const bucket = owner ? practiceBySlug.get(owner.lessonSlug) : undefined;
        if (!bucket) continue;
        bucket[storageId] = saved;
      }
      const values: Array<[string, unknown, boolean]> = [
        [RESUME_KEY, bundle.resume, bundle.resume === null],
        [TRACE_KEY, bundle.trace ?? defaultTrace, false],
        [LEARNING_KEY, bundle.learning, false],
        ...practiceSlugs.map((slug) => [practiceStorageKey(slug), practiceBySlug.get(slug) ?? {}, false] as [string, unknown, boolean]),
      ];
      const previous = values.map(([key]) => [key, window.localStorage.getItem(key)] as const);
      try {
        for (const [key, value, remove] of values) {
          if (remove) window.localStorage.removeItem(key);
          else window.localStorage.setItem(key, JSON.stringify(value));
        }
      } catch {
        let restored = true;
        for (const [key, oldValue] of previous) {
          try {
            if (oldValue === null) window.localStorage.removeItem(key);
            else window.localStorage.setItem(key, oldValue);
          } catch {
            restored = false;
          }
        }
        throw new Error(restored
          ? "Progress could not be imported. Your previous saved data was restored."
          : "Progress import failed and browser storage prevented full rollback. Check device storage before trying again.");
      }
      for (const [key] of values) notifyLocalState(key);
      window.dispatchEvent(new Event("bitsandbytes:resume"));
      window.dispatchEvent(new Event(LEARNING_PROGRESS_EVENT));
      setStatus("Progress imported and checked against the current lessons and exercises.");
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Progress could not be imported.");
    } finally {
      if (inputRef.current) inputRef.current.value = "";
    }
  }

  function resetProgress() {
    try {
      for (const key of [RESUME_KEY, TRACE_KEY, LEARNING_KEY, ...practiceSlugs.map(practiceStorageKey)]) {
        if (key === TRACE_KEY) window.localStorage.setItem(key, JSON.stringify({ scenarioId: traces[0].id, frameIndex: 0 }));
        else if (key === LEARNING_KEY) window.localStorage.setItem(key, JSON.stringify(emptyLearningProgress()));
        else if (key.startsWith("bitsandbytes.practice.")) window.localStorage.setItem(key, "{}");
        else window.localStorage.removeItem(key);
        notifyLocalState(key);
      }
      window.dispatchEvent(new Event("bitsandbytes:resume"));
      window.dispatchEvent(new Event(LEARNING_PROGRESS_EVENT));
      setStatus("Device-local learning progress on this browser has been cleared.");
    } catch {
      setStatus("Progress could not be reset in this browser.");
    }
  }

  const stored = useSyncExternalStore(
    (callback) => {
      window.addEventListener("storage", callback);
      window.addEventListener("bitsandbytes:resume", callback);
      window.addEventListener(LEARNING_PROGRESS_EVENT, callback);
      return () => {
        window.removeEventListener("storage", callback);
        window.removeEventListener("bitsandbytes:resume", callback);
        window.removeEventListener(LEARNING_PROGRESS_EVENT, callback);
      };
    },
    () => {
      try {
        return `${window.localStorage.getItem(RESUME_KEY) ?? ""}|${window.localStorage.getItem(LEARNING_KEY) ?? ""}`;
      } catch {
        return "";
      }
    },
    () => "",
  );
  const hasProgress = stored.split("|").some((part) => part && part !== "null" && part !== '{"schemaVersion":1,"lessons":{}}');
  if (!hasProgress) return null;

  return (
    <details className="progress-tools">
      <summary>Manage device-local progress</summary>
      <p>Export or import your saved lesson location, trace step and practice choices. The file stays on your device unless you choose to move it.</p>
      <div className="progress-tool-actions">
        <button type="button" className="button button-secondary" onClick={exportProgress}>Export progress</button>
        <button type="button" className="button button-secondary" onClick={() => inputRef.current?.click()}>Import progress</button>
        <button type="button" className="button button-secondary" onClick={resetProgress}>Reset progress</button>
        <input ref={inputRef} type="file" accept="application/json,.json" className="sr-only" aria-label="Choose a Bits and Bytes progress JSON file" onChange={(event) => void importProgress(event.target.files?.[0])} />
      </div>
      <p className="progress-tools-status" role="status" aria-live="polite">{status}</p>
    </details>
  );
}
