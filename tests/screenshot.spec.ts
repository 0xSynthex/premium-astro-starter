import { test, expect } from '@playwright/test';

test('homepage renders primary conversion path', async ({ page }) => {
  const consoleErrors: string[] = [];
  page.on('console', (msg) => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });

  await page.goto('/');
  await expect(page.getByRole('heading', { name: /Build websites that feel expensive/i })).toBeVisible();
  await expect(page.getByRole('link', { name: /Start with a real brief/i }).first()).toBeVisible();
  await expect(page.getByText(/Brief before design/i)).toBeVisible();
  await expect(page.getByText('Section library', { exact: true })).toBeVisible();
  await expect(page.getByText(/ProofBar/i)).toBeVisible();
  await expect(page.getByText(/Use the sections as a system/i)).toBeVisible();
  expect(consoleErrors).toEqual([]);
});

test('visual screenshot smoke', async ({ page }, testInfo) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot(`homepage-${testInfo.project.name}.png`, {
    fullPage: true,
    maxDiffPixelRatio: 0.02,
  });
});
