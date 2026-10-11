"use client";

import Link from "next/link";
import { useMemo, useState } from "react";

export type ReferenceRow = {
  name: string;
  purpose: string;
  behavior: string;
  sourceLabel: string;
  sourceUrl: string;
  lessonSlug: string;
  lessonTitle: string;
};

export type GlossaryTerm = {
  term: string;
  definition: string;
  lessonSlug: string;
  lessonTitle: string;
};

export type CostRow = {
  module: string;
  name: string;
  time: string;
  memory: string;
  lessonSlug: string;
  lessonTitle: string;
};

export function ReferenceSearch({
  comparisons,
  terms,
  costs,
}: {
  comparisons: ReferenceRow[];
  terms: GlossaryTerm[];
  costs: CostRow[];
}) {
  const [query, setQuery] = useState("");
  const normalized = query.trim().toLocaleLowerCase("en");
  const filteredComparisons = useMemo(() => comparisons.filter((item) =>
    `${item.name} ${item.purpose} ${item.behavior} ${item.lessonTitle}`.toLocaleLowerCase("en").includes(normalized)
  ), [comparisons, normalized]);
  const filteredTerms = useMemo(() => terms.filter((item) =>
    `${item.term} ${item.definition} ${item.lessonTitle}`.toLocaleLowerCase("en").includes(normalized)
  ), [normalized, terms]);
  const filteredCosts = useMemo(() => costs.filter((item) =>
    `${item.module} ${item.name} ${item.time} ${item.memory} ${item.lessonTitle}`.toLocaleLowerCase("en").includes(normalized)
  ), [costs, normalized]);

  return (
    <>
      <div className="reference-search">
        <label htmlFor="reference-query">Search concepts and Python libraries</label>
        <div className="curriculum-search-control">
          <input id="reference-query" type="search" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Try “queue”, “lower bound” or “heap”" />
          {query && <button type="button" className="curriculum-clear" onClick={() => setQuery("")}>Clear</button>}
        </div>
        <p className="curriculum-result-count" role="status" aria-live="polite">
          {filteredComparisons.length + filteredTerms.length + filteredCosts.length} reference entries
        </p>
      </div>

      {filteredComparisons.length > 0 && (
        <section className="reference-section" aria-labelledby="comparison-title">
          <h2 id="comparison-title">Python library comparison</h2>
          <div className="reference-table-wrap">
            <table>
              <thead><tr><th scope="col">Tool</th><th scope="col">Useful for</th><th scope="col">Behavior and tradeoff</th><th scope="col">Learn more</th></tr></thead>
              <tbody>{filteredComparisons.map((item) => (
                <tr key={item.name}>
                  <th scope="row"><a href={item.sourceUrl} target="_blank" rel="noreferrer"><code>{item.name}</code><span className="reference-source">{item.sourceLabel}</span><span className="sr-only"> (official docs, new tab)</span></a></th>
                  <td>{item.purpose}</td>
                  <td>{item.behavior}</td>
                  <td><Link href={`/lessons/${item.lessonSlug}`}>{item.lessonTitle}</Link></td>
                </tr>
              ))}</tbody>
            </table>
          </div>
        </section>
      )}

      {filteredTerms.length > 0 && (
        <section className="reference-section" aria-labelledby="glossary-title">
          <h2 id="glossary-title">Glossary</h2>
          <dl className="glossary-list">
            {filteredTerms.map((item) => (
              <div key={item.term}>
                <dt>{item.term}</dt>
                <dd>{item.definition} <Link href={`/lessons/${item.lessonSlug}`}>In {item.lessonTitle}</Link></dd>
              </div>
            ))}
          </dl>
        </section>
      )}

      <section className="reference-section" aria-labelledby="cost-title">
        <h2 id="cost-title">Library costs</h2>
        <p id="cost-row-count">{costs.length} cost rows</p>
        {filteredCosts.length > 0 ? (
          <div className="reference-table-wrap">
            <table>
              <thead>
                <tr>
                  <th scope="col">Function</th>
                  <th scope="col">Time</th>
                  <th scope="col">Memory</th>
                  <th scope="col">Lesson</th>
                </tr>
              </thead>
              <tbody>
                {filteredCosts.map((item) => (
                  <tr key={`${item.module}.${item.name}`}>
                    <th scope="row"><code>{item.name}</code></th>
                    <td>{item.time}</td>
                    <td>{item.memory}</td>
                    <td><Link href={`/lessons/${item.lessonSlug}`}>{item.lessonTitle}</Link></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : filteredComparisons.length + filteredTerms.length > 0 ? (
          <p className="curriculum-empty">No cost rows match this search.</p>
        ) : null}
      </section>

      {filteredComparisons.length === 0 && filteredTerms.length === 0 && filteredCosts.length === 0 && (
        <p className="curriculum-empty">No reference entries match “{query.trim()}”. Try another term or clear the search.</p>
      )}
    </>
  );
}
