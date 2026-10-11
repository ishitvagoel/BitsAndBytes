"use client";

import { useCallback, useSyncExternalStore } from "react";

const memoryStore = new Map<string, string>();

export function useLocalJsonState<T>(key: string, fallback: T, validate: (value: unknown) => T) {
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
      // A blocked write keeps the in-memory value for this tab.
    }
    window.dispatchEvent(new CustomEvent(eventName, { detail: { source: "local-state" } }));
  }, [eventName, getSnapshot, key, validate]);
  return [value, setValue] as const;
}
