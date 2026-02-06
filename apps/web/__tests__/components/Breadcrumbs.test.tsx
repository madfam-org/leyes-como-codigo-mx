import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';

vi.mock('@/components/providers/LanguageContext', () => ({
    useLang: vi.fn(() => ({ lang: 'es', setLang: vi.fn() })),
}));

import { Breadcrumbs } from '@/components/Breadcrumbs';

describe('Breadcrumbs', () => {
    it('renders with law name', () => {
        render(<Breadcrumbs lawName="Constitución Política" />);
        expect(screen.getByText('Inicio')).toBeDefined();
        expect(screen.getByText('Explorar')).toBeDefined();
        expect(screen.getByText('Constitución Política')).toBeDefined();
    });

    it('has aria-label', () => {
        render(<Breadcrumbs lawName="Test Law" />);
        expect(screen.getByLabelText('Breadcrumb')).toBeDefined();
    });

    it('marks current page', () => {
        render(<Breadcrumbs lawName="Test Law" />);
        const current = screen.getByText('Test Law');
        expect(current.getAttribute('aria-current')).toBe('page');
    });

    it('renders links for home and explore', () => {
        render(<Breadcrumbs lawName="Test" />);
        const inicio = screen.getByText('Inicio');
        expect(inicio.closest('a')?.getAttribute('href')).toBe('/');
        const explorar = screen.getByText('Explorar');
        expect(explorar.closest('a')?.getAttribute('href')).toBe('/laws');
    });
});
