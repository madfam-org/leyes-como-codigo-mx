import { LawDetail } from '@/components/laws/LawDetail';
import { Metadata } from 'next';
import { API_BASE_URL } from '@/lib/config';

/**
 * Generate dynamic metadata for law pages with Open Graph support.
 * Enables rich previews when sharing law/article links on social media.
 */
export async function generateMetadata({
    params,
}: {
    params: Promise<{ id: string }>
}): Promise<Metadata> {
    const { id } = await params;
    const lawId = decodeURIComponent(id);
    const apiUrl = API_BASE_URL;
    const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://tezca.mx';

    try {
        const lawRes = await fetch(`${apiUrl}/laws/${lawId}/`, {
            next: { revalidate: 3600 }
        });

        if (!lawRes.ok) {
            return {
                title: 'Ley no encontrada — Tezca',
                description: 'La ley solicitada no está disponible.'
            };
        }

        const lawData = await lawRes.json();
        const law = lawData.law || lawData;

        const tierLabel = law.tier === 'state' ? 'Estatal' : law.tier === 'municipal' ? 'Municipal' : 'Federal';
        const description = `${law.name} — ${tierLabel}${law.category ? ` · ${law.category}` : ''}. Texto completo en formato digital.`;

        return {
            title: `${law.name || law.official_id} — Tezca`,
            description,
            openGraph: {
                title: law.name || law.official_id,
                description,
                type: 'article',
                url: `${siteUrl}/laws/${lawId}`,
                siteName: 'Tezca',
            },
            twitter: {
                card: 'summary_large_image',
                title: law.name || law.official_id,
                description,
            }
        };

    } catch (error) {
        console.error('Failed to generate metadata:', error);
        return {
            title: 'Tezca — El Espejo de la Ley',
            description: 'Legislación mexicana digitalizada y accesible'
        };
    }
}

export default async function LawDetailPage({
    params
}: {
    params: Promise<{ id: string }>
}) {
    // Decode ID in case it comes encoded
    const { id } = await params;
    const decodedId = decodeURIComponent(id);

    return <LawDetail lawId={decodedId} />;
}
