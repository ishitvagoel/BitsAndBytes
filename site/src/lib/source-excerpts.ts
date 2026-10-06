import fs from "node:fs";
import path from "node:path";

export type SourceExcerpt = {
  id: string;
  sourcePath: string;
  code: string;
  traceLines: Record<string, number[]>;
  commit?: string;
};

const excerptSources: Record<string, { sourcePath: string; start: string; end: string }> = {
  "binary-search": {
    sourcePath: "bitsandbytes/search/binary_search.py",
    start: "# BEGIN LEARNING EXCERPT: binary-search",
    end: "# END LEARNING EXCERPT: binary-search",
  },
};

export function getSourceExcerpt(id: string): SourceExcerpt {
  const definition = excerptSources[id];
  if (!definition) throw new Error(`Unknown source excerpt: ${id}`);

  const repositoryRoot = path.join(process.cwd(), "..");
  const sourcePath = path.join(repositoryRoot, definition.sourcePath);
  const lines = fs.readFileSync(sourcePath, "utf-8").split(/\r?\n/);
  const startIndexes = lines.flatMap((line, index) => line.trim() === definition.start ? [index] : []);
  const endIndexes = lines.flatMap((line, index) => line.trim() === definition.end ? [index] : []);
  if (startIndexes.length !== 1 || endIndexes.length !== 1 || endIndexes[0] <= startIndexes[0]) {
    throw new Error(`Source excerpt markers for ${id} must appear exactly once and in order`);
  }

  const codeLines: string[] = [];
  const traceLines: Record<string, number[]> = {};
  let currentTraceStep: string | undefined;
  for (const line of lines.slice(startIndexes[0] + 1, endIndexes[0])) {
    const marker = /^\s*#\s*TRACE:([a-z0-9-]+)\s*$/.exec(line);
    if (marker) {
      currentTraceStep = marker[1];
      traceLines[currentTraceStep] = [];
      continue;
    }
    codeLines.push(line);
    if (currentTraceStep && line.trim()) traceLines[currentTraceStep].push(codeLines.length - 1);
  }
  const code = codeLines.join("\n").trim();
  if (!code) throw new Error(`Source excerpt ${id} is empty`);
  for (const step of ["initialize", "compare-left", "narrow-left", "compare-right", "narrow-right", "return-match", "return-absent"]) {
    if (!traceLines[step]?.length) throw new Error(`Source excerpt ${id} is missing trace lines for ${step}`);
  }
  return {
    id,
    sourcePath: definition.sourcePath,
    code,
    traceLines,
    ...(process.env.VERCEL_GIT_COMMIT_SHA ? { commit: process.env.VERCEL_GIT_COMMIT_SHA } : {}),
  };
}
