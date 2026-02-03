import { LawDetail } from '@/components/laws/LawDetail';

export default function LawDetailPage({
    params
}: {
    params: { id: string }
}) {
    // Decode ID in case it comes encoded
    const decodedId = decodeURIComponent(params.id);

    return <LawDetail lawId={decodedId} />;
}
