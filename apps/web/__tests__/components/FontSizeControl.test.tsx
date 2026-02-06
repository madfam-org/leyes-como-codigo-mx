import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';

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

import { FontSizeControl } from '@/components/FontSizeControl';

describe('FontSizeControl', () => {
    const mockOnChange = vi.fn();

    beforeEach(() => {
        localStorageMock.clear();
        vi.clearAllMocks();
    });

    it('renders three font size buttons', () => {
        render(<FontSizeControl onChange={mockOnChange} />);
        expect(screen.getByLabelText('Small text')).toBeInTheDocument();
        expect(screen.getByLabelText('Normal text')).toBeInTheDocument();
        expect(screen.getByLabelText('Large text')).toBeInTheDocument();
    });

    it('renders button labels A-, A, A+', () => {
        render(<FontSizeControl onChange={mockOnChange} />);
        expect(screen.getByText('A-')).toBeInTheDocument();
        expect(screen.getByText('A')).toBeInTheDocument();
        expect(screen.getByText('A+')).toBeInTheDocument();
    });

    it('calls onChange with text-sm when small button clicked', () => {
        render(<FontSizeControl onChange={mockOnChange} />);
        fireEvent.click(screen.getByLabelText('Small text'));
        expect(mockOnChange).toHaveBeenCalledWith('text-sm');
    });

    it('calls onChange with text-lg when large button clicked', () => {
        render(<FontSizeControl onChange={mockOnChange} />);
        fireEvent.click(screen.getByLabelText('Large text'));
        expect(mockOnChange).toHaveBeenCalledWith('text-lg');
    });

    it('stores selected size in localStorage', () => {
        render(<FontSizeControl onChange={mockOnChange} />);
        fireEvent.click(screen.getByLabelText('Small text'));
        expect(localStorageMock.setItem).toHaveBeenCalledWith('preferred-font-size', 'text-sm');
    });

    it('has aria-pressed true on the active button', () => {
        render(<FontSizeControl onChange={mockOnChange} />);
        // Default is text-base
        expect(screen.getByLabelText('Normal text')).toHaveAttribute('aria-pressed', 'true');
        expect(screen.getByLabelText('Small text')).toHaveAttribute('aria-pressed', 'false');
        expect(screen.getByLabelText('Large text')).toHaveAttribute('aria-pressed', 'false');
    });

    it('has role="group" with aria-label "Font size"', () => {
        render(<FontSizeControl onChange={mockOnChange} />);
        expect(screen.getByRole('group', { name: 'Font size' })).toBeInTheDocument();
    });
});
