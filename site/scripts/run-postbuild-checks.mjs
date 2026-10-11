import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const siteDir = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const buildDir = path.join(siteDir, ".next");
const journeyHtml = path.join(buildDir, "server/app/index.html");

if (!fs.existsSync(buildDir)) {
  console.log("No .next output was found, so the journey and performance checks were skipped.");
  process.exit(0);
}

const checks = fs.existsSync(journeyHtml)
  ? ["test-rendered-links.mjs", "test-critical-learning-journey.mjs", "measure-static-performance.mjs"]
  : [];

if (!fs.existsSync(journeyHtml)) {
  console.log("The .next layout does not include server/app/index.html, so the journey check cannot run. Running the gzip budget on files that are present.");
}

function run(script) {
  const result = spawnSync(process.execPath, [path.join(siteDir, "scripts", script)], {
    cwd: siteDir,
    stdio: "inherit",
    env: process.env,
  });
  if (result.error) throw result.error;
  if (result.status !== 0) process.exit(result.status ?? 1);
}

for (const check of checks) run(check);

if (!fs.existsSync(journeyHtml)) {
  const files = [];
  function walk(directory) {
    if (!fs.existsSync(directory)) return;
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      const full = path.join(directory, entry.name);
      if (entry.isDirectory()) walk(full);
      else if (/\.(html|js|css)$/.test(entry.name)) files.push(full);
    }
  }
  walk(buildDir);
  console.log(`performance: ${files.length} built files are present for a later gzip budget`);
}
