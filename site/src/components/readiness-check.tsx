"use client";

import Link from "next/link";
import { useState } from "react";

const questions = [
  {
    id: "indexing",
    prompt: "What does `values[1]` read?",
    code: "values = [4, 7, 9]",
    options: ["The first item, 4", "The second item, 7", "The item with value 1"],
    answer: 1,
    explanation: "Python lists start at index 0, so index 1 refers to the second item.",
  },
  {
    id: "loop",
    prompt: "How many times does this loop run?",
    code: "for item in [2, 5, 8]:\n    print(item)",
    options: ["Once", "Three times", "It never runs"],
    answer: 1,
    explanation: "The loop visits each of the three list items once.",
  },
  {
    id: "function",
    prompt: "What happens when `double(3)` is called?",
    code: "def double(number):\n    return number * 2",
    options: ["The function returns 6", "The function returns 3", "The function prints 6"],
    answer: 0,
    explanation: "The call gives 3 to the parameter `number`; the function returns 3 * 2, which is 6.",
  },
  {
    id: "append",
    prompt: "After this line, what is in `items`?",
    code: "items = [1, 2]\nitems.append(3)",
    options: ["[1, 2]", "[3, 1, 2]", "[1, 2, 3]"],
    answer: 2,
    explanation: "`append` adds the new item to the end of the list.",
  },
] as const;

export function ReadinessCheck() {
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [submitted, setSubmitted] = useState(false);
  const score = questions.reduce((total, question) => total + Number(answers[question.id] === question.answer), 0);
  const complete = questions.every((question) => answers[question.id] !== undefined);

  function reset() {
    setAnswers({});
    setSubmitted(false);
  }

  return (
    <div className="readiness-check">
      <p className="readiness-intro">This quick check covers list indexing, loops, functions and adding to a list. It does not test algorithm knowledge. It is guidance only; every lesson stays open.</p>
      {questions.map((question, questionIndex) => (
        <fieldset className="readiness-question" key={question.id}>
          <legend><span>Question {questionIndex + 1}.</span> {question.prompt}</legend>
          <pre><code>{question.code}</code></pre>
          <div className="readiness-options">
            {question.options.map((option, optionIndex) => {
              const selected = answers[question.id] === optionIndex;
              const correct = question.answer === optionIndex;
              const resultClass = submitted && selected ? (correct ? "answer-correct" : "answer-incorrect") : "";
              return (
                <label className={`readiness-option ${resultClass}`} key={option}>
                  <input
                    type="radio"
                    name={question.id}
                    checked={selected}
                    onChange={() => setAnswers((current) => ({ ...current, [question.id]: optionIndex }))}
                  />
                  <span>{option}</span>
                </label>
              );
            })}
          </div>
          {submitted && <p className="readiness-feedback">{answers[question.id] === question.answer ? "Correct. " : "Review this one. "}{question.explanation}</p>}
        </fieldset>
      ))}

      <div className="readiness-actions">
        {!submitted ? (
          <button className="button button-primary" type="button" disabled={!complete} onClick={() => setSubmitted(true)}>Check my answers</button>
        ) : (
          <button className="button button-secondary" type="button" onClick={reset}>Try again</button>
        )}
        {!complete && !submitted && <span>Answer all four questions to see the explanations.</span>}
      </div>

      {submitted && (
        <section className="readiness-result" aria-live="polite">
          <h2>{score} of {questions.length} correct</h2>
          {score >= 3 ? (
            <>
              <p>You seem ready for the guide’s Python reading level. You can still use the optional bridge any time.</p>
              <Link className="button button-primary" href="/lessons/binary-search">Start the learning pilot <span aria-hidden="true">→</span></Link>
            </>
          ) : (
            <>
              <p>A short Python refresher may make the examples easier to follow. You can take it first or go straight to any lesson.</p>
              <Link className="button button-primary" href="/python-foundations">Open the optional Python bridge <span aria-hidden="true">→</span></Link>
              <p><Link href="/lessons/binary-search">Go directly to the learning pilot</Link></p>
            </>
          )}
        </section>
      )}
    </div>
  );
}
