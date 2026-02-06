import type { Metadata } from 'next';

export const metadata: Metadata = {
    title: 'Acerca de — Tezca',
    description: 'La misión de Tezca: transformar la legislación mexicana en infraestructura digital pública, abierta y computacional.',
};

export default function AcercaDeLayout({ children }: { children: React.ReactNode }) {
    return children;
}
