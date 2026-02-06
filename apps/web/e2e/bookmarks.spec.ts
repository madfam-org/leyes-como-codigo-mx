import { test, expect } from './fixtures';

test.describe('Bookmarks flow', () => {
    test('bookmark button toggles on law detail page', async ({ page }) => {
        await page.goto('/laws/ley-federal-del-trabajo');

        // Wait for law to load
        await expect(page.getByText('Ley Federal del Trabajo').first()).toBeVisible();

        // Bookmark button shows "Agregar a favoritos" initially
        const bookmarkBtn = page.locator('button[title="Agregar a favoritos"]');
        await expect(bookmarkBtn).toBeVisible();

        // Click to bookmark
        await bookmarkBtn.click();

        // Title changes to "Quitar de favoritos"
        const removeBtn = page.locator('button[title="Quitar de favoritos"]');
        await expect(removeBtn).toBeVisible();
        await expect(removeBtn).toHaveAttribute('aria-pressed', 'true');

        // Click again to un-bookmark
        await removeBtn.click();

        // Back to "Agregar a favoritos"
        await expect(page.locator('button[title="Agregar a favoritos"]')).toBeVisible();
    });

    test('favoritos page shows bookmarked law or empty state', async ({ page }) => {
        // Visit favoritos with no bookmarks — empty state
        await page.goto('/favoritos');

        await expect(page.getByText('No tienes leyes guardadas')).toBeVisible();
        await expect(page.getByText('Explorar leyes')).toBeVisible();

        // Now bookmark a law via the detail page
        await page.goto('/laws/ley-federal-del-trabajo');
        await expect(page.getByText('Ley Federal del Trabajo').first()).toBeVisible();

        await page.locator('button[title="Agregar a favoritos"]').click();
        await expect(page.locator('button[title="Quitar de favoritos"]')).toBeVisible();

        // Navigate to favoritos — bookmarked law appears
        await page.goto('/favoritos');

        await expect(page.getByText('Favoritos').first()).toBeVisible();
        await expect(page.getByText('Ley Federal del Trabajo').first()).toBeVisible();
    });

    test('bookmark persists across navigation (localStorage)', async ({ page }) => {
        // Bookmark a law
        await page.goto('/laws/ley-federal-del-trabajo');
        await expect(page.getByText('Ley Federal del Trabajo').first()).toBeVisible();

        await page.locator('button[title="Agregar a favoritos"]').click();
        await expect(page.locator('button[title="Quitar de favoritos"]')).toBeVisible();

        // Navigate away to homepage
        await page.goto('/');
        await expect(page.getByText('Tezca').first()).toBeVisible();

        // Navigate back to same law detail page
        await page.goto('/laws/ley-federal-del-trabajo');
        await expect(page.getByText('Ley Federal del Trabajo').first()).toBeVisible();

        // Bookmark should still be active
        await expect(page.locator('button[title="Quitar de favoritos"]')).toBeVisible();
        await expect(page.locator('button[title="Quitar de favoritos"]')).toHaveAttribute('aria-pressed', 'true');
    });
});
