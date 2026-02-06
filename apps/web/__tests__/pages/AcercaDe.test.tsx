import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import AcercaDePage from '@/app/acerca-de/page';
import { LanguageProvider } from '@/components/providers/LanguageContext';

function renderPage() {
  return render(
    <LanguageProvider>
      <AcercaDePage />
    </LanguageProvider>
  );
}

describe('AcercaDe (Manifesto Page)', () => {
  it('renders "Tezca" title in hero section', () => {
    renderPage();
    expect(screen.getByRole('heading', { level: 1, name: 'Tezca' })).toBeInTheDocument();
  });

  it('renders subtitle "El Espejo de la Ley" in Spanish by default', () => {
    renderPage();
    expect(screen.getByText('El Espejo de la Ley')).toBeInTheDocument();
  });

  it('renders all five manifesto sections with Roman numerals', () => {
    renderPage();
    const numerals = ['I', 'II', 'III', 'IV', 'V'];
    numerals.forEach((numeral) => {
      expect(screen.getByText(numeral)).toBeInTheDocument();
    });
  });

  it('renders all five section titles in Spanish by default', () => {
    renderPage();
    expect(screen.getByText('La Sombra')).toBeInTheDocument();
    expect(screen.getByText('El Tezcatl')).toBeInTheDocument();
    expect(screen.getByText('La Transformación')).toBeInTheDocument();
    expect(screen.getByText('Infraestructura, no Especulación')).toBeInTheDocument();
    expect(screen.getByText('El Futuro')).toBeInTheDocument();
  });

  it('renders closing CTA "Bienvenido a Tezca"', () => {
    renderPage();
    expect(screen.getByText('Bienvenido a Tezca')).toBeInTheDocument();
  });

  it('switches to English content when language toggle is clicked', () => {
    renderPage();
    const enButton = screen.getByRole('button', { name: 'Switch to English' });
    fireEvent.click(enButton);

    expect(screen.getByText('The Mirror of the Law')).toBeInTheDocument();
    expect(screen.getByText('The Shadow')).toBeInTheDocument();
    expect(screen.getByText('The Tezcatl')).toBeInTheDocument();
    expect(screen.getByText('The Transformation')).toBeInTheDocument();
    expect(screen.getByText('Infrastructure, not Speculation')).toBeInTheDocument();
    expect(screen.getByText('The Future')).toBeInTheDocument();
    expect(screen.getByText('Welcome to Tezca')).toBeInTheDocument();
  });

  it('has a link back to home', () => {
    renderPage();
    const backLink = screen.getByRole('link', { name: /Volver al inicio|Back to home/ });
    expect(backLink).toHaveAttribute('href', '/');
  });
});
