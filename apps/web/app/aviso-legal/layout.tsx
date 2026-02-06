import type { Metadata } from 'next';

export const metadata: Metadata = {
    title: 'Aviso Legal — Tezca',
    description: 'Aviso legal de Tezca. Este sitio no es una publicación oficial del gobierno mexicano.',
};

export default function AvisoLegalLayout({ children }: { children: React.ReactNode }) {
    return children;
}
