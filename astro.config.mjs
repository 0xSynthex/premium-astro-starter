import { defineConfig } from 'astro/config';

const base = process.env.GITHUB_REPOSITORY?.endsWith('/premium-astro-starter') ? '/premium-astro-starter' : '/';

export default defineConfig({
  output: 'static',
  base,
});
