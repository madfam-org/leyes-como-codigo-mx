import type { Metadata } from 'next';

export const metadata: Metadata = {
    title: 'Términos y Condiciones — Tezca',
    description: 'Términos y condiciones de uso de Tezca. Naturaleza del servicio, alcances y limitaciones.',
};

export default function TerminosLayout({ children }: { children: React.ReactNode }) {
    return children;
}
