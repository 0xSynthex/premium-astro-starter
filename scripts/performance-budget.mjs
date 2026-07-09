#!/usr/bin/env node
import { chromium } from '@playwright/test';
import { statSync, readdirSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, extname } from 'node:path';

const url = process.argv[2] || 'http://127.0.0.1:4321/';
const budgets = {
  totalKb: Number(process.env.PERF_TOTAL_KB || 450),
  jsKb: Number(process.env.PERF_JS_KB || 120),
  cssKb: Number(process.env.PERF_CSS_KB || 120),
  imageKb: Number(process.env.PERF_IMAGE_KB || 250),
  requestCount: Number(process.env.PERF_REQUESTS || 25),
  domContentLoadedMs: Number(process.env.PERF_DCL_MS || 1500),
};

function walk(dir) {
  const out = [];
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walk(p));
    else out.push(p);
  }
  return out;
}

function distSizes() {
  const root = 'dist';
  const sizes = { total: 0, js: 0, css: 0, image: 0, files: [] };
  try {
    for (const file of walk(root)) {
      const bytes = statSync(file).size;
      const ext = extname(file).toLowerCase();
      sizes.total += bytes;
      if (ext === '.js') sizes.js += bytes;
      if (ext === '.css') sizes.css += bytes;
      if (['.png', '.jpg', '.jpeg', '.webp', '.avif', '.gif', '.svg'].includes(ext)) sizes.image += bytes;
      sizes.files.push({ file, bytes });
    }
  } catch {
    throw new Error('dist/ not found. Run npm run build first.');
  }
  sizes.files.sort((a, b) => b.bytes - a.bytes);
  return sizes;
}

function kb(bytes) {
  return Math.round((bytes / 1024) * 10) / 10;
}

function failIf(condition, message, failures) {
  if (condition) failures.push(message);
}

const sizes = distSizes();
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1440, height: 1100 } });
const requests = [];
page.on('requestfinished', async (request) => {
  const response = await request.response();
  requests.push({ url: request.url(), status: response?.status() ?? 0, resourceType: request.resourceType() });
});
await page.goto(url, { waitUntil: 'domcontentloaded' });
await page.waitForLoadState('networkidle', { timeout: 10_000 }).catch(() => {});
const nav = await page.evaluate(() => {
  const n = performance.getEntriesByType('navigation')[0];
  return n ? {
    domContentLoadedMs: Math.round(n.domContentLoadedEventEnd),
    loadMs: Math.round(n.loadEventEnd),
    transferSize: Math.round(n.transferSize || 0),
  } : null;
});
const title = await page.title();
await browser.close();

const report = {
  url,
  title,
  budgets,
  dist: {
    totalKb: kb(sizes.total),
    jsKb: kb(sizes.js),
    cssKb: kb(sizes.css),
    imageKb: kb(sizes.image),
    largestFiles: sizes.files.slice(0, 10).map((f) => ({ file: f.file, kb: kb(f.bytes) })),
  },
  browser: {
    requestCount: requests.length,
    domContentLoadedMs: nav?.domContentLoadedMs ?? null,
    loadMs: nav?.loadMs ?? null,
  },
};

const failures = [];
failIf(report.dist.totalKb > budgets.totalKb, `total ${report.dist.totalKb}KB > ${budgets.totalKb}KB`, failures);
failIf(report.dist.jsKb > budgets.jsKb, `js ${report.dist.jsKb}KB > ${budgets.jsKb}KB`, failures);
failIf(report.dist.cssKb > budgets.cssKb, `css ${report.dist.cssKb}KB > ${budgets.cssKb}KB`, failures);
failIf(report.dist.imageKb > budgets.imageKb, `images ${report.dist.imageKb}KB > ${budgets.imageKb}KB`, failures);
failIf(report.browser.requestCount > budgets.requestCount, `requests ${report.browser.requestCount} > ${budgets.requestCount}`, failures);
if (report.browser.domContentLoadedMs !== null) {
  failIf(report.browser.domContentLoadedMs > budgets.domContentLoadedMs, `DCL ${report.browser.domContentLoadedMs}ms > ${budgets.domContentLoadedMs}ms`, failures);
}

report.passed = failures.length === 0;
report.failures = failures;
mkdirSync('qa/reports', { recursive: true });
writeFileSync('qa/reports/performance-budget.json', JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify(report, null, 2));
if (failures.length) process.exit(1);
