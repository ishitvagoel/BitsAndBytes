"use client";

import { useCallback, useEffect, useMemo, useSyncExternalStore } from "react";
import traceFixtures from "@/data/binary-search-traces.json";
import exerciseFixtures from "@/data/exercises.json";
import { CopyableCodeBlock } from "@/components/copyable-code-block";
import { practiceStorageKey } from "@/lib/practice-storage";
import {
  LEARNING_PROGRESS_EVENT,
  LEARNING_PROGRESS_KEY,
  recordObjectiveAttempt,
  validateLearningProgress,
  type LessonProgressConfig,
} from "@/lib/learning-progress";

type Scenario = {
  id: string;
  label: string;
  values: number[];
  target: number;
  result: number;
  frames: TraceFrame[];
};

type TraceFrame = {
  left: number;
  right: number;
  middle: number | null;
  inspected: number | null;
  message: string;
  result: "range" | "continue" | "found" | "missing";
  codeStep: string;
};

const scenarios = traceFixtures as Scenario[];

const TRACE_STORAGE_KEY = "bitsandbytes.binary-search-trace.v1";
const memoryStore = new Map<string, string>();

type PracticeQuestion = {
  id: string;
  lessonSlug: string;
  storageId: string;
  objectiveId: string;
  prompt: string;
  hints: string[];
  options: { id: string; label: string }[];
  answer: string;
  correct: string;
  retry: string;
};

const allQuestions = exerciseFixtures as PracticeQuestion[];

type SavedAnswer = { selected: string; checked: boolean; hintIndex: number };

function validateTraceState(value: unknown): { scenarioId: string; frameIndex: number } {
  if (typeof value === "object" && value !== null && "scenarioId" in value && "frameIndex" in value) {
    const state = value as { scenarioId: unknown; frameIndex: unknown };
    const scenario = scenarios.find((item) => item.id === state.scenarioId);
    if (scenario && typeof state.frameIndex === "number" && Number.isInteger(state.frameIndex)) {
      return {
        scenarioId: scenario.id,
        frameIndex: Math.max(0, Math.min(state.frameIndex, scenario.frames.length - 1)),
      };
    }
  }
  return { scenarioId: scenarios[0].id, frameIndex: 0 };
}

function validatePracticeState(value: unknown): Record<string, SavedAnswer> {
  if (typeof value !== "object" || value === null || Array.isArray(value)) return {};
  const answers: Record<string, SavedAnswer> = {};
  for (const question of allQuestions) {
    const raw = (value as Record<string, unknown>)[question.storageId];
    if (typeof raw !== "object" || raw === null || !("selected" in raw) || !("checked" in raw)) continue;
    const answer = raw as { selected: unknown; checked: unknown; hintIndex?: unknown };
    if (
      typeof answer.selected === "string" &&
      question.options.some((option) => option.id === answer.selected) &&
      typeof answer.checked === "boolean" &&
      (answer.hintIndex === undefined || (Number.isInteger(answer.hintIndex) && (answer.hintIndex as number) >= 0))
    ) {
      answers[question.storageId] = {
        selected: answer.selected,
        checked: answer.checked,
        hintIndex: Math.min((answer.hintIndex as number | undefined) ?? 0, question.hints.length),
      };
    }
  }
  return answers;
}

function useLocalJsonState<T>(key: string, fallback: T, validate: (value: unknown) => T) {
  const fallbackJson = JSON.stringify(fallback);
  const eventName = `bitsandbytes:local-state:${key}`;
  const subscribe = useCallback((onChange: () => void) => {
    const onStorage = (event: StorageEvent) => {
      if (event.key === key || event.key === null) memoryStore.delete(key);
      onChange();
    };
    const onLocalState = (event: Event) => {
      const localStateEvent = event as CustomEvent<{ source?: string }>;
      if (localStateEvent.detail?.source !== "local-state") memoryStore.delete(key);
      onChange();
    };
    window.addEventListener("storage", onStorage);
    window.addEventListener(eventName, onLocalState);
    return () => {
      window.removeEventListener("storage", onStorage);
      window.removeEventListener(eventName, onLocalState);
    };
  }, [eventName, key]);
  const getSnapshot = useCallback(() => {
    const memoryValue = memoryStore.get(key);
    if (memoryValue !== undefined) return memoryValue;
    try {
      const raw = window.localStorage.getItem(key) ?? fallbackJson;
      return JSON.stringify(validate(JSON.parse(raw))) ?? fallbackJson;
    } catch {
      return memoryStore.get(key) ?? fallbackJson;
    }
  }, [fallbackJson, key, validate]);
  const getServerSnapshot = useCallback(() => fallbackJson, [fallbackJson]);
  const snapshot = useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);
  const value = validate(JSON.parse(snapshot) as unknown);
  const setValue = useCallback((next: T | ((current: T) => T)) => {
    const current = validate(JSON.parse(getSnapshot()) as unknown);
    const updated = typeof next === "function" ? (next as (current: T) => T)(current) : next;
    const serialized = JSON.stringify(validate(updated));
    memoryStore.set(key, serialized);
    try {
      window.localStorage.setItem(key, serialized);
      memoryStore.delete(key);
    } catch {
      // Keep a session-local copy if the browser blocks persistent storage.
    }
    window.dispatchEvent(new CustomEvent(eventName, { detail: { source: "local-state" } }));
  }, [eventName, getSnapshot, key, validate]);
  return [value, setValue] as const;
}

export function BinarySearchLab({
  sourceCode,
  sourcePath,
  sourceCommit,
  traceLines,
}: { sourceCode: string; sourcePath: string; sourceCommit?: string; traceLines: Record<string, number[]> }) {
  const [traceState, setTraceState] = useLocalJsonState(
    TRACE_STORAGE_KEY,
    { scenarioId: scenarios[0].id, frameIndex: 0 },
    validateTraceState,
  );
  const scenarioIndex = Math.max(0, scenarios.findIndex((item) => item.id === traceState.scenarioId));
  const scenario = scenarios[scenarioIndex];
  const frames = scenario.frames;
  const frameIndex = Math.max(0, Math.min(traceState.frameIndex, frames.length - 1));
  const frame = frames[Math.min(frameIndex, frames.length - 1)];

  const changeScenario = (id: string) => {
    const next = scenarios.findIndex((item) => item.id === id);
    if (next < 0) return;
    setTraceState({ scenarioId: scenarios[next].id, frameIndex: 0 });
  };

  return (
    <section className="learning-lab" id="trace-section" aria-labelledby="trace-lab-title">
      <div className="lab-heading">
        <div>
          <p className="eyebrow">Step-by-step trace</p>
          <h2 id="trace-lab-title">Watch the possible range shrink</h2>
        </div>
        <label className="scenario-picker">
          <span>Example</span>
          <select
            value={scenario.id}
            onChange={(event) => changeScenario(event.target.value)}
            aria-label="Choose a binary search example"
          >
            {scenarios.map((item) => (
              <option key={item.id} value={item.id}>{item.label}</option>
            ))}
          </select>
        </label>
      </div>

      <p className="lab-question">
        Find <strong>{scenario.target}</strong> in the sorted list. Before advancing, predict which indexes remain possible.
      </p>

      <dl className="trace-state-table" aria-label="Binary-search state">
        <div><dt>Left index</dt><dd>{frame.left}</dd></div>
        <div><dt>Right index</dt><dd>{frame.right}</dd></div>
        <div><dt>Middle inspected</dt><dd>{frame.inspected === null ? "None yet" : frame.inspected}</dd></div>
        <div><dt>Value</dt><dd>{frame.inspected === null ? "—" : scenario.values[frame.inspected]}</dd></div>
        <div><dt>Remaining range</dt><dd>{frame.left <= frame.right ? `${frame.left} through ${frame.right}` : "Empty"}</dd></div>
      </dl>

      <ol className="search-array" aria-label="List values with their current search status">
        {scenario.values.length ? scenario.values.map((value, index) => {
          const inside = index >= frame.left && index <= frame.right;
          const found = index === frame.middle;
          const inspected = index === frame.inspected && !found;
          const inspectedAndDiscarded = inspected && !inside;
          const status = found ? "checked" : inspected ? "inspected" : inside ? "possible" : "ruled out";
          return (
            <li
              key={`${index}-${value}`}
              className={`search-cell search-cell-${status.replaceAll(" ", "-")}`}
              aria-label={`Index ${index}, value ${value}: ${status}`}
            >
              <span className="search-cell-index">Index {index}</span>
              <span className="search-cell-value">{value}</span>
              <span className="search-cell-state">{status === "checked" ? "Target" : status === "inspected" ? inspectedAndDiscarded ? "Inspected; ruled out" : "Inspected; still possible" : status === "possible" ? "Possible" : "Ruled out"}</span>
            </li>
          );
        }) : (
          <li className="empty-array">Empty list — there are no indexes to search.</li>
        )}
      </ol>

      <p className="trace-announcement" aria-live="polite" aria-atomic="true">
        <span className="trace-step-count">Step {frameIndex + 1} of {frames.length}</span>
        {frame.message}
      </p>

      <div className="trace-controls" aria-label="Trace controls">
        <button type="button" className="button button-secondary" onClick={() => setTraceState((current) => ({ ...current, frameIndex: 0 }))} disabled={frameIndex === 0}>
          Reset
        </button>
        <div className="trace-step-buttons">
          <button type="button" className="button button-secondary" onClick={() => setTraceState((current) => ({ ...current, frameIndex: Math.max(0, frameIndex - 1) }))} disabled={frameIndex === 0}>
            Previous step
          </button>
          <button type="button" className="button button-primary" onClick={() => setTraceState((current) => ({ ...current, frameIndex: Math.min(frames.length - 1, frameIndex + 1) }))} disabled={frameIndex === frames.length - 1}>
            Next step
          </button>
        </div>
      </div>
      <section className="trace-source-panel" id="binary-search-source" aria-labelledby="trace-source-title">
        <div className="trace-source-heading">
          <div>
            <p className="eyebrow">Repository implementation</p>
            <h3 id="trace-source-title">Follow the active lines</h3>
          </div>
        </div>
        <p className="trace-source-help">
          From <code>{sourcePath}</code>{sourceCommit ? <>
            {" "}at build commit <a href={`https://github.com/ishitvagoel/BitsAndBytes/blob/${sourceCommit}/${sourcePath}`} target="_blank" rel="noreferrer"><code>{sourceCommit.slice(0, 8)}</code> <span className="sr-only">(open exact source revision in a new tab)</span></a>
          </> : " in this build"}. Highlighted lines show the operation represented by the current trace message.
        </p>
        <CopyableCodeBlock
          code={sourceCode}
          language="python"
          label="Python source"
          lineNumbers
          activeLines={traceLines[frame.codeStep] ?? []}
        />
      </section>
      <p className="lab-footnote">When local storage is available, the trace saves this example and step in this browser. You can change the example or reset it at any time.</p>
    </section>
  );
}

export function LessonPractice({
  lessonSlug,
  progressConfigs,
}: { lessonSlug: string; progressConfigs: Record<string, LessonProgressConfig> }) {
  const [answers, setAnswers] = useLocalJsonState(practiceStorageKey(lessonSlug), {}, validatePracticeState);
  const questions = useMemo(() => allQuestions.filter((question) => question.lessonSlug === lessonSlug), [lessonSlug]);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const reviewObjective = params.get("reviewObjective");
    if (!reviewObjective || window.location.hash !== "#practice-section") return;
    const reviewQuestions = questions.filter((question) => question.objectiveId === reviewObjective);
    if (!reviewQuestions.length) return;
    setAnswers((current) => {
      const fresh = { ...current };
      for (const question of reviewQuestions) fresh[question.storageId] = { selected: "", checked: false, hintIndex: 0 };
      return fresh;
    });
    params.delete("reviewObjective");
    const query = params.toString();
    window.history.replaceState(window.history.state, "", `${window.location.pathname}${query ? `?${query}` : ""}${window.location.hash}`);
  }, [questions, setAnswers]);

  const selectAnswer = (questionId: string, selected: string) => {
    setAnswers((current) => ({
      ...current,
      [questionId]: { selected, checked: false, hintIndex: current[questionId]?.hintIndex ?? 0 },
    }));
  };

  const showNextHint = (questionId: string) => {
    setAnswers((current) => {
      const previous = current[questionId] ?? { selected: "", checked: false, hintIndex: 0 };
      return { ...current, [questionId]: { ...previous, hintIndex: previous.hintIndex + 1 } };
    });
  };

  const checkAnswer = (questionId: string) => {
    const question = questions.find((item) => item.storageId === questionId);
    if (!question) return;
    const selected = answers[questionId]?.selected;
    setAnswers((current) => ({
      ...current,
      [questionId]: {
        selected: current[questionId]?.selected ?? "",
        checked: true,
        hintIndex: current[questionId]?.hintIndex ?? 0,
      },
    }));
    if (!selected) return;
    try {
      const progress = validateLearningProgress(
        JSON.parse(window.localStorage.getItem(LEARNING_PROGRESS_KEY) ?? "null") as unknown,
        progressConfigs,
      );
      const updated = recordObjectiveAttempt(progress, lessonSlug, progressConfigs[lessonSlug], question.objectiveId, selected === question.answer);
      window.localStorage.setItem(LEARNING_PROGRESS_KEY, JSON.stringify(updated));
      window.dispatchEvent(new Event(LEARNING_PROGRESS_EVENT));
    } catch {
      // The practice feedback still works when browser storage is unavailable.
    }
  };

  return (
    <section className="practice-section" id="practice-section" aria-labelledby="practice-title">
      <p className="eyebrow">Practice with feedback</p>
      <h2 id="practice-title">Check your understanding</h2>
      <p className="practice-intro">Try each checkpoint before revealing the feedback. Ask for a hint when you need one. Answers and hints stay in this browser when local storage is available.</p>
      <div className="practice-grid">
        {questions.map((question, index) => {
          const saved = answers[question.storageId] ?? { selected: "", checked: false, hintIndex: 0 };
          const correct = saved.selected === question.answer;
          return (
            <fieldset className="practice-card" key={question.id}>
              <legend><span className="practice-number">{index + 1}</span>{question.prompt}</legend>
              <div className="practice-options">
                {question.options.map((option) => (
                  <label className="practice-option" key={option.id}>
                    <input
                      type="radio"
                      name={question.id}
                      value={option.id}
                      checked={saved.selected === option.id}
                      onChange={() => selectAnswer(question.storageId, option.id)}
                    />
                    <span>{option.label}</span>
                  </label>
                ))}
              </div>
              {saved.hintIndex < question.hints.length && (
                <div className="practice-hint">
                  <button type="button" className="text-button" onClick={() => showNextHint(question.storageId)}>
                    Show hint {saved.hintIndex + 1}
                  </button>
                  {saved.hintIndex > 0 && <p>{question.hints[saved.hintIndex - 1]}</p>}
                </div>
              )}
              <button type="button" className="button button-secondary check-answer" onClick={() => checkAnswer(question.storageId)} disabled={!saved.selected}>
                Check answer
              </button>
              {saved.checked && (
                <p className={`practice-feedback ${correct ? "feedback-correct" : "feedback-retry"}`} aria-live="polite">
                  <strong>{correct ? "Correct." : "Review this."}</strong> {correct ? question.correct : question.retry}
                </p>
              )}
            </fieldset>
          );
        })}
      </div>
      <p className="local-progress-note">Progress is never sent to an account or synced to another device. If local storage is blocked, choices last only until you leave this page.</p>
    </section>
  );
}
