import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const siteDir = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(siteDir, "../..");
const guideDir = path.join(root, "guide");
const curriculum = fs.readFileSync(path.join(siteDir, "../src/lib/curriculum.ts"), "utf8");
const reference = new Set();
const referenceStage = curriculum.match(/id: "reference"[\s\S]*?slugs: \[([^\]]+)\]/);
if (referenceStage) {
  for (const match of referenceStage[1].matchAll(/"([a-z0-9-]+)"/g)) reference.add(match[1]);
}

const entries = [];
for (const fileName of fs.readdirSync(guideDir).filter((name) => name.endsWith(".md")).sort()) {
  const text = fs.readFileSync(path.join(guideDir, fileName), "utf8");
  const parts = text.split("---", 3);
  const front = Object.fromEntries(parts[1].split("\n").flatMap((line) => {
    const index = line.indexOf(":");
    return index < 0 ? [] : [[line.slice(0, index).trim(), line.slice(index + 1).trim()]];
  }));
  const body = parts[2] ?? "";
  const headings = [...body.matchAll(/^#{2,3}\s+(.+)$/gm)].map((match) => match[1].trim().toLowerCase());
  const code = [...body.matchAll(/`([^`\n]+)`/g)].map((match) => match[1].toLowerCase());
  const plain = body.replace(/```[\s\S]*?```/g, " ").replace(/[#>*_\[\]`]/g, " ").replace(/\s+/g, " ").trim().toLowerCase();
  entries.push({
    slug: front.slug,
    title: (front.title ?? front.slug).toLowerCase(),
    headings,
    code,
    body: plain,
    reference: reference.has(front.slug),
  });
}

const output = path.join(siteDir, "../public/search-index.json");
fs.mkdirSync(path.dirname(output), { recursive: true });
fs.writeFileSync(output, JSON.stringify(entries));
console.log(`search index: ${entries.length} lessons, ${fs.statSync(output).size} bytes`);
