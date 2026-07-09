# Lead Capture Pattern

Use `src/components/sections/LeadCaptureForm.astro` for static landing pages that need a safe form structure before backend integration.

## Included

- Accessible labels and required fields
- Honeypot anti-spam field named `website`
- Privacy copy slot via prop
- Loading/status UI hooks
- `lead_form_submit` browser event for analytics integration
- `data-track-form="lead"` marker for GTM/analytics hooks

## Backend integration

Default `action="#"` is a placeholder. Replace with a project-approved backend:

- existing API endpoint
- static form provider
- Cloudflare Worker
- serverless function
- same-server POST endpoint

Do not collect sensitive data unless storage, retention, privacy copy, and deletion policy are ready.

## Analytics hook

```js
window.addEventListener('lead_form_submit', (event) => {
  // Push to analytics only after consent / project policy allows it.
});
```

## Security

Never commit form provider tokens, webhook secrets, OAuth credentials, or private submissions. Keep secrets in environment/profile config only.
