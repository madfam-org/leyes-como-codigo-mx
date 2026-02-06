import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, afterEach } from 'vitest';
import { TableOfContents } from '@/components/laws/TableOfContents';
import { LanguageProvider } from '@/components/providers/LanguageContext';
import type { Article } from '@/components/laws/types';

function renderWithLang(ui: React.ReactElement) {
    return render(<LanguageProvider>{ui}</LanguageProvider>);
}

describe('TableOfContents', () => {
    const mockArticles: Article[] = [
        { article_id: '1', text: 'Artículo primero...' },
        { article_id: '2', text: 'Artículo segundo...' },
        { article_id: '3', text: 'Artículo tercero...' },
    ];

    const mockOnClick = vi.fn();

    afterEach(() => {
        mockOnClick.mockClear();
    });

    it('renders header', () => {
        renderWithLang(
            <TableOfContents articles={mockArticles} activeArticle={null} onArticleClick={mockOnClick} />
        );
        expect(screen.getByText('Tabla de Contenidos')).toBeInTheDocument();
    });

    it('renders article buttons', () => {
        renderWithLang(
            <TableOfContents articles={mockArticles} activeArticle={null} onArticleClick={mockOnClick} />
        );

        expect(screen.getByText('Artículo 1')).toBeInTheDocument();
        expect(screen.getByText('Artículo 2')).toBeInTheDocument();
        expect(screen.getByText('Artículo 3')).toBeInTheDocument();
    });

    it('shows empty state when no articles', () => {
        renderWithLang(
            <TableOfContents articles={[]} activeArticle={null} onArticleClick={mockOnClick} />
        );

        expect(screen.getByText('No se encontraron artículos.')).toBeInTheDocument();
    });

    it('renders article count', () => {
        renderWithLang(
            <TableOfContents articles={mockArticles} activeArticle={null} onArticleClick={mockOnClick} />
        );

        expect(screen.getByText('3 elementos')).toBeInTheDocument();
    });

    it('calls onArticleClick with correct ID', () => {
        renderWithLang(
            <TableOfContents articles={mockArticles} activeArticle={null} onArticleClick={mockOnClick} />
        );

        fireEvent.click(screen.getByText('Artículo 2'));
        expect(mockOnClick).toHaveBeenCalledWith('2');
    });

    it('highlights active article', () => {
        renderWithLang(
            <TableOfContents articles={mockArticles} activeArticle="2" onArticleClick={mockOnClick} />
        );

        const activeButton = screen.getByText('Artículo 2').closest('button');
        expect(activeButton).toHaveClass('bg-primary/10');
        expect(activeButton).toHaveClass('text-primary');
    });

    it('displays "Texto Completo" for texto_completo article_id', () => {
        const articles: Article[] = [
            { article_id: 'texto_completo', text: 'Full text...' },
        ];

        renderWithLang(
            <TableOfContents articles={articles} activeArticle={null} onArticleClick={mockOnClick} />
        );

        expect(screen.getByText('Texto Completo')).toBeInTheDocument();
    });

    it('shows zero count for empty articles', () => {
        renderWithLang(
            <TableOfContents articles={[]} activeArticle={null} onArticleClick={mockOnClick} />
        );

        expect(screen.getByText('0 elementos')).toBeInTheDocument();
    });
});
