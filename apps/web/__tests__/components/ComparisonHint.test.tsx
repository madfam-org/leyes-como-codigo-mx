import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';

vi.mock('@/components/providers/LanguageContext', () => ({
    useLang: vi.fn(() => ({ lang: 'es', setLang: vi.fn() })),
}));

// Mock localStorage
const localStorageMock = (() => {
    let store: Record<string, string> = {};
    return {
        getItem: vi.fn((key: string) => store[key] ?? null),
        setItem: vi.fn((key: string, value: string) => {
            store[key] = value;
        }),
        removeItem: vi.fn((key: string) => {
            delete store[key];
        }),
        clear: vi.fn(() => {
            store = {};
        }),
        get length() {
            return Object.keys(store).length;
        },
        key: vi.fn((i: number) => Object.keys(store)[i] ?? null),
    };
})();

Object.defineProperty(window, 'localStorage', { value: localStorageMock });

import { ComparisonHint } from '@/components/ComparisonHint';

describe('ComparisonHint', () => {
    beforeEach(() => {
        localStorageMock.clear();
        vi.clearAllMocks();
    });

    it('renders hint text when not dismissed', () => {
        render(<ComparisonHint />);
        expect(screen.getByText('Selecciona leyes para compararlas')).toBeInTheDocument();
    });

    it('renders dismiss button with aria-label', () => {
        render(<ComparisonHint />);
        expect(screen.getByLabelText('Cerrar')).toBeInTheDocument();
    });

    it('hides hint after dismiss button is clicked', () => {
        render(<ComparisonHint />);
        expect(screen.getByText('Selecciona leyes para compararlas')).toBeInTheDocument();

        fireEvent.click(screen.getByLabelText('Cerrar'));

        expect(screen.queryByText('Selecciona leyes para compararlas')).not.toBeInTheDocument();
    });

    it('sets localStorage key on dismiss', () => {
        render(<ComparisonHint />);
        fireEvent.click(screen.getByLabelText('Cerrar'));
        expect(localStorageMock.setItem).toHaveBeenCalledWith('comparison-hint-dismissed', '1');
    });

    it('is hidden when localStorage has comparison-hint-dismissed set', () => {
        localStorageMock.setItem('comparison-hint-dismissed', '1');
        const { container } = render(<ComparisonHint />);
        expect(container.innerHTML).toBe('');
    });
});
