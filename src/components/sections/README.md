# Section Library

Reusable Astro sections for premium landing pages. Keep copy concrete and proof-led; these components are structure, not filler.

## Components

- `HeroEditorial.astro` — high-impact Decide/Learn hero with CTA and proof chips.
- `DirectionBoard.astro` — visual board / product preview shell.
- `BriefChecklist.astro` — intake checklist or requirements grid.
- `ProofBar.astro` — compact trust/proof metrics; use real proof only.
- `ProcessSteps.astro` — process/how-it-works sequence.
- `ComparisonBand.astro` — generic vs premium comparison rows.
- `FaqList.astro` — native `<details>` FAQ block.
- `LeadCaptureForm.astro` — accessible backend-neutral lead form with honeypot/privacy/tracking hooks.
- `FinalCta.astro` — final conversion section.
- `MobileStickyCta.astro` — mobile-only sticky CTA.

## Rules

- Do not invent testimonials, client logos, metrics, or proof.
- Prefer fewer, stronger sections over long generic pages.
- Landing pages are usually Decide/Learn surfaces: one idea per section.
- If a component encourages filler, rewrite the content or delete the component.
- Verify desktop/mobile screenshots after composing sections.
- Never wire a form to production storage until backend, privacy, retention, and deletion policy are ready.
