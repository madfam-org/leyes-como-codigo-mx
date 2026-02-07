import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';

const mockSetLang = vi.fn();

vi.mock('@/components/providers/LanguageContext', () => ({
    useLang: vi.fn(() => ({ lang: 'es', setLang: mockSetLang })),
}));

import { useLang } from '@/components/providers/LanguageContext';
import { LanguageToggle } from '@/components/LanguageToggle';

describe('LanguageToggle', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        vi.mocked(useLang).mockReturnValue({ lang: 'es', setLang: mockSetLang });
    });

    it('renders ES, EN, and NAH buttons', () => {
        render(<LanguageToggle />);
        expect(screen.getByText('ES')).toBeInTheDocument();
        expect(screen.getByText('EN')).toBeInTheDocument();
        expect(screen.getByText('NAH')).toBeInTheDocument();
    });

    it('clicking EN calls setLang with "en"', () => {
        render(<LanguageToggle />);
        fireEvent.click(screen.getByText('EN'));
        expect(mockSetLang).toHaveBeenCalledWith('en');
    });

    it('clicking ES calls setLang with "es"', () => {
        render(<LanguageToggle />);
        fireEvent.click(screen.getByText('ES'));
        expect(mockSetLang).toHaveBeenCalledWith('es');
    });

    it('ES button has aria-pressed true when lang is es', () => {
        render(<LanguageToggle />);
        const esButton = screen.getByLabelText('Cambiar a español');
        expect(esButton).toHaveAttribute('aria-pressed', 'true');
    });

    it('EN button has aria-pressed false when lang is es', () => {
        render(<LanguageToggle />);
        const enButton = screen.getByLabelText('Switch to English');
        expect(enButton).toHaveAttribute('aria-pressed', 'false');
    });

    it('EN button has aria-pressed true when lang is en', () => {
        vi.mocked(useLang).mockReturnValue({ lang: 'en', setLang: mockSetLang });
        render(<LanguageToggle />);
        const enButton = screen.getByLabelText('Switch to English');
        expect(enButton).toHaveAttribute('aria-pressed', 'true');
    });

    it('ES button has aria-pressed false when lang is en', () => {
        vi.mocked(useLang).mockReturnValue({ lang: 'en', setLang: mockSetLang });
        render(<LanguageToggle />);
        const esButton = screen.getByLabelText('Cambiar a español');
        expect(esButton).toHaveAttribute('aria-pressed', 'false');
    });

    it('has correct aria-label on each button', () => {
        render(<LanguageToggle />);
        expect(screen.getByLabelText('Cambiar a español')).toBeInTheDocument();
        expect(screen.getByLabelText('Switch to English')).toBeInTheDocument();
        expect(screen.getByLabelText('Xicpati nāhuatl')).toBeInTheDocument();
    });

    it('clicking NAH calls setLang with "nah"', () => {
        render(<LanguageToggle />);
        fireEvent.click(screen.getByText('NAH'));
        expect(mockSetLang).toHaveBeenCalledWith('nah');
    });

    it('NAH button has aria-pressed true when lang is nah', () => {
        vi.mocked(useLang).mockReturnValue({ lang: 'nah', setLang: mockSetLang });
        render(<LanguageToggle />);
        const nahButton = screen.getByLabelText('Xicpati nāhuatl');
        expect(nahButton).toHaveAttribute('aria-pressed', 'true');
    });

    it('NAH button has aria-pressed false when lang is es', () => {
        render(<LanguageToggle />);
        const nahButton = screen.getByLabelText('Xicpati nāhuatl');
        expect(nahButton).toHaveAttribute('aria-pressed', 'false');
    });

    it('wrapper has role="group" with aria-label', () => {
        render(<LanguageToggle />);
        expect(screen.getByRole('group', { name: 'Language' })).toBeInTheDocument();
    });
});
