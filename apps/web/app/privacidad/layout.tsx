import type { Metadata } from 'next';

export const metadata: Metadata = {
    title: 'Política de Privacidad — Tezca',
    description: 'Política de privacidad de Tezca. Información sobre recopilación de datos y derechos del usuario.',
};

export default function PrivacidadLayout({ children }: { children: React.ReactNode }) {
    return children;
}
