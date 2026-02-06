import { render, screen, fireEvent, act } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';

vi.mock('@/components/providers/LanguageContext', () => ({
    useLang: vi.fn(() => ({ lang: 'es', setLang: vi.fn() })),
}));

import { ShareButtons } from '@/components/ShareButtons';

describe('ShareButtons', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        Object.assign(navigator, {
            clipboard: {
                writeText: vi.fn().mockResolvedValue(undefined),
            },
        });
    });

    it('renders Twitter/X share link', () => {
        render(<ShareButtons title="Test Law" />);
        const twitterLink = screen.getByTitle('Twitter / X');
        expect(twitterLink).toBeInTheDocument();
        expect(twitterLink).toHaveAttribute('href', expect.stringContaining('twitter.com/intent/tweet'));
        expect(twitterLink).toHaveAttribute('target', '_blank');
        expect(twitterLink).toHaveAttribute('rel', 'noopener noreferrer');
    });

    it('renders LinkedIn share link', () => {
        render(<ShareButtons title="Test Law" />);
        const linkedinLink = screen.getByTitle('LinkedIn');
        expect(linkedinLink).toBeInTheDocument();
        expect(linkedinLink).toHaveAttribute('href', expect.stringContaining('linkedin.com/sharing'));
        expect(linkedinLink).toHaveAttribute('target', '_blank');
    });

    it('renders WhatsApp share link', () => {
        render(<ShareButtons title="Test Law" />);
        const whatsappLink = screen.getByTitle('WhatsApp');
        expect(whatsappLink).toBeInTheDocument();
        expect(whatsappLink).toHaveAttribute('href', expect.stringContaining('wa.me'));
        expect(whatsappLink).toHaveAttribute('target', '_blank');
    });

    it('renders copy link button with correct title', () => {
        render(<ShareButtons title="Test Law" />);
        const copyBtn = screen.getByTitle('Copiar enlace');
        expect(copyBtn).toBeInTheDocument();
    });

    it('calls navigator.clipboard.writeText on copy click', async () => {
        render(<ShareButtons title="Test Law" />);
        const copyBtn = screen.getByTitle('Copiar enlace');

        await act(async () => {
            fireEvent.click(copyBtn);
        });

        expect(navigator.clipboard.writeText).toHaveBeenCalled();
    });

    it('shows "Copiado!" text after copy click', async () => {
        render(<ShareButtons title="Test Law" />);
        const copyBtn = screen.getByTitle('Copiar enlace');

        await act(async () => {
            fireEvent.click(copyBtn);
        });

        expect(screen.getByText('Copiado!')).toBeInTheDocument();
    });

    it('encodes title in share URLs', () => {
        render(<ShareButtons title="Ley de Amparo" />);
        const twitterLink = screen.getByTitle('Twitter / X');
        expect(twitterLink.getAttribute('href')).toContain('Ley%20de%20Amparo');
    });

    it('applies custom className', () => {
        const { container } = render(<ShareButtons title="Test" className="my-custom-class" />);
        expect(container.firstChild).toHaveClass('my-custom-class');
    });
});
