import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

if (process.env.VERCEL === "1") {
  console.log("Vercel's Next.js builder packages server output before post-build scripts run; local static-artifact checks are skipped here.");
  console.log("Run `npm run build` outside Vercel to validate rendered links, the critical journey and the local asset budget.");
  process.exit(0);
}

const siteDir = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const checks = [
  "test-rendered-links.mjs",
  "test-critical-learning-journey.mjs",
  "measure-static-performance.mjs",
];

for (const check of checks) {
  const result = spawnSync(process.execPath, [path.join(siteDir, "scripts", check)], {
    cwd: siteDir,
    stdio: "inherit",
  });
  if (result.error) throw result.error;
  if (result.status !== 0) process.exit(result.status ?? 1);
}
