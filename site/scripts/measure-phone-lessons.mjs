import { createRequire } from "node:module";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const siteDir = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const curriculum = fs.readFileSync(path.join(siteDir, "src/lib/curriculum.ts"), "utf8");
const stages = curriculum.match(/export const curriculumStages:[\s\S]*?\n\];/)[0];
const slugs = [];
for (const match of stages.matchAll(/id:\s*"([^"]+)"[\s\S]*?slugs:\s*\[([^\]]*)\]/g)) {
  if (match[1] === "reference") continue;
  slugs.push(...[...match[2].matchAll(/"([a-z0-9-]+)"/g)].map((item) => item[1]));
}

const puppeteer = createRequire("/tmp/puppeteer-run/package.json")("puppeteer-core");
const browser = await puppeteer.launch({
  executablePath: "/usr/bin/google-chrome",
  headless: true,
  args: ["--no-sandbox", "--disable-dev-shm-usage"],
});
const page = await browser.newPage();
await page.setViewport({ width: 390, height: 844, deviceScaleFactor: 1 });
const rows = [];
for (const slug of slugs) {
  await page.goto(`http://127.0.0.1:3000/lessons/${slug}`, { waitUntil: "networkidle0" });
  const measured = await page.evaluate(() => {
    const paragraph = document.querySelector(".lesson-body p");
    const overflow = [...document.querySelectorAll("body *")].filter((element) => {
      if (element.closest(".table-scroll")) return false;
      return element.scrollWidth > document.documentElement.clientWidth + 1;
    }).length;
    const targets = [...document.querySelectorAll(".lesson-main-column a, .lesson-main-column button")].map((element) => {
      const box = element.getBoundingClientRect();
      return Math.min(box.width, box.height);
    });
    return {
      height: document.documentElement.scrollHeight,
      top: paragraph ? paragraph.getBoundingClientRect().top : null,
      overflow,
      smallest: targets.length ? Math.min(...targets) : null,
    };
  });
  rows.push({ slug, ...measured });
}
await browser.close();
const bad = rows.filter((row) => row.overflow > 0 || (row.top !== null && row.top > 700) || (row.smallest !== null && row.smallest < 44) || row.height > 5000);
console.log(rows.map((row) => `${row.slug} height=${row.height} top=${row.top} overflow=${row.overflow} tap=${row.smallest}`).join("\n"));
console.log(`phone lessons: ${rows.length} checked, ${bad.length} outside the reading limits`);
if (bad.length) process.exit(1);
