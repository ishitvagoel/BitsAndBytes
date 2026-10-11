import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { curriculumDetails, curriculumObjectiveIds } from "../src/lib/curriculum.ts";

const siteDir = path.dirname(fileURLToPath(import.meta.url));
const repositoryRoot = path.resolve(siteDir, "../..");
const guideDir = path.join(repositoryRoot, "guide");
const references = JSON.parse(fs.readFileSync(path.join(siteDir, "../src/data/lesson-references.json"), "utf8"));
const traces = JSON.parse(fs.readFileSync(path.join(siteDir, "../src/data/binary-search-traces.json"), "utf8"));
const source = JSON.parse(fs.readFileSync(path.join(siteDir, "../src/data/binary-search-source.json"), "utf8"));
const exercises = JSON.parse(fs.readFileSync(path.join(siteDir, "../src/data/exercises.json"), "utf8"));
const lessonTraces = JSON.parse(fs.readFileSync(path.join(siteDir, "../src/data/lesson-traces.json"), "utf8"));

function frontmatter(markdown) {
  const parts = markdown.split("---", 3);
  if (parts.length !== 3 || parts[0] !== "") throw new Error("Lesson is missing closed frontmatter");
  return Object.fromEntries(parts[1].split(/\r?\n/).flatMap((line) => {
    const index = line.indexOf(":");
    return index < 0 ? [] : [[line.slice(0, index).trim(), line.slice(index + 1).trim()]];
  }));
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

try {
  const lessonFiles = fs.readdirSync(guideDir).filter((name) => name.endsWith(".md")).sort();
  const slugs = new Set();
  const orders = new Set();
  let moduleCount = 0;

  for (const fileName of lessonFiles) {
    const markdown = fs.readFileSync(path.join(guideDir, fileName), "utf8");
    const meta = frontmatter(markdown);
    assert(meta.slug && meta.module && meta.order, `${fileName}: missing slug/module/order`);
    assert(!slugs.has(meta.slug), `${fileName}: duplicate slug ${meta.slug}`);
    slugs.add(meta.slug);
    assert(!orders.has(meta.order), `${fileName}: duplicate order ${meta.order}`);
    orders.add(meta.order);

    const reference = references[meta.slug];
    assert(reference, `${fileName}: missing generated source/test references`);
    const modules = meta.module.split(",").map((item) => item.trim());
    assert(reference.modules.length === modules.length, `${fileName}: module reference count differs from frontmatter`);
    for (const [index, module] of modules.entries()) {
      const data = reference.modules[index];
      const expectedSource = `${module.replaceAll(".", "/")}.py`;
      assert(data.module === module && data.sourcePath === expectedSource, `${fileName}: source mapping mismatch for ${module}`);
      const sourcePath = path.join(repositoryRoot, data.sourcePath);
      assert(fs.existsSync(sourcePath), `${fileName}: missing source ${data.sourcePath}`);
      const sourceText = fs.readFileSync(sourcePath, "utf8");
      for (const symbol of data.symbols) {
        assert(new RegExp(`(?:def|class)\\s+${symbol}\\b`).test(sourceText), `${module}: missing declared symbol ${symbol}`);
      }
      for (const [symbol, tests] of Object.entries(data.testsBySymbol)) {
        for (const testName of tests) {
          assert(/^test_[\w-]+\.py$/.test(testName), `${module}: invalid test path ${testName}`);
          const testPath = path.join(repositoryRoot, "tests", testName);
          assert(fs.existsSync(testPath), `${module}: missing test ${testName}`);
          assert(fs.readFileSync(testPath, "utf8").includes(symbol), `${testName}: no import/reference for ${symbol}`);
        }
      }
      for (const testName of data.testPaths) {
        assert(fs.existsSync(path.join(repositoryRoot, "tests", testName)), `${module}: missing listed test ${testName}`);
      }
      moduleCount += 1;
    }
  }

  assert(Object.keys(references).length === slugs.size, "Generated crosswalk has unknown or missing lesson slugs");
  const objectiveBySlug = new Map(Object.entries(curriculumObjectiveIds));
  assert(objectiveBySlug.size === slugs.size && [...slugs].every((slug) => objectiveBySlug.has(slug)), "Objective IDs and lesson slugs differ");
  const objectiveIds = [...objectiveBySlug.values()].flat();
  assert(objectiveIds.every((id) => /^[a-z0-9]+(?:-[a-z0-9]+)+$/.test(id)), "Objective IDs must use stable lowercase hyphenated identifiers");
  assert(new Set(objectiveIds).size === objectiveIds.length, "Duplicate objective IDs across lessons");

  const pilotPath = path.join(guideDir, "06-binary-search.md");
  const pilot = fs.readFileSync(pilotPath, "utf8");
  for (const section of ["By the end of this lesson", "Before you start", "Start with a prediction", "Next step"]) {
    assert(pilot.includes(section), `Binary-search pilot missing required section text: ${section}`);
  }

  const sourceLines = source.code.split("\n").length;
  assert(source.sourcePath === "bitsandbytes/search/binary_search.py", "Unexpected pilot source path");
  assert(source.traceLines && traces.length > 0, "Missing trace/source mappings");
  const implementation = fs.readFileSync(path.join(repositoryRoot, source.sourcePath), "utf8").split(/\r?\n/);
  const startMarker = "# BEGIN LEARNING EXCERPT: binary-search";
  const endMarker = "# END LEARNING EXCERPT: binary-search";
  const start = implementation.indexOf(startMarker);
  const end = implementation.indexOf(endMarker);
  assert(start >= 0 && end > start && implementation.lastIndexOf(startMarker) === start && implementation.lastIndexOf(endMarker) === end, "Invalid or duplicate source excerpt markers");
  const currentCode = [];
  const currentTraceLines = {};
  let currentStep;
  for (const line of implementation.slice(start + 1, end)) {
    const marker = /^\s*#\s*TRACE:([a-z0-9-]+)\s*$/.exec(line);
    if (marker) {
      currentStep = marker[1];
      assert(!currentTraceLines[currentStep], `Duplicate source trace marker ${currentStep}`);
      currentTraceLines[currentStep] = [];
      continue;
    }
    currentCode.push(line);
    if (currentStep && line.trim()) currentTraceLines[currentStep].push(currentCode.length - 1);
  }
  assert(currentCode.join("\n").trim() === source.code, "Generated pilot excerpt is stale; rerun build_binary_search_traces.py");
  assert(JSON.stringify(currentTraceLines) === JSON.stringify(source.traceLines), "Generated trace-line mappings are stale; rerun build_binary_search_traces.py");
  for (const scenario of traces) {
    assert(Array.isArray(scenario.values) && Array.isArray(scenario.frames) && scenario.frames.length > 0, `Invalid trace ${scenario.id}`);
    for (const frame of scenario.frames) {
      assert(Array.isArray(source.traceLines[frame.codeStep]), `${scenario.id}: no source-line map for ${frame.codeStep}`);
      assert(source.traceLines[frame.codeStep].every((line) => line >= 0 && line < sourceLines), `${scenario.id}: source-line map is out of range`);
    }
  }
  assert(Array.isArray(exercises) && exercises.length > 0, "Missing pilot exercise data");
  const exerciseIds = new Set();
  const storageIds = new Set();
  const exercisesByLesson = new Map();
  for (const exercise of exercises) {
    assert(exercise.id && typeof exercise.id === "string" && !exerciseIds.has(exercise.id), `Missing or duplicate exercise ID ${exercise.id}`);
    assert(exercise.storageId && typeof exercise.storageId === "string" && !storageIds.has(exercise.storageId), `${exercise.id}: missing or duplicate storage ID`);
    exerciseIds.add(exercise.id);
    storageIds.add(exercise.storageId);
    assert(slugs.has(exercise.lessonSlug), `${exercise.id}: unknown lesson slug ${exercise.lessonSlug}`);
    const lessonExercises = exercisesByLesson.get(exercise.lessonSlug) ?? [];
    lessonExercises.push(exercise);
    exercisesByLesson.set(exercise.lessonSlug, lessonExercises);
    assert(typeof exercise.prompt === "string" && exercise.prompt.trim(), `${exercise.id}: missing prompt`);
    assert(Array.isArray(exercise.options) && exercise.options.length >= 2, `${exercise.id}: needs at least two options`);
    const optionIds = new Set();
    for (const option of exercise.options) {
      assert(option.id && option.label && !optionIds.has(option.id), `${exercise.id}: missing or duplicate option`);
      optionIds.add(option.id);
    }
    assert(optionIds.has(exercise.answer), `${exercise.id}: answer is not one of its options`);
    assert(typeof exercise.correct === "string" && exercise.correct.trim(), `${exercise.id}: missing correct feedback`);
    assert(typeof exercise.retry === "string" && exercise.retry.trim(), `${exercise.id}: missing retry feedback`);
    assert(["choice", "predict-output", "fill-cell"].includes(exercise.kind), `${exercise.id}: unknown kind ${exercise.kind}`);
    if (exercise.kind === "predict-output") {
      assert(typeof exercise.code === "string" && exercise.code.includes("print"), `${exercise.id}: predict-output needs code`);
    }
    if (exercise.kind === "fill-cell") {
      const scenes = lessonTraces[exercise.lessonSlug] ?? [];
      const frame = scenes.flatMap((scene) => scene.frames).find((item) => item.label === exercise.frameLabel);
      const row = frame?.rows.find((item) => item.label === exercise.rowLabel);
      assert(frame && row && Number.isInteger(exercise.cellIndex) && row.cells[exercise.cellIndex], `${exercise.id}: fill-cell does not match a trace cell`);
    }
  }
  for (const slug of slugs) {
    const detail = curriculumDetails[slug];
    assert(detail, `${slug}: missing exercise IDs in the curriculum manifest`);
    const manifestIds = detail.exerciseIds;
    const dataIds = (exercisesByLesson.get(slug) ?? []).map((exercise) => exercise.id);
    assert(JSON.stringify(dataIds) === JSON.stringify(manifestIds), `${slug}: exercise data and curriculum manifest IDs differ`);
    const manifestObjectiveIds = new Set(curriculumObjectiveIds[slug] ?? []);
    assert(manifestObjectiveIds.size > 0, `${slug}: missing stable objective IDs`);
    assert((exercisesByLesson.get(slug) ?? []).every((exercise) => manifestObjectiveIds.has(exercise.objectiveId)), `${slug}: an exercise references an unknown learning objective`);
  }

  const knownTraceIds = new Set([
    ...traces.map((trace) => trace.id),
    ...Object.values(lessonTraces).flatMap((items) => items.map((trace) => trace.id)),
  ]);
  for (const detail of Object.values(curriculumDetails)) {
    for (const id of detail.traceIds) {
      assert(knownTraceIds.has(id), `unknown trace id ${id}`);
    }
  }

  console.log(`curriculum data: ok (${slugs.size} lessons, ${moduleCount} source modules, ${traces.length} trace scenarios)`);
} catch (error) {
  console.error(`curriculum data: ${error instanceof Error ? error.message : String(error)}`);
  process.exitCode = 1;
}
