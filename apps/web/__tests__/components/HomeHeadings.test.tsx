import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { langState } from '../helpers/lang-mock';

const mockUseLang = vi.fn();
vi.mock('@/components/providers/LanguageContext', () => ({
    useLang: () => mockUseLang(),
}));

import { HomeHeadings } from '@/components/HomeHeadings';

describe('HomeHeadings', () => {
    it('renders heading in Spanish by default', () => {
        mockUseLang.mockReturnValue(langState('es'));
        render(<HomeHeadings />);
        expect(screen.getByText('Explorar por Jurisdicción')).toBeInTheDocument();
    });

    it('renders heading in English', () => {
        mockUseLang.mockReturnValue(langState('en'));
        render(<HomeHeadings />);
        expect(screen.getByText('Explore by Jurisdiction')).toBeInTheDocument();
    });

    it('renders heading in Nahuatl', () => {
        mockUseLang.mockReturnValue(langState('nah'));
        render(<HomeHeadings />);
        expect(screen.getByText('Xictlachiya ic Tēyācanaliztli')).toBeInTheDocument();
    });
});
