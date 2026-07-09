# Premium Astro Starter

Free/open-source starter for professional landing pages.

## What is included

- Astro static build
- CSS design tokens in `src/styles/global.css`
- premium editorial landing example
- reusable Astro section library in `src/components/sections/`
- copy/conversion templates in `copy/`
- website QA report template in `qa/`
- Playwright desktop/mobile smoke + screenshot QA
- free local image optimization via ImageMagick + cwebp
- GitHub Pages deploy path via committed `docs/` output
- GitHub Actions workflow template kept disabled because the current GitHub token lacks `workflow` scope
- no paid APIs required

## Commands

```bash
npm install
npm run dev
npm run build
npm run test
npm run qa
npm run qa:perf
npm run qa:full
npm run optimize:images -- assets/raw public/images
~/bin/create-premium-site my-project
```

## Workflow

1. Collect website brief: goal, audience, CTA, references, assets, constraints.
2. Choose surface type. Landing pages are usually Decide/Learn.
3. Draft copy with `copy/landing-brief.md`, `copy/hero-formulas.md`, and `copy/objections.md`.
4. Define compact design system in `src/styles/global.css`.
5. Implement in `src/pages/index.astro` or split into components for larger sites.
6. Run `npm run qa` and fill `qa/website-qa-template.md` before delivery.
7. If deploying, verify live URL with curl/browser.

## GitHub Pages free deploy

This repo uses the free branch deploy path:

1. Run `npm run qa`.
2. Copy `dist/` to `docs/`.
3. Commit and push `docs/`.
4. Configure GitHub Pages source as `main` branch, `/docs` folder.

A GitHub Actions workflow template is stored at `.github/workflows.disabled/pages.yml.template`. To enable Actions deploy later, re-authenticate `gh` with `workflow` scope, move it to `.github/workflows/pages.yml`, and push.

## Security

Do not commit secrets, customer data, private screenshots, `.env`, credentials, or client material. Keep this starter generic and safe for public GitHub.

## Image optimization

Use the local free pipeline before committing public image assets:

```bash
npm run optimize:images -- assets/raw public/images
npm run optimize:images -- assets/raw public/images -- --max-width 1600 --quality 78
```

Behavior:

- jpg/jpeg/png/webp: auto-orient, strip metadata, resize down, compress
- jpg/jpeg/png: also creates a `.webp` version
- svg/gif/avif: copied unchanged
- unknown file types: skipped and reported

Keep private/raw client material out of git unless explicitly approved for that project.

## Section library

Reusable sections live in `src/components/sections/`:

- `HeroEditorial.astro` — Decide/Learn hero with CTA and proof chips
- `DirectionBoard.astro` — preview / visual board shell
- `BriefChecklist.astro` — intake checklist grid
- `ProofBar.astro` — real proof/trust metrics
- `ProcessSteps.astro` — how-it-works/process sequence
- `ComparisonBand.astro` — generic vs premium comparison
- `FaqList.astro` — native FAQ block
- `FinalCta.astro` — final conversion block
- `MobileStickyCta.astro` — mobile sticky CTA

Rule: use sections to clarify the offer, prove trust, answer objections, or move the user toward the CTA. Delete any section that becomes filler.

## Copy and conversion

Templates live in `copy/`:

- `landing-brief.md` — collect offer, audience, proof, objections, tone, CTA
- `hero-formulas.md` — headline/subcopy/CTA structures
- `objections.md` — map objections to page sections

Full framework:

```text
/home/hermes/wiki/design/copy-conversion-framework.md
```

QA template:

```text
qa/website-qa-template.md
```

Rules: never invent testimonials, logos, metrics, or outcomes. Use real proof, process clarity, or ask for missing business input.

## Performance budget

Run the free local budget check:

```bash
npm run qa:perf
```

It builds the site, checks `dist/` asset budgets, opens the page with Playwright, counts requests, and writes:

```text
qa/reports/performance-budget.json
```

Default budgets can be overridden per run:

```bash
PERF_TOTAL_KB=650 PERF_IMAGE_KB=400 npm run qa:perf
```

Use `npm run qa:full` before serious delivery.

## Create a new project

Use the local generator:

```bash
~/bin/create-premium-site my-project
```

It copies this starter without `.git`, `node_modules`, build output, `docs`, test output, or `.env*`; updates `package.json`; creates project folders; and initializes a fresh local git repo. It does not push or create a GitHub repo.

## Free recommended additions

- GitHub Pages / Cloudflare Pages free plan for preview deploys.
- Figma free plan + manual exported screenshots if no API token is available.
- Browser DevTools + Playwright screenshots for visual QA.
- ImageMagick/cwebp/sharp for asset optimization.

Secrets/API keys are optional and should live in `.env`, never in chat.
