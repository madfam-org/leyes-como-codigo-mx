import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import ComparisonView from '@/components/ComparisonView';
import { api } from '@/lib/api';

// Mock API
vi.mock('@/lib/api', () => ({
    api: {
        getLawArticles: vi.fn(),
        getLawStructure: vi.fn(),
    },
}));

describe('ComparisonView', () => {
    const mockArticles1 = {
        law_id: 'law_1',
        law_name: 'Law 1',
        articles: [{ article_id: 'Art 1', text: 'Text 1' }],
    };
    const mockArticles2 = {
        law_id: 'law_2',
        law_name: 'Law 2',
        articles: [{ article_id: 'Art 1', text: 'Text 1 modified' }],
    };
    
    const mockStructure = {
        law_id: 'law_1',
        structure: [
            { label: 'Book I', children: [] }
        ]
    };

    it('renders loading state initially', () => {
        render(<ComparisonView lawIds={['1', '2']} />);
        expect(screen.getByText(/Analizando estructura legal/i)).toBeInTheDocument();
    });

    it('renders comparison split view', async () => {
        vi.mocked(api.getLawArticles).mockImplementation(async (id) => {
            if (id === '1') return mockArticles1;
            if (id === '2') return mockArticles2;
            throw new Error('Not found');
        });
            
        vi.mocked(api.getLawStructure)
            .mockResolvedValue({ law_id: 'law_1', structure: [] });

        render(<ComparisonView lawIds={['1', '2']} />);

        await waitFor(() => {
            expect(screen.getByText('Law 1')).toBeInTheDocument();
            expect(screen.getByText('Law 2')).toBeInTheDocument();
        });
        
        expect(screen.getByText('Comparación Estructural')).toBeInTheDocument();
    });

    it('renders structure sidebar', async () => {
        vi.mocked(api.getLawArticles)
            .mockResolvedValue(mockArticles1);
        vi.mocked(api.getLawStructure)
            .mockResolvedValue(mockStructure);

        render(<ComparisonView lawIds={['1', '2']} />);

        await waitFor(() => {
            // Check if structure is rendered (might be hidden on mobile but present in DOM)
            expect(screen.getAllByText('Book I')[0]).toBeInTheDocument();
        });
    });
});
