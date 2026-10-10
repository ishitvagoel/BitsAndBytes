"use client";

import { useCallback, useMemo, useSyncExternalStore } from "react";

export type TraceCellStatus = "idle" | "active" | "done" | "excluded" | "chosen";

export type TraceScenario = {
  id: string;
  title: string;
  prompt: string;
  frames: Array<{
    label: string;
    narration: string;
    state: Array<{ name: string; value: string }>;
    rows: Array<{ label: string; cells: Array<{ text: string; status: TraceCellStatus }> }>;
  }>;
};

const statusClass: Record<TraceCellStatus, string> = {
  idle: "trace-cell-idle",
  active: "trace-cell-active",
  done: "trace-cell-done",
  excluded: "trace-cell-excluded",
  chosen: "trace-cell-chosen",
};

function storageKey(lessonSlug: string) {
  return `bitsandbytes.trace.${lessonSlug}.v1`;
}

export function TraceBench({ lessonSlug, scenarios }: { lessonSlug: string; scenarios: TraceScenario[] }) {
  const key = storageKey(lessonSlug);
  const eventName = `bitsandbytes:local-state:${key}`;
  const fallback = useMemo(() => JSON.stringify({ scenarioId: scenarios[0]?.id ?? "", frameIndex: 0 }), [scenarios]);
  const validate = useCallback((value: unknown) => {
    if (value && typeof value === "object" && "scenarioId" in value && "frameIndex" in value) {
      const candidate = value as { scenarioId: unknown; frameIndex: unknown };
      const scenario = scenarios.find((item) => item.id === candidate.scenarioId) ?? scenarios[0];
      const frameIndex = typeof candidate.frameIndex === "number" && Number.isInteger(candidate.frameIndex)
        ? Math.max(0, Math.min(candidate.frameIndex, Math.max(scenario.frames.length - 1, 0)))
        : 0;
      return { scenarioId: scenario.id, frameIndex };
    }
    return { scenarioId: scenarios[0].id, frameIndex: 0 };
  }, [scenarios]);

  const snapshot = useSyncExternalStore(
    (onChange) => {
      const onStorage = () => onChange();
      window.addEventListener("storage", onStorage);
      window.addEventListener(eventName, onStorage);
      return () => {
        window.removeEventListener("storage", onStorage);
        window.removeEventListener(eventName, onStorage);
      };
    },
    () => {
      try {
        return JSON.stringify(validate(JSON.parse(window.localStorage.getItem(key) ?? fallback)));
      } catch {
        return fallback;
      }
    },
    () => fallback,
  );
  const saved = validate(JSON.parse(snapshot) as unknown);
  const scenario = scenarios.find((item) => item.id === saved.scenarioId) ?? scenarios[0];
  const frame = scenario.frames[saved.frameIndex];

  function write(next: { scenarioId: string; frameIndex: number }) {
    const serialized = JSON.stringify(validate(next));
    try {
      window.localStorage.setItem(key, serialized);
    } catch {
      // The trace still moves for this click when storage is blocked.
    }
    window.dispatchEvent(new Event(eventName));
  }

  return (
    <section className="trace-bench" id="trace-section" aria-labelledby="trace-bench-title">
      <p className="eyebrow">Step-by-step trace</p>
      <h2 id="trace-bench-title">{scenario.title}</h2>
      <p>{scenario.prompt}</p>
      {scenarios.length > 1 && (
        <label className="trace-scenario">
          Example
          <select
            value={scenario.id}
            onChange={(event) => write({ scenarioId: event.target.value, frameIndex: 0 })}
          >
            {scenarios.map((item) => <option key={item.id} value={item.id}>{item.title}</option>)}
          </select>
        </label>
      )}
      <dl className="trace-state">
        {frame.state.map((item) => (
          <div key={item.name}>
            <dt>{item.name}</dt>
            <dd>{item.value}</dd>
          </div>
        ))}
      </dl>
      {frame.rows.map((row) => (
        <div className="trace-row" key={row.label}>
          <p>{row.label}</p>
          <ol className="search-array">
            {row.cells.map((cell, index) => (
              <li className={`search-cell ${statusClass[cell.status]}`} key={`${row.label}-${index}`}>
                <span className="search-cell-index">{index}</span>
                <span className="search-cell-value">{cell.text}</span>
                <span className="search-cell-state">{cell.status}</span>
              </li>
            ))}
          </ol>
        </div>
      ))}
      <p className="trace-narration" role="status">{frame.narration}</p>
      <div className="trace-controls">
        <button type="button" onClick={() => write({ scenarioId: scenario.id, frameIndex: 0 })} disabled={saved.frameIndex === 0}>Reset</button>
        <button type="button" onClick={() => write({ scenarioId: scenario.id, frameIndex: saved.frameIndex - 1 })} disabled={saved.frameIndex === 0}>Previous step</button>
        <button type="button" onClick={() => write({ scenarioId: scenario.id, frameIndex: saved.frameIndex + 1 })} disabled={saved.frameIndex >= scenario.frames.length - 1}>Next step</button>
      </div>
    </section>
  );
}
