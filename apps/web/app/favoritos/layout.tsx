import type { Metadata } from 'next';

export const metadata: Metadata = {
    title: 'Favoritos — Tezca',
    description: 'Tus leyes guardadas en Tezca. Accede rapidamente a la legislacion que consultas con frecuencia.',
};

export default function FavoritosLayout({ children }: { children: React.ReactNode }) {
    return children;
}
