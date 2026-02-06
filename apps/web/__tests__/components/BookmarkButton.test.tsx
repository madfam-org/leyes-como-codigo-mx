import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';

vi.mock('@/components/providers/LanguageContext', () => ({
    useLang: vi.fn(() => ({ lang: 'es', setLang: vi.fn() })),
}));

const mockToggle = vi.fn();
const mockIsBookmarked = vi.fn(() => false);

vi.mock('@/components/providers/BookmarksContext', () => ({
    useBookmarks: () => ({
        bookmarks: [],
        isBookmarked: mockIsBookmarked,
        toggleBookmark: mockToggle,
        removeBookmark: vi.fn(),
    }),
}));

import { BookmarkButton } from '@/components/BookmarkButton';

describe('BookmarkButton', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        mockIsBookmarked.mockReturnValue(false);
    });

    it('renders add state', () => {
        render(<BookmarkButton lawId="cpeum" lawName="Constitución" />);
        expect(screen.getByTitle('Agregar a favoritos')).toBeDefined();
    });

    it('calls toggleBookmark on click', () => {
        render(<BookmarkButton lawId="cpeum" lawName="Constitución" />);
        fireEvent.click(screen.getByTitle('Agregar a favoritos'));
        expect(mockToggle).toHaveBeenCalledWith('cpeum', 'Constitución');
    });

    it('shows active state when bookmarked', () => {
        mockIsBookmarked.mockReturnValue(true);
        render(<BookmarkButton lawId="cpeum" lawName="Constitución" />);
        expect(screen.getByTitle('Quitar de favoritos')).toBeDefined();
    });
});
