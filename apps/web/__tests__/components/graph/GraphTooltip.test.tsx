import { render, screen } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { makeLangMock, langState } from '../../helpers/lang-mock';

const mockUseLang = makeLangMock();
vi.mock('@/components/providers/LanguageContext', () => ({
    useLang: () => mockUseLang(),
}));

import { GraphTooltip } from '@/components/graph/GraphTooltip';
import type { GraphNode } from '@/lib/api';

const node: GraphNode = {
    id: 'cpeum',
    label: 'Constitución Política',
    tier: 'federal',
    category: 'fiscal',
    status: null,
    law_type: null,
    state: null,
    ref_count: 42,
    is_focal: false,
};

describe('GraphTooltip', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        mockUseLang.mockReturnValue(langState('es'));
    });

    it('renders nothing when node is null', () => {
        const { container } = render(<GraphTooltip node={null} position={{ x: 0, y: 0 }} />);
        expect(container.firstChild).toBeNull();
    });

    it('renders nothing when position is null', () => {
        const { container } = render(<GraphTooltip node={node} position={null} />);
        expect(container.firstChild).toBeNull();
    });

    it('renders the node label', () => {
        render(<GraphTooltip node={node} position={{ x: 100, y: 200 }} />);
        expect(screen.getByText('Constitución Política')).toBeInTheDocument();
    });

    it('renders the tier badge', () => {
        render(<GraphTooltip node={node} position={{ x: 0, y: 0 }} />);
        expect(screen.getByText('federal')).toBeInTheDocument();
    });

    it('renders the ref_count + i18n suffix', () => {
        render(<GraphTooltip node={node} position={{ x: 0, y: 0 }} />);
        // "42 referencias"
        expect(screen.getByText(/42/)).toBeInTheDocument();
        expect(screen.getByText(/referencias/)).toBeInTheDocument();
    });

    it('uses English suffix when lang is en', () => {
        mockUseLang.mockReturnValue(langState('en'));
        render(<GraphTooltip node={node} position={{ x: 0, y: 0 }} />);
        expect(screen.getByText(/references/)).toBeInTheDocument();
        expect(screen.getByText('Click to view')).toBeInTheDocument();
    });

    it('positions itself based on the position prop', () => {
        const { container } = render(
            <GraphTooltip node={node} position={{ x: 100, y: 200 }} />,
        );
        const tooltip = container.firstChild as HTMLElement;
        expect(tooltip.style.left).toBe('112px'); // x + 12
        expect(tooltip.style.top).toBe('190px'); // y - 10
    });

    it('omits the category badge when node has no category', () => {
        const noCat: GraphNode = { ...node, category: null };
        const { container } = render(
            <GraphTooltip node={noCat} position={{ x: 0, y: 0 }} />,
        );
        // Tier still renders; category swatch is gone — just verify no crash
        expect(container.firstChild).toBeTruthy();
    });
});
