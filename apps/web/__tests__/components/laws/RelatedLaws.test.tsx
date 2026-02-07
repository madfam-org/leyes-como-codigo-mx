import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { RelatedLaws } from '@/components/laws/RelatedLaws';
import { api } from '@/lib/api';

// Mock dependencies
vi.mock('@/lib/api', () => ({
    api: {
        getRelatedLaws: vi.fn(),
    },
}));

vi.mock('@/components/providers/LanguageContext', () => ({
    useLang: () => ({ lang: 'es' }),
}));

vi.mock('next/link', () => ({
    default: ({ children, href, ...props }: { children: React.ReactNode; href: string; [key: string]: unknown }) => (
        <a href={href} {...props}>{children}</a>
    ),
}));

vi.mock('@tezca/ui', () => ({
    Card: ({ children, className }: { children: React.ReactNode; className?: string }) => (
        <div data-testid="card" className={className}>{children}</div>
    ),
    CardContent: ({ children, className }: { children: React.ReactNode; className?: string }) => (
        <div className={className}>{children}</div>
    ),
    Badge: ({ children, variant, className }: { children: React.ReactNode; variant?: string; className?: string }) => (
        <span data-testid="badge" data-variant={variant} className={className}>{children}</span>
    ),
}));

const mockRelated = [
    { law_id: 'ley-amparo', name: 'Ley de Amparo', tier: 'federal', category: 'constitucional', score: 0.95 },
    { law_id: 'codigo-penal', name: 'Codigo Penal Federal', tier: 'federal', category: 'penal', score: 0.82 },
];

describe('RelatedLaws', () => {
    beforeEach(() => {
        vi.mocked(api.getRelatedLaws).mockReset();
    });

    it('shows loading skeleton while fetching', () => {
        vi.mocked(api.getRelatedLaws).mockReturnValue(new Promise(() => {})); // never resolves

        const { container } = render(<RelatedLaws lawId="constitucion" />);

        expect(screen.getByText('Leyes Relacionadas')).toBeInTheDocument();
        expect(container.querySelector('.animate-pulse')).toBeInTheDocument();
    });

    it('renders related law cards after loading', async () => {
        vi.mocked(api.getRelatedLaws).mockResolvedValue({
            law_id: 'constitucion',
            related: mockRelated,
        });

        render(<RelatedLaws lawId="constitucion" />);

        await waitFor(() => {
            expect(screen.getByText('Ley de Amparo')).toBeInTheDocument();
        });

        expect(screen.getByText('Codigo Penal Federal')).toBeInTheDocument();
    });

    it('renders tier and category badges', async () => {
        vi.mocked(api.getRelatedLaws).mockResolvedValue({
            law_id: 'constitucion',
            related: [mockRelated[0]],
        });

        render(<RelatedLaws lawId="constitucion" />);

        await waitFor(() => {
            expect(screen.getByText('Federal')).toBeInTheDocument();
        });

        expect(screen.getByText('constitucional')).toBeInTheDocument();
    });

    it('generates correct links to law detail pages', async () => {
        vi.mocked(api.getRelatedLaws).mockResolvedValue({
            law_id: 'constitucion',
            related: [mockRelated[0]],
        });

        render(<RelatedLaws lawId="constitucion" />);

        await waitFor(() => {
            const link = screen.getByText('Ley de Amparo').closest('a');
            expect(link).toHaveAttribute('href', '/leyes/ley-amparo');
        });
    });

    it('returns null when no related laws found', async () => {
        vi.mocked(api.getRelatedLaws).mockResolvedValue({
            law_id: 'constitucion',
            related: [],
        });

        const { container } = render(<RelatedLaws lawId="constitucion" />);

        await waitFor(() => {
            expect(container.querySelector('.animate-pulse')).not.toBeInTheDocument();
        });

        // Component returns null for empty results
        expect(screen.queryByText('Leyes Relacionadas')).not.toBeInTheDocument();
    });

    it('returns null when API call fails', async () => {
        vi.mocked(api.getRelatedLaws).mockRejectedValue(new Error('API error'));

        const { container } = render(<RelatedLaws lawId="constitucion" />);

        await waitFor(() => {
            expect(container.querySelector('.animate-pulse')).not.toBeInTheDocument();
        });

        // Falls back to empty array, so renders null
        expect(screen.queryByText('Leyes Relacionadas')).not.toBeInTheDocument();
    });

    it('calls api.getRelatedLaws with correct lawId', () => {
        vi.mocked(api.getRelatedLaws).mockReturnValue(new Promise(() => {}));

        render(<RelatedLaws lawId="ley-de-amparo" />);

        expect(api.getRelatedLaws).toHaveBeenCalledWith('ley-de-amparo');
    });

    it('renders section with accessible aria-label after loading', async () => {
        vi.mocked(api.getRelatedLaws).mockResolvedValue({
            law_id: 'constitucion',
            related: mockRelated,
        });

        render(<RelatedLaws lawId="constitucion" />);

        await waitFor(() => {
            const section = screen.getByRole('region', { name: 'Leyes Relacionadas' });
            expect(section).toBeInTheDocument();
        });
    });
});
