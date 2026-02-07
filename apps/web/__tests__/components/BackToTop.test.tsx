import { render, screen, fireEvent, act } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { BackToTop } from '@/components/BackToTop';

describe('BackToTop', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        Object.defineProperty(window, 'scrollY', { value: 0, writable: true });
        window.scrollTo = vi.fn();
    });

    it('is not visible initially when scrollY is 0', () => {
        render(<BackToTop />);
        expect(screen.queryByRole('button', { name: 'Volver arriba' })).not.toBeInTheDocument();
    });

    it('becomes visible when scrollY exceeds 400', () => {
        render(<BackToTop />);

        act(() => {
            Object.defineProperty(window, 'scrollY', { value: 500, writable: true });
            fireEvent.scroll(window);
        });

        expect(screen.getByRole('button', { name: 'Volver arriba' })).toBeInTheDocument();
    });

    it('hides again when scrollY drops below 400', () => {
        render(<BackToTop />);

        act(() => {
            Object.defineProperty(window, 'scrollY', { value: 500, writable: true });
            fireEvent.scroll(window);
        });

        expect(screen.getByRole('button', { name: 'Volver arriba' })).toBeInTheDocument();

        act(() => {
            Object.defineProperty(window, 'scrollY', { value: 100, writable: true });
            fireEvent.scroll(window);
        });

        expect(screen.queryByRole('button', { name: 'Volver arriba' })).not.toBeInTheDocument();
    });

    it('calls window.scrollTo on click', () => {
        render(<BackToTop />);

        act(() => {
            Object.defineProperty(window, 'scrollY', { value: 500, writable: true });
            fireEvent.scroll(window);
        });

        const button = screen.getByRole('button', { name: 'Volver arriba' });
        fireEvent.click(button);

        expect(window.scrollTo).toHaveBeenCalledWith({ top: 0, behavior: 'smooth' });
    });

    it('has aria-label "Volver arriba"', () => {
        render(<BackToTop />);

        act(() => {
            Object.defineProperty(window, 'scrollY', { value: 500, writable: true });
            fireEvent.scroll(window);
        });

        const button = screen.getByLabelText('Volver arriba');
        expect(button).toBeInTheDocument();
    });
});
