import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const siteDir = path.dirname(fileURLToPath(import.meta.url));
const outputDir = path.join(siteDir, "../.next/server/app");
const aliases = JSON.parse(fs.readFileSync(path.join(siteDir, "../src/data/lesson-slug-aliases.json"), "utf8"));
const home = fs.readFileSync(path.join(outputDir, "index.html"), "utf8");
const pilot = fs.readFileSync(path.join(outputDir, "lessons/binary-search.html"), "utf8");
const answerSearch = fs.readFileSync(path.join(outputDir, "lessons/binary-search-on-answer.html"), "utf8");

assert.match(home, /href="\/lessons\/binary-search"[^>]*>Start the lesson/);
assert.match(home, /Check whether the Python examples will feel familiar/);
assert.match(home, /Search the glossary and compare Python tools/);
assert.match(pilot, /id="main-content"/);
assert.match(pilot, /href="\/"[^>]*>← Course home/);
assert.match(pilot, /href="\/lessons\/queues-and-deque"/);
const lessonSequence = /<nav class="lesson-nav" aria-label="Lesson sequence">([\s\S]*?)<\/nav>/.exec(pilot)?.[1] ?? "";
assert.match(lessonSequence, /href="\/lessons\/binary-search-on-answer"/);
assert.doesNotMatch(lessonSequence, /href="\/lessons\/queues-and-deque"/);
assert.match(pilot, /Trace controls/);
assert.match(pilot, /aria-label="Binary-search state"/);
assert.match(pilot, /id="trace-section"/);
assert.match(pilot, /practice-section/);
assert.match(pilot, /Implementation and tests/);

for (const canonicalSlug of Object.values(aliases)) {
  assert.ok(fs.existsSync(path.join(outputDir, "lessons", `${canonicalSlug}.html`)), `Missing static lesson route ${canonicalSlug}`);
}

assert.ok(fs.existsSync(path.join(outputDir, "reference.html")), "Missing glossary/reference route");
const graphLesson = fs.readFileSync(path.join(outputDir, "lessons/graphs.html"), "utf8");
assert.match(graphLesson, /href="\/lessons\/graph-representations"/);
assert.match(graphLesson, /href="https:\/\/github\.com\/ishitvagoel\/BitsAndBytes\/blob\//);
assert.match(answerSearch, /largest pile size is a feasible upper bound/);
assert.match(answerSearch, /O\(p log M\)/);
assert.match(answerSearch, /id="practice-section"/);
console.log(`critical learning journey: home → pilot → next lesson (${Object.keys(aliases).length} lesson routes) ok`);
