import fs from "node:fs";
import path from "node:path";
import { curriculumDetails, curriculumStages } from "../src/lib/curriculum.ts";

const siteDir = process.cwd();
const guideDir = path.join(siteDir, "..", "guide");
const outputPath = path.join(siteDir, "..", "docs", "lesson-readiness-audit.md");

function readTitle(slug) {
  const files = fs.readdirSync(guideDir);
  const file = files.find((name) => name.endsWith(".md") && new RegExp(`^---\\ntitle:.*\\nslug: ${slug}\\n`, "m").test(fs.readFileSync(path.join(guideDir, name), "utf8")));
  if (!file) throw new Error(`No guide file found for ${slug}`);
  const text = fs.readFileSync(path.join(guideDir, file), "utf8");
  return { title: /^title: (.+)$/m.exec(text)?.[1] ?? slug, file };
}

function nextAction(readiness) {
  switch (readiness) {
    case "ready":
      return "Keep the readiness claim current; run browser and learner acceptance checks before release.";
    case "partial":
      return "Finish the missing readiness-rubric elements; recheck outcome, exercise and objective alignment.";
    case "reference":
      return "Confirm reference scope, source freshness, accessibility and links; keep outside the course sequence.";
    default:
      return "Expand to the readiness rubric: motivating example, worked reasoning, source-linked code, cost derivation, progressive practice, primary references and recall.";
  }
}

const rows = [];
for (const stage of curriculumStages) {
  for (const slug of stage.slugs) {
    const detail = curriculumDetails[slug];
    if (!detail) throw new Error(`Missing curriculum details for ${slug}`);
    rows.push({ stage: stage.title, slug, ...readTitle(slug), ...detail });
  }
}

const counts = Object.groupBy(rows, (row) => row.contentReadiness);
const lines = [
  "# Lesson readiness audit",
  "",
  "Generated from `site/src/lib/curriculum.ts` and guide front matter. This is a per-topic work queue, not a claim that the rubric has been independently checked. Update readiness only after reviewing the lesson against the rubric in `../BitsAndBytes_Redesign_Checklist.md`.",
  "",
  `**Snapshot:** ${rows.length} lesson routes; ${counts.ready?.length ?? 0} Ready, ${counts.partial?.length ?? 0} Partially taught, ${counts.summary?.length ?? 0} Summary, ${counts.reference?.length ?? 0} Reference.`,
  "",
  "| Stage | Lesson | Readiness | Objectives | Practice | Next action |",
  "|---|---|---|---:|---:|---|",
];

for (const row of rows) {
  lines.push(`| ${row.stage} | [${row.title}](../guide/${row.file}) | ${row.contentReadiness} | ${row.outcomes.length} | ${row.exerciseIds.length} | ${nextAction(row.contentReadiness)} |`);
}

lines.push(
  "",
  "## Review notes",
  "",
  "- Review each row against the lesson content; readiness metadata and route existence alone are not evidence of teaching quality.",
  "- The pilot and follow-on still need browser and learner evidence even where their content is more developed.",
  "- For each reviewed lesson, replace the generic next action with the specific missing rubric items and evidence. Keep unreviewed lessons at their current readiness.",
  "",
);

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, lines.join("\n"));
console.log(`lesson readiness audit: ${rows.length} lessons (${Object.entries(counts).map(([state, lessons]) => `${lessons.length} ${state}`).join(", ")}) written to ${path.relative(siteDir, outputPath)}`);
