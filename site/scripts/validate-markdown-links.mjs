import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { resolveLessonMarkdownHref } from "../src/lib/markdown-links.ts";

const siteDir = path.dirname(fileURLToPath(import.meta.url));
const repositoryRoot = path.resolve(siteDir, "../..");
const guideDir = path.join(repositoryRoot, "guide");
const aliases = JSON.parse(fs.readFileSync(path.join(siteDir, "../src/data/lesson-slug-aliases.json"), "utf8"));
const lessonSlugs = new Set(Object.values(aliases));
const lessonFilesBySlug = new Map();
for (const name of fs.readdirSync(guideDir).filter((item) => item.endsWith(".md"))) {
  const text = fs.readFileSync(path.join(guideDir, name), "utf8");
  const slug = /^slug:\s*(.+)$/m.exec(text)?.[1]?.trim();
  if (slug) lessonFilesBySlug.set(slug, path.join(guideDir, name));
}
const linkPattern = /\]\(([^)\s]+)(?:\s+[^)]*)?\)/g;
const failures = [];
let checked = 0;

for (const name of fs.readdirSync(guideDir).filter((item) => item.endsWith(".md"))) {
  const source = fs.readFileSync(path.join(guideDir, name), "utf8");
  for (const match of source.matchAll(linkPattern)) {
    const target = match[1];
    if (/^(?:https?:|mailto:|#)/i.test(target)) continue;
    checked += 1;
    const [pathname, fragment = ""] = target.split("#", 2);

    if (pathname.endsWith(".md")) {
      const route = resolveLessonMarkdownHref(pathname, lessonSlugs);
      const slug = route?.split("/")[2];
      if (!route) failures.push(`${name}: ${target} does not map to a lesson URL`);
      if (fragment) {
        const targetFile = path.resolve(guideDir, pathname);
        const lessonFile = fs.existsSync(targetFile) ? targetFile : lessonFilesBySlug.get(slug);
        if (lessonFile) {
          const headingIds = new Set(fs.readFileSync(lessonFile, "utf8").split(/\r?\n/)
            .filter((line) => /^#{2,3}\s+/.test(line))
            .map((line) => line.replace(/^#{2,3}\s+/, "").replace(/\s+#+\s*$/, "")
              .toLocaleLowerCase("en").replace(/[`*_~]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "")));
          if (!headingIds.has(decodeURIComponent(fragment))) failures.push(`${name}: ${target} has no matching heading`);
        }
      }
      continue;
    }

    const resolved = path.resolve(guideDir, pathname);
    const relative = path.relative(repositoryRoot, resolved);
    if (relative.startsWith("..") || path.isAbsolute(relative) || !fs.existsSync(resolved)) {
      failures.push(`${name}: ${target} does not resolve to a repository file`);
    }
  }
}

if (failures.length) {
  console.error(`markdown links: ${failures.length} invalid link(s) among ${checked} checked`);
  for (const failure of failures) console.error(`- ${failure}`);
  process.exitCode = 1;
} else {
  console.log(`markdown links: ${checked} local links resolve to lesson routes or repository files`);
}
