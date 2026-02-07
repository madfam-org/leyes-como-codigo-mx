import { test, expect } from './fixtures';

test.describe('Search filters', () => {
    test.beforeEach(async ({ page }) => {
        // Mock municipalities endpoint used by SearchFilters
        await page.route('**/api/v1/municipalities/*', (route) =>
            route.fulfill({ json: [] })
        );
    });

    test('changing jurisdiction filter updates URL', async ({ page }) => {
        await page.goto('/busqueda?q=ley');

        // Wait for results to render
        await expect(page.getByText('Ley Federal del Trabajo').first()).toBeVisible();

        // On desktop, filters sidebar is visible. Click "Estatal" jurisdiction button.
        const estatalButton = page.getByRole('button', { name: /Estatal/ });
        await estatalButton.click();

        // URL should include jurisdiction param with state
        await expect(page).toHaveURL(/jurisdiction=.*state/);
    });

    test('clear filters resets URL to query only', async ({ page }) => {
        // Start with a non-default filter in URL
        await page.goto('/busqueda?q=ley&jurisdiction=federal,state');

        // Wait for results to render
        await expect(page.getByText('Ley Federal del Trabajo').first()).toBeVisible();

        // The "Limpiar" (clear) button should appear since filters are non-default
        const clearButton = page.getByRole('button', { name: /Limpiar/ });
        await expect(clearButton).toBeVisible();

        await clearButton.click();

        // After clearing, URL should reset to default jurisdiction (federal only)
        await expect(page).toHaveURL(/q=ley/);
        await expect(page).toHaveURL(/jurisdiction=federal/);
        // State should no longer be in jurisdiction
        await expect(page).not.toHaveURL(/jurisdiction=.*state/);
    });

    test('filter state persists in URL across page reload', async ({ page }) => {
        await page.goto('/busqueda?q=ley');

        // Wait for results
        await expect(page.getByText('Ley Federal del Trabajo').first()).toBeVisible();

        // Click "Estatal" to add state jurisdiction
        const estatalButton = page.getByRole('button', { name: /Estatal/ });
        await estatalButton.click();

        // Verify URL has the state jurisdiction
        await expect(page).toHaveURL(/jurisdiction=.*state/);

        // The "Estatal" button should have aria-pressed="true"
        await expect(estatalButton).toHaveAttribute('aria-pressed', 'true');

        // Reload the page
        await page.reload();

        // Wait for results again
        await expect(page.getByText('Ley Federal del Trabajo').first()).toBeVisible();

        // The "Estatal" button should still be pressed after reload
        const estatalBtnAfterReload = page.getByRole('button', { name: /Estatal/ });
        await expect(estatalBtnAfterReload).toHaveAttribute('aria-pressed', 'true');
    });
});
