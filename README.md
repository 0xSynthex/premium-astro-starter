# Premium Astro Starter

Free/open-source starter for professional landing pages.

## What is included

- Astro static build
- CSS design tokens in `src/styles/global.css`
- premium editorial landing example
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
npm run optimize:images -- assets/raw public/images
```

## Workflow

1. Collect website brief: goal, audience, CTA, references, assets, constraints.
2. Choose surface type. Landing pages are usually Decide/Learn.
3. Define compact design system in `src/styles/global.css`.
4. Implement in `src/pages/index.astro` or split into components for larger sites.
5. Run `npm run qa` before delivery.
6. If deploying, verify live URL with curl/browser.

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

## Free recommended additions

- GitHub Pages / Cloudflare Pages free plan for preview deploys.
- Figma free plan + manual exported screenshots if no API token is available.
- Browser DevTools + Playwright screenshots for visual QA.
- ImageMagick/cwebp/sharp for asset optimization.

Secrets/API keys are optional and should live in `.env`, never in chat.
