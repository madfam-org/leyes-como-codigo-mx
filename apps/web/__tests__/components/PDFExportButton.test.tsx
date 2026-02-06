import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';

vi.mock('@/components/providers/LanguageContext', () => ({
    useLang: vi.fn(() => ({ lang: 'es', setLang: vi.fn() })),
}));

import { PDFExportButton } from '@/components/PDFExportButton';

describe('PDFExportButton', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        window.print = vi.fn();
    });

    it('renders the button', () => {
        render(<PDFExportButton />);
        expect(screen.getByRole('button')).toBeInTheDocument();
    });

    it('shows "Imprimir / PDF" title in Spanish', () => {
        render(<PDFExportButton />);
        expect(screen.getByTitle('Imprimir / PDF')).toBeInTheDocument();
    });

    it('displays button text', () => {
        render(<PDFExportButton />);
        expect(screen.getByText('Imprimir / PDF')).toBeInTheDocument();
    });

    it('calls window.print on click', () => {
        render(<PDFExportButton />);
        fireEvent.click(screen.getByRole('button'));
        expect(window.print).toHaveBeenCalledOnce();
    });

    it('renders printer icon as aria-hidden', () => {
        const { container } = render(<PDFExportButton />);
        const svg = container.querySelector('svg');
        expect(svg).toHaveAttribute('aria-hidden', 'true');
    });
});
