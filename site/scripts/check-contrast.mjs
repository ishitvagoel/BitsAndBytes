import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const cssPath = path.join(path.dirname(fileURLToPath(import.meta.url)), "../src/app/globals.css");
const css = fs.readFileSync(cssPath, "utf8");

function luminance(hex) {
  const channels = hex.slice(1).match(/../g).map((pair) => {
    const value = parseInt(pair, 16) / 255;
    return value <= 0.03928 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2];
}

function contrast(foreground, background) {
  const left = luminance(foreground);
  const right = luminance(background);
  const [lighter, darker] = left > right ? [left, right] : [right, left];
  return (lighter + 0.05) / (darker + 0.05);
}

const root = /:root\s*\{([^}]+)\}/.exec(css)?.[1] ?? "";
const tokens = {};
for (const match of root.matchAll(/(--[\w-]+)\s*:\s*(#[0-9a-fA-F]{6})/g)) {
  tokens[match[1]] = match[2].toLowerCase();
}

const paper = tokens["--surface"] ?? tokens["--paper"];
if (!paper) {
  console.error("contrast: missing paper token");
  process.exit(1);
}

const paperSubjects = new Set([
  ".lesson-nav-title",
  ".lesson-nav-label",
  ".lesson-nav-end",
  ".module-list",
  ".module-list h2",
  ".reading-card",
]);

function subject(selector) {
  return selector.split(",").map((part) => part.trim().split(/\s+/).at(-1));
}

const failures = [];
const rulePattern = /([^{}]+)\{([^{}]+)\}/g;
for (const match of css.matchAll(rulePattern)) {
  const color = /(?:^|;)\s*color\s*:\s*([^;]+)/.exec(match[2]);
  if (!color) continue;
  const declared = color[1].trim();
  const resolved = declared.startsWith("var(")
    ? tokens[declared.slice(4, -1).trim()]
    : /^#[0-9a-fA-F]{6}$/.test(declared) ? declared.toLowerCase() : null;
  for (const selector of subject(match[1])) {
    if (!paperSubjects.has(selector) || !resolved) continue;
    const ratio = contrast(resolved, paper);
    if (ratio < 4.5) {
      failures.push(`${selector} uses ${declared} (${resolved}) on ${paper} at ${ratio.toFixed(2)}:1`);
    }
  }
}

const tokenPairs = [
  ["--ink", "--surface"],
  ["--ink-muted", "--paper"],
  ["--link", "--surface"],
  ["--success", "--success-soft"],
  ["--amber-ink", "--amber-soft"],
  ["--amber-ink", "--amber"],
];

for (const [foregroundName, backgroundName] of tokenPairs) {
  const foreground = tokens[foregroundName];
  const background = tokens[backgroundName];
  if (!foreground || !background) {
    failures.push(`missing token ${foregroundName} or ${backgroundName}`);
    continue;
  }
  const ratio = contrast(foreground, background);
  if (ratio < 4.5) {
    failures.push(`${foregroundName} ${foreground} on ${backgroundName} ${background} is ${ratio.toFixed(2)}:1`);
  }
}

if (failures.length > 0) {
  console.error(`contrast: ${failures.length} paper-surface failures`);
  for (const failure of failures) console.error(`  ${failure}`);
  process.exit(1);
}

console.log(`contrast: paper text passes 4.5:1 against ${paper} (${paperSubjects.size} selectors, ${tokenPairs.length} token pairs)`);
