import fs from "node:fs";
import path from "node:path";
import { gzipSync } from "node:zlib";

const siteDir = process.cwd();
const buildDir = path.join(siteDir, ".next");
const route = "/lessons/binary-search";
const htmlPath = path.join(buildDir, "server/app/lessons/binary-search.html");

if (!fs.existsSync(htmlPath)) {
  throw new Error(`Missing production output for ${route}; run npm run build first.`);
}

const html = fs.readFileSync(htmlPath);
const source = html.toString("utf8");
const assetUrls = new Set([
  ...[...source.matchAll(/src="([^"]+\.js(?:\?[^"]*)?)"/g)].map((match) => match[1]),
  ...[...source.matchAll(/href="([^"]+\.css(?:\?[^"]*)?)"/g)].map((match) => match[1]),
]);

function measure(bytes) {
  return { raw: bytes.length, gzip: gzipSync(bytes, { level: 9 }).length };
}

const assets = [...assetUrls].map((url) => {
  const relative = url.replace(/^\/_next\//, "").split("?", 1)[0];
  const filePath = path.join(buildDir, relative);
  if (!fs.existsSync(filePath)) throw new Error(`Missing route asset ${url}`);
  const measured = measure(fs.readFileSync(filePath));
  return { url, type: url.endsWith(".css") ? "css" : "js", ...measured };
});

const htmlSize = measure(html);
const js = assets.filter((asset) => asset.type === "js");
const css = assets.filter((asset) => asset.type === "css");
const sum = (items, key) => items.reduce((total, item) => total + item[key], 0);
const budgets = { html: 40 * 1024, javascript: 200 * 1024, stylesheets: 10 * 1024, initialTransfer: 256 * 1024 };
const result = {
  route,
  html: htmlSize,
  javascript: { assets: js.length, raw: sum(js, "raw"), gzip: sum(js, "gzip") },
  stylesheets: { assets: css.length, raw: sum(css, "raw"), gzip: sum(css, "gzip") },
  totalInitialTransferEstimateGzip: htmlSize.gzip + sum(js, "gzip") + sum(css, "gzip"),
  budgetsGzip: budgets,
  compression: "gzip level 9 applied to unique local HTML and referenced JS/CSS build files",
  assets,
};

if (result.html.gzip > budgets.html
  || result.javascript.gzip > budgets.javascript
  || result.stylesheets.gzip > budgets.stylesheets
  || result.totalInitialTransferEstimateGzip > budgets.initialTransfer) {
  throw new Error("The binary-search production route exceeded a documented gzip budget.");
}

console.log(JSON.stringify(result, null, 2));
