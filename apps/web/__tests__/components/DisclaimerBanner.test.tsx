import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { DisclaimerBanner } from '@/components/DisclaimerBanner';
import { LanguageProvider } from '@/components/providers/LanguageContext';

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

function renderBanner() {
  return render(
    <LanguageProvider>
      <DisclaimerBanner />
    </LanguageProvider>
  );
}

describe('DisclaimerBanner', () => {
  beforeEach(() => {
    localStorageMock.clear();
    vi.clearAllMocks();
  });

  it('is hidden when localStorage has disclaimer-dismissed set', () => {
    localStorageMock.setItem('disclaimer-dismissed', '1');
    renderBanner();
    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
  });

  it('is visible when localStorage is empty', async () => {
    renderBanner();
    // useEffect sets visible=true after mount
    const alert = await screen.findByRole('alert');
    expect(alert).toBeInTheDocument();
  });

  it('dismiss button stores value and hides banner', async () => {
    renderBanner();
    const alert = await screen.findByRole('alert');
    expect(alert).toBeInTheDocument();

    const dismissBtn = screen.getByLabelText('Cerrar aviso');
    fireEvent.click(dismissBtn);

    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
    expect(localStorageMock.setItem).toHaveBeenCalledWith('disclaimer-dismissed', '1');
  });

  it('contains link to /aviso-legal', async () => {
    renderBanner();
    await screen.findByRole('alert');
    const link = screen.getByRole('link', { name: 'Leer más' });
    expect(link).toHaveAttribute('href', '/aviso-legal');
  });

  it('has role="alert" for accessibility', async () => {
    renderBanner();
    const alert = await screen.findByRole('alert');
    expect(alert).toBeInTheDocument();
  });
});
