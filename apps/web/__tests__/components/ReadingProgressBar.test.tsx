import { render, screen, fireEvent, act } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { ReadingProgressBar } from '@/components/ReadingProgressBar';

describe('ReadingProgressBar', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        Object.defineProperty(window, 'scrollY', { value: 0, writable: true });
        Object.defineProperty(window, 'innerHeight', { value: 800, writable: true });
        Object.defineProperty(document.documentElement, 'scrollHeight', { value: 2800, writable: true, configurable: true });
    });

    it('renders nothing when progress is 0', () => {
        const { container } = render(<ReadingProgressBar />);
        expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
        expect(container.innerHTML).toBe('');
    });

    it('renders progressbar role when scrolled', () => {
        render(<ReadingProgressBar />);

        act(() => {
            Object.defineProperty(window, 'scrollY', { value: 1000, writable: true });
            fireEvent.scroll(window);
        });

        expect(screen.getByRole('progressbar')).toBeInTheDocument();
    });

    it('has aria-valuenow reflecting scroll progress', () => {
        render(<ReadingProgressBar />);

        // scrollHeight=2800, innerHeight=800, docHeight=2000, scrollY=1000 => 50%
        act(() => {
            Object.defineProperty(window, 'scrollY', { value: 1000, writable: true });
            fireEvent.scroll(window);
        });

        const bar = screen.getByRole('progressbar');
        expect(bar).toHaveAttribute('aria-valuenow', '50');
    });

    it('has aria-valuemin and aria-valuemax attributes', () => {
        render(<ReadingProgressBar />);

        act(() => {
            Object.defineProperty(window, 'scrollY', { value: 500, writable: true });
            fireEvent.scroll(window);
        });

        const bar = screen.getByRole('progressbar');
        expect(bar).toHaveAttribute('aria-valuemin', '0');
        expect(bar).toHaveAttribute('aria-valuemax', '100');
    });

    it('caps progress at 100 when scrolled to bottom', () => {
        render(<ReadingProgressBar />);

        act(() => {
            Object.defineProperty(window, 'scrollY', { value: 3000, writable: true });
            fireEvent.scroll(window);
        });

        const bar = screen.getByRole('progressbar');
        expect(bar).toHaveAttribute('aria-valuenow', '100');
    });
});
