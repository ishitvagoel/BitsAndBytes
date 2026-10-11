import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";

const routes = [
  "/",
  "/lessons/input-size-and-operation-counts",
  "/lessons/cost-models",
  "/lessons/binary-search",
  "/lessons/merge-sort",
  "/reference",
  "/readiness",
  "/python-foundations",
  "/lessons/does-not-exist",
  "/lessons/stacks",
];
const viewports = [
  { width: 1440, height: 900 },
  { width: 390, height: 844 },
];
const baseUrl = process.env.AUDIT_BASE_URL ?? "http://127.0.0.1:3000";
const chromePath = process.env.CHROME_PATH ?? "/usr/bin/google-chrome";

function loadPuppeteer() {
  const roots = [
    path.dirname(fileURLToPath(import.meta.url)),
    "/tmp/puppeteer-run",
  ];
  for (const root of roots) {
    try {
      return createRequire(path.join(root, "package.json"))("puppeteer-core");
    } catch {
      // Try the next location that may have puppeteer-core installed.
    }
  }
  return null;
}

const puppeteer = loadPuppeteer();
if (!puppeteer) {
  console.error("rendered contrast: puppeteer-core is not installed, so the audit did not run");
  process.exit(1);
}

const browser = await puppeteer.launch({
  executablePath: chromePath,
  headless: true,
  args: ["--no-sandbox", "--disable-dev-shm-usage"],
});
const page = await browser.newPage();
let lowContrast = 0;
let smallControls = 0;

for (const viewport of viewports) {
  await page.setViewport(viewport);
  for (const route of routes) {
    const response = await page.goto(new URL(route, baseUrl).toString(), { waitUntil: "networkidle0" });
    const status = response?.status() ?? 0;
    if (route !== "/lessons/does-not-exist" && status >= 400) {
      console.error(`${route} returned ${status}`);
      lowContrast += 1;
    }
    const report = await page.evaluate(() => {
      function channel(value) {
        const scaled = value <= 0.03928 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
        return scaled;
      }
      function parseColor(text) {
        const match = text.match(/rgba?\(([^)]+)\)/);
        if (!match) return null;
        const parts = match[1].split(",").map((part) => Number.parseFloat(part.trim()));
        return { r: parts[0], g: parts[1], b: parts[2], a: parts[3] ?? 1 };
      }
      function luminance(color) {
        const values = [color.r, color.g, color.b].map((item) => channel(item / 255));
        return 0.2126 * values[0] + 0.7152 * values[1] + 0.0722 * values[2];
      }
      function mix(front, back) {
        const alpha = front.a;
        return {
          r: front.r * alpha + back.r * (1 - alpha),
          g: front.g * alpha + back.g * (1 - alpha),
          b: front.b * alpha + back.b * (1 - alpha),
          a: 1,
        };
      }
      function backgroundOf(element) {
        const layers = [];
        let current = element;
        while (current) {
          const parsed = parseColor(getComputedStyle(current).backgroundColor);
          if (parsed && parsed.a > 0) layers.push(parsed);
          if (parsed && parsed.a === 1) break;
          current = current.parentElement;
        }
        const html = parseColor(getComputedStyle(document.documentElement).backgroundColor);
        const body = parseColor(getComputedStyle(document.body).backgroundColor);
        const base = (body && body.a === 1 ? body : null) ?? (html && html.a === 1 ? html : null) ?? { r: 16, g: 19, b: 24, a: 1 };
        return layers.reduceRight((back, front) => mix(front, back), base);
      }
      function ratio(front, back) {
        const left = luminance(front);
        const right = luminance(back);
        const lighter = Math.max(left, right);
        const darker = Math.min(left, right);
        return (lighter + 0.05) / (darker + 0.05);
      }
      const failures = [];
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      let node = walker.nextNode();
      while (node) {
        const text = node.textContent?.replace(/\s+/g, " ").trim();
        const parent = node.parentElement;
        if (text && parent) {
          const style = getComputedStyle(parent);
          const rect = parent.getBoundingClientRect();
          const visible = style.visibility !== "hidden" && style.display !== "none" && Number(style.opacity) > 0 && rect.width > 0 && rect.height > 0;
          if (visible) {
            const front = parseColor(style.color);
            const back = backgroundOf(parent);
            if (front && back) {
              const size = Number.parseFloat(style.fontSize);
              const bold = Number.parseInt(style.fontWeight, 10) >= 700;
              const large = size >= 24 || (bold && size >= 18.67);
              const score = ratio(front, back);
              if (score < (large ? 3 : 4.5)) failures.push(text.slice(0, 40));
            }
          }
        }
        node = walker.nextNode();
      }
      let small = 0;
      for (const control of document.querySelectorAll("a, button, input, select, textarea, summary")) {
        const rect = control.getBoundingClientRect();
        const style = getComputedStyle(control);
        if (style.display === "none" || rect.width === 0 || rect.height === 0) continue;
        if (rect.width < 44 && rect.height < 44) small += 1;
      }
      return { failures, small };
    });
    lowContrast += report.failures.length;
    smallControls += report.small;
    if (report.failures.length || report.small) {
      console.log(`${viewport.width}x${viewport.height} ${route}: ${report.failures.length} low-contrast, ${report.small} controls under 44px`);
      for (const sample of report.failures.slice(0, 8)) console.log(`  ${sample}`);
    }
  }
}

await browser.close();
console.log(`rendered contrast: ${lowContrast} low-contrast nodes, ${smallControls} controls under 44px`);
if (lowContrast > 0) process.exit(1);
