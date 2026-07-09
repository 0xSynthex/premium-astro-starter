# Premium Astro Starter

Free/open-source starter for professional landing pages.

## What is included

- Astro static build
- CSS design tokens in `src/styles/global.css`
- premium editorial landing example
- Playwright desktop/mobile smoke + screenshot QA
- GitHub Actions workflow for free GitHub Pages deploys
- no paid APIs required

## Commands

```bash
npm install
npm run dev
npm run build
npm run test
npm run qa
```

## Workflow

1. Collect website brief: goal, audience, CTA, references, assets, constraints.
2. Choose surface type. Landing pages are usually Decide/Learn.
3. Define compact design system in `src/styles/global.css`.
4. Implement in `src/pages/index.astro` or split into components for larger sites.
5. Run `npm run qa` before delivery.
6. If deploying, verify live URL with curl/browser.

## GitHub Pages

This repo includes `.github/workflows/pages.yml`.

- Push to `main`.
- In GitHub repo settings, set Pages source to GitHub Actions if needed.
- The workflow runs audit, build, and Playwright tests before deploy.

## Security

Do not commit secrets, customer data, private screenshots, `.env`, credentials, or client material. Keep this starter generic and safe for public GitHub.

## Free recommended additions

- GitHub Pages / Cloudflare Pages free plan for preview deploys.
- Figma free plan + manual exported screenshots if no API token is available.
- Browser DevTools + Playwright screenshots for visual QA.
- ImageMagick/cwebp/sharp for asset optimization.

Secrets/API keys are optional and should live in `.env`, never in chat.
