"use client";

import { useState, type ReactNode } from "react";

function highlightPythonLine(line: string): ReactNode[] {
  const tokenPattern = /(#[^\n]*|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|\b\d+(?:\.\d+)?\b|\b(?:def|return|while|if|elif|else|in|not|and|or|is|for|class|True|False|None|import|from|as|with|raise|try|except|finally|pass|yield|lambda|assert)\b)/g;
  const nodes: ReactNode[] = [];
  let previousIndex = 0;
  let match: RegExpExecArray | null;
  while ((match = tokenPattern.exec(line)) !== null) {
    if (match.index > previousIndex) nodes.push(line.slice(previousIndex, match.index));
    const token = match[0];
    const tokenClass = token.startsWith("#")
      ? "python-token-comment"
      : /^['"]/.test(token)
        ? "python-token-string"
        : /^\d/.test(token)
          ? "python-token-number"
          : "python-token-keyword";
    nodes.push(<span className={tokenClass} key={`${match.index}-${token}`}>{token}</span>);
    previousIndex = tokenPattern.lastIndex;
  }
  if (previousIndex < line.length) nodes.push(line.slice(previousIndex));
  return nodes.length ? nodes : [" "];
}

export function CopyableCodeBlock({
  code,
  language,
  activeLines = [],
  lineNumbers = false,
  label,
}: {
  code: string;
  language?: string;
  activeLines?: number[];
  lineNumbers?: boolean;
  label?: string;
}) {
  const [status, setStatus] = useState("");
  const highlighted = new Set(activeLines);

  async function copyCode() {
    try {
      await navigator.clipboard.writeText(code);
      setStatus("Code copied.");
    } catch {
      setStatus("Copy is unavailable here. Select the code to copy it manually.");
    }
  }

  const lines = code.split("\n");
  return (
    <div className={`code-block-wrapper${lineNumbers ? " code-block-with-lines" : ""}`}>
      <div className="code-block-toolbar">
        <span>{label ?? language ?? "Code"}</span>
        <button type="button" className="code-copy-button" onClick={copyCode}>Copy<span className="sr-only"> {label ?? language ?? "code"}</span></button>
      </div>
      <pre><code className={language ? `language-${language}` : undefined}>{lines.map((line, index) => (
        <span className={`code-line${highlighted.has(index) ? " code-line-active" : ""}`} key={index} aria-current={highlighted.has(index) ? "true" : undefined}>
          {lineNumbers && <span className="code-line-number" aria-hidden="true">{index + 1}</span>}
          <span>{language === "python" ? highlightPythonLine(line) : line || " "}</span>
        </span>
      ))}</code></pre>
      <p className="code-copy-status" role="status" aria-live="polite">{status}</p>
    </div>
  );
}
