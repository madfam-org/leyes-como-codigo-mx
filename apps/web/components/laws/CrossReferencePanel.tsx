'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { ExternalLink, ChevronDown, ChevronUp } from 'lucide-react';
import { Badge } from '@tezca/ui';
import { useLang } from '@/components/providers/LanguageContext';
import { API_BASE_URL } from '@/lib/config';

const content = {
    es: {
        title: 'Referencias Cruzadas',
        outgoing: 'Leyes referenciadas',
        incoming: 'Leyes que citan esta',
        totalOutgoing: 'Referencias salientes',
        totalIncoming: 'Citas recibidas',
        noRefs: 'No se detectaron referencias cruzadas para esta ley.',
        showMore: 'Ver todas',
        showLess: 'Ver menos',
        times: 'veces',
        loading: 'Cargando referencias...',
    },
    en: {
        title: 'Cross-References',
        outgoing: 'Referenced laws',
        incoming: 'Laws citing this',
        totalOutgoing: 'Outgoing references',
        totalIncoming: 'Citations received',
        noRefs: 'No cross-references detected for this law.',
        showMore: 'Show all',
        showLess: 'Show less',
        times: 'times',
        loading: 'Loading references...',
    },
    nah: {
        title: 'Tlanōnōtzaliztli Nepantlah',
        outgoing: 'Tenahuatilli tlanōnōtzalli',
        incoming: 'Tenahuatilli tlanōnōtzanih',
        totalOutgoing: 'Tlanōnōtzaliztli quīzanih',
        totalIncoming: 'Tlanōnōtzaliztli ahcih',
        noRefs: 'Ahmo monextia tlanōnōtzaliztli inīn tenahuatilli.',
        showMore: 'Xicnextia mochi',
        showLess: 'Xicnextia ahmo miec',
        times: 'quēzquipa',
        loading: 'Tlanōnōtzaliztli motēmoa...',
    },
};

interface RefLaw {
    slug: string;
    count: number;
}

interface RefStats {
    total_outgoing: number;
    total_incoming: number;
    most_referenced_laws: RefLaw[];
    most_citing_laws: RefLaw[];
}

interface CrossReferencePanelProps {
    lawId: string;
}

export function CrossReferencePanel({ lawId }: CrossReferencePanelProps) {
    const { lang } = useLang();
    const t = content[lang];
    const [stats, setStats] = useState<RefStats | null>(null);
    const [loading, setLoading] = useState(true);
    const [expanded, setExpanded] = useState(false);

    useEffect(() => {
        fetch(`${API_BASE_URL}/laws/${lawId}/references/`)
            .then(r => r.ok ? r.json() : null)
            .then(data => {
                if (data?.statistics) setStats(data.statistics);
                setLoading(false);
            })
            .catch(() => setLoading(false));
    }, [lawId]);

    if (loading) {
        return (
            <div className="mt-8 p-4 border rounded-lg bg-card animate-pulse">
                <div className="h-5 w-48 bg-muted rounded" />
                <div className="mt-3 h-4 w-32 bg-muted rounded" />
            </div>
        );
    }

    if (!stats || (stats.total_outgoing === 0 && stats.total_incoming === 0)) {
        return null;
    }

    const totalRefs = stats.total_outgoing + stats.total_incoming;
    const previewLimit = 5;
    const hasMoreOutgoing = stats.most_referenced_laws.length > previewLimit;
    const hasMoreIncoming = stats.most_citing_laws.length > previewLimit;
    const showExpand = hasMoreOutgoing || hasMoreIncoming;

    const outgoingList = expanded
        ? stats.most_referenced_laws
        : stats.most_referenced_laws.slice(0, previewLimit);
    const incomingList = expanded
        ? stats.most_citing_laws
        : stats.most_citing_laws.slice(0, previewLimit);

    return (
        <section
            className="mt-8 border rounded-lg bg-card shadow-sm"
            aria-label={t.title}
        >
            <div className="p-4 sm:p-6">
                <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-bold tracking-tight flex items-center gap-2">
                        <ExternalLink className="h-5 w-5 text-primary" />
                        {t.title}
                    </h2>
                    <div className="flex gap-2">
                        <Badge variant="secondary" className="text-xs">
                            {stats.total_outgoing} {t.totalOutgoing.toLowerCase()}
                        </Badge>
                        <Badge variant="outline" className="text-xs">
                            {stats.total_incoming} {t.totalIncoming.toLowerCase()}
                        </Badge>
                    </div>
                </div>

                <div className="grid gap-6 md:grid-cols-2">
                    {/* Outgoing: laws this law references */}
                    {outgoingList.length > 0 && (
                        <div>
                            <h3 className="text-sm font-semibold text-muted-foreground mb-2">
                                {t.outgoing}
                            </h3>
                            <ul className="space-y-1.5">
                                {outgoingList.map(ref => (
                                    <li key={ref.slug}>
                                        <Link
                                            href={`/leyes/${ref.slug}`}
                                            className="flex items-center justify-between text-sm hover:text-primary transition-colors group"
                                        >
                                            <span className="truncate group-hover:underline">
                                                {ref.slug}
                                            </span>
                                            <span className="text-xs text-muted-foreground flex-shrink-0 ml-2">
                                                {ref.count} {t.times}
                                            </span>
                                        </Link>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}

                    {/* Incoming: laws that cite this law */}
                    {incomingList.length > 0 && (
                        <div>
                            <h3 className="text-sm font-semibold text-muted-foreground mb-2">
                                {t.incoming}
                            </h3>
                            <ul className="space-y-1.5">
                                {incomingList.map(ref => (
                                    <li key={ref.slug}>
                                        <Link
                                            href={`/leyes/${ref.slug}`}
                                            className="flex items-center justify-between text-sm hover:text-primary transition-colors group"
                                        >
                                            <span className="truncate group-hover:underline">
                                                {ref.slug}
                                            </span>
                                            <span className="text-xs text-muted-foreground flex-shrink-0 ml-2">
                                                {ref.count} {t.times}
                                            </span>
                                        </Link>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>

                {showExpand && (
                    <button
                        onClick={() => setExpanded(!expanded)}
                        className="mt-4 flex items-center gap-1 text-sm text-primary hover:underline"
                    >
                        {expanded ? (
                            <>
                                <ChevronUp className="h-4 w-4" />
                                {t.showLess}
                            </>
                        ) : (
                            <>
                                <ChevronDown className="h-4 w-4" />
                                {t.showMore} ({totalRefs})
                            </>
                        )}
                    </button>
                )}
            </div>
        </section>
    );
}
