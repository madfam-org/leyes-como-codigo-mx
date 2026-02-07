import { render, screen } from '@testing-library/react';
import Home from '@/app/page';

vi.mock('next/link', () => ({
    default: ({ href, children, ...props }: { href: string; children: React.ReactNode }) => (
        <a href={href} {...props}>{children}</a>
    ),
}));

vi.mock('@tezca/ui', () => ({
    Card: ({ children, ...props }: React.PropsWithChildren) => <div data-testid="card" {...props}>{children}</div>,
    CardHeader: ({ children, ...props }: React.PropsWithChildren) => <div {...props}>{children}</div>,
    CardTitle: ({ children, ...props }: React.PropsWithChildren) => <h3 {...props}>{children}</h3>,
    CardDescription: ({ children, ...props }: React.PropsWithChildren) => <p {...props}>{children}</p>,
    CardContent: ({ children, ...props }: React.PropsWithChildren) => <div {...props}>{children}</div>,
}));

describe('Home page', () => {
    it('renders all 5 navigation cards', () => {
        render(<Home />);
        const cards = screen.getAllByTestId('card');
        expect(cards).toHaveLength(5);
    });

    it('renders card titles in Spanish', () => {
        render(<Home />);
        expect(screen.getByText('Ingestión y Scraping')).toBeInTheDocument();
        expect(screen.getByText('Métricas')).toBeInTheDocument();
        expect(screen.getByText('DataOps')).toBeInTheDocument();
        expect(screen.getByText('Roadmap')).toBeInTheDocument();
        expect(screen.getByText('Configuración')).toBeInTheDocument();
    });

    it('links to correct routes', () => {
        render(<Home />);
        const links = screen.getAllByRole('link');
        const hrefs = links.map(l => l.getAttribute('href'));
        expect(hrefs).toContain('/ingestion');
        expect(hrefs).toContain('/metrics');
        expect(hrefs).toContain('/dataops');
        expect(hrefs).toContain('/roadmap');
        expect(hrefs).toContain('/settings');
    });

    it('renders card descriptions', () => {
        render(<Home />);
        expect(screen.getByText(/Gestionar fuentes de datos/)).toBeInTheDocument();
        expect(screen.getByText(/Estadísticas del sistema/)).toBeInTheDocument();
        expect(screen.getByText(/Cobertura de datos/)).toBeInTheDocument();
        expect(screen.getByText(/Plan de expansión/)).toBeInTheDocument();
        expect(screen.getByText(/Estado de servicios/)).toBeInTheDocument();
    });
});
