import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const siteDir = path.dirname(fileURLToPath(import.meta.url));
const outputDir = path.join(siteDir, "../.next/server/app");
const htmlFiles = fs.readdirSync(outputDir, { recursive: true })
  .filter((name) => typeof name === "string" && name.endsWith(".html"));
const routes = new Map();
for (const name of htmlFiles) {
  const route = name === "index.html" ? "/" : `/${name.replace(/\.html$/, "")}`;
  routes.set(route, fs.readFileSync(path.join(outputDir, name), "utf8"));
}

function idsIn(html) {
  return new Set([...html.matchAll(/\bid="([^"]+)"/g)].map((match) => match[1]));
}

const idsByRoute = new Map([...routes].map(([route, html]) => [route, idsIn(html)]));
const failures = [];
let checked = 0;
for (const [route, html] of routes) {
  for (const match of html.matchAll(/<a\b[^>]*\bhref="([^"]+)"[^>]*>/g)) {
    const href = match[1].replaceAll("&amp;", "&");
    if (/^(?:https?:|mailto:|tel:|javascript:|data:)/i.test(href)) continue;
    const target = new URL(href, `https://bitsandbytes.invalid${route}`);
    const targetRoute = decodeURIComponent(target.pathname).replace(/\/$/, "") || "/";
    checked += 1;
    if (!routes.has(targetRoute)) {
      failures.push(`${route}: ${href} points to missing route ${targetRoute}`);
      continue;
    }
    if (target.hash && !idsByRoute.get(targetRoute)?.has(decodeURIComponent(target.hash.slice(1)))) {
      failures.push(`${route}: ${href} points to missing anchor ${target.hash} on ${targetRoute}`);
    }
  }
}

assert.deepEqual(failures, [], failures.slice(0, 25).join("\n"));
console.log(`rendered links: ${checked} internal links and fragments resolve across ${routes.size} generated pages`);
