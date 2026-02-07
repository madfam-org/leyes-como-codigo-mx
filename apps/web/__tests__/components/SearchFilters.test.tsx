import { render, screen, fireEvent, act } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { SearchFilters, type SearchFilterState } from '@/components/SearchFilters';
import { LanguageProvider } from '@/components/providers/LanguageContext';
import { api } from '@/lib/api';

// Mock the API
vi.mock('@/lib/api', () => ({
    api: {
        getStates: vi.fn().mockResolvedValue({ states: [] }),
        getMunicipalities: vi.fn().mockResolvedValue([]),
    },
}));

function renderWithLang(ui: React.ReactElement) {
    return render(<LanguageProvider>{ui}</LanguageProvider>);
}

describe('SearchFilters', () => {
    const mockFilters: SearchFilterState = {
        jurisdiction: ['federal'],
        category: null,
        state: null,
        municipality: null,
        status: 'all',
        sort: 'relevance',
        title: '',
        chapter: '',
        law_type: 'all',
    };

    const mockOnChange = vi.fn();

    beforeEach(() => {
        mockOnChange.mockReset();
        vi.mocked(api.getStates).mockResolvedValue({ states: [] });
    });

    it('renders jurisdiction options', async () => {
        await act(async () => {
            renderWithLang(<SearchFilters filters={mockFilters} onFiltersChange={mockOnChange} resultCount={10} />);
        });

        expect(screen.getByRole('button', { name: /Federal/i })).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /Estatal/i })).toBeInTheDocument();
    });

    it('calls onFiltersChange when jurisdiction changes', async () => {
        await act(async () => {
            renderWithLang(<SearchFilters filters={mockFilters} onFiltersChange={mockOnChange} resultCount={10} />);
        });

        const federalButton = screen.getByRole('button', { name: /Federal/i });
        fireEvent.click(federalButton);

        expect(mockOnChange).toHaveBeenCalled();
    });

    it('shows state dropdown when state jurisdiction is selected', async () => {
        const mockGetStates = vi.mocked(api.getStates);
        mockGetStates.mockResolvedValue({ states: ['Colima', 'Jalisco'] });

        await act(async () => {
            renderWithLang(<SearchFilters filters={{ ...mockFilters, jurisdiction: ['state'] }} onFiltersChange={mockOnChange} resultCount={10} />);
        });

        expect(await screen.findByText('Estado')).toBeInTheDocument();
        expect(mockGetStates).toHaveBeenCalled();
    });

    describe('Structural Filters', () => {
        it('renders title and chapter inputs', async () => {
            await act(async () => {
                renderWithLang(<SearchFilters filters={mockFilters} onFiltersChange={mockOnChange} resultCount={10} />);
            });

            expect(screen.getByPlaceholderText(/Filtrar por t.tulo/i)).toBeInTheDocument();
            expect(screen.getByPlaceholderText(/Filtrar por cap.tulo/i)).toBeInTheDocument();
        });

        it('calls onFiltersChange when title input changes', async () => {
            await act(async () => {
                renderWithLang(<SearchFilters filters={mockFilters} onFiltersChange={mockOnChange} resultCount={10} />);
            });

            const titleInput = screen.getByPlaceholderText(/Filtrar por t.tulo/i);
            fireEvent.change(titleInput, { target: { value: 'Titulo I' } });

            expect(mockOnChange).toHaveBeenCalledWith(expect.objectContaining({
                title: 'Titulo I'
            }));
        });
    });

    describe('Facets', () => {
        const facets = {
            by_tier: [
                { key: 'federal', count: 333 },
                { key: 'state', count: 11363 },
                { key: 'municipal', count: 0 },
            ],
            by_category: [
                { key: 'civil', count: 120 },
                { key: 'penal', count: 85 },
            ],
            by_status: [
                { key: 'vigente', count: 400 },
                { key: 'abrogado', count: 15 },
            ],
            by_law_type: [
                { key: 'legislative', count: 250 },
                { key: 'non_legislative', count: 150 },
            ],
        };

        it('displays facet counts next to jurisdiction buttons', async () => {
            await act(async () => {
                renderWithLang(
                    <SearchFilters
                        filters={mockFilters}
                        onFiltersChange={mockOnChange}
                        resultCount={10}
                        facets={facets}
                    />
                );
            });

            // Facet counts are rendered as (N) next to jurisdiction names
            expect(screen.getByText('(333)')).toBeInTheDocument();
            expect(screen.getByText('(11,363)')).toBeInTheDocument();
            expect(screen.getByText('(0)')).toBeInTheDocument();
        });

        it('applies opacity-50 class to jurisdiction button with zero count', async () => {
            await act(async () => {
                renderWithLang(
                    <SearchFilters
                        filters={mockFilters}
                        onFiltersChange={mockOnChange}
                        resultCount={10}
                        facets={facets}
                    />
                );
            });

            // Municipal has count 0, its button should have opacity-50
            const municipalButton = screen.getByRole('button', { name: /Municipal/i });
            expect(municipalButton.className).toContain('opacity-50');
        });

        it('does not show facet counts when facets prop is not provided', async () => {
            await act(async () => {
                renderWithLang(
                    <SearchFilters
                        filters={mockFilters}
                        onFiltersChange={mockOnChange}
                        resultCount={10}
                    />
                );
            });

            // Without facets, no parenthesized counts should appear next to jurisdictions
            expect(screen.queryByText('(333)')).not.toBeInTheDocument();
            expect(screen.queryByText('(0)')).not.toBeInTheDocument();
        });
    });
});
