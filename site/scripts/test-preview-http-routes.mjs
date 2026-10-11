import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const siteDir = path.dirname(fileURLToPath(import.meta.url));
const baseUrl = process.argv[2] ?? process.env.PREVIEW_URL;
if (!baseUrl) throw new Error("Pass a reachable preview base URL or set PREVIEW_URL.");

const guideDir = path.resolve(siteDir, "../../guide");
const lessonSlugs = fs.readdirSync(guideDir).flatMap((name) => {
  if (!name.endsWith(".md")) return [];
  const slug = /^slug:\s*(.+)$/m.exec(fs.readFileSync(path.join(guideDir, name), "utf8"))?.[1]?.trim();
  return slug ? [slug] : [];
});
const routes = ["/", "/readiness", "/python-foundations", "/reference", ...lessonSlugs.map((slug) => `/lessons/${slug}`)];
const failures = [];

for (const route of routes) {
  let response;
  try {
    response = await fetch(new URL(route, baseUrl));
  } catch (error) {
    failures.push(`${route}: ${error instanceof Error ? error.message : String(error)}`);
    continue;
  }
  const html = await response.text();
  if (response.status !== 200) failures.push(`${route}: HTTP ${response.status}`);
  else if (!html.includes("<main") || !html.includes("<title>")) failures.push(`${route}: missing main content or document title`);
}

if (failures.length) {
  console.error(`preview route smoke test failed (${failures.length}/${routes.length})`);
  for (const failure of failures) console.error(`- ${failure}`);
  process.exitCode = 1;
} else {
  console.log(`preview route smoke test: ${routes.length}/${routes.length} routes return a titled page with main content`);
}
