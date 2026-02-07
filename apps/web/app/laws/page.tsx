'use client';

import { useEffect, useState, useCallback } from 'react';
import type { LawListItem } from '@tezca/lib';
import LawCard from '@/components/LawCard';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import { api } from '@/lib/api';
import { useLang } from '@/components/providers/LanguageContext';

const content = {
    es: {
        subtitle: 'Explora la legislaci\u00f3n mexicana',
        home: '\u2190 Inicio',
        lawsAvailable: 'Leyes Disponibles',
        browseLaws: 'Leyes',
        loading: 'Cargando leyes...',
        loadError: 'No se pudieron cargar las leyes. Intenta de nuevo.',
        retry: 'Reintentar',
        noLaws: 'No se encontraron leyes.',
        compareHint: 'Selecciona leyes con \u2611 para comparar',
    },
    en: {
        subtitle: 'Explore Mexican legislation',
        home: '\u2190 Home',
        lawsAvailable: 'Laws Available',
        browseLaws: 'Laws',
        loading: 'Loading laws...',
        loadError: 'Could not load laws. Please try again.',
        retry: 'Retry',
        noLaws: 'No laws found.',
        compareHint: 'Select laws with \u2611 to compare',
    },
    nah: {
        subtitle: 'Xictlachia in m\u0113xihcatl tenahuatilli',
        home: '\u2190 Caltenco',
        lawsAvailable: 'Tenahuatilli Oncah',
        browseLaws: 'Tenahuatilli',
        loading: 'Mot\u0113moa tenahuatilli...',
        loadError: 'Ahmo huel\u012Bz mot\u0113moa tenahuatilli. Xicy\u0113yec\u014Dlti occ\u0113ppa.',
        retry: 'Occ\u0113ppa',
        noLaws: 'Ahmo oncah tenahuatilli.',
        compareHint: 'Xictlap\u0113peni tenahuatilli ic \u2611 ic motlan\u0101namiqui',
    },
};

export default function LawsPage() {
    const { lang } = useLang();
    const t = content[lang];
    const searchParams = useSearchParams();
    const jurisdictionParam = searchParams.get('jurisdiction');

    const [laws, setLaws] = useState<LawListItem[]>([]);
    const [totalCount, setTotalCount] = useState(0);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);

    const fetchLaws = useCallback(async () => {
        setLoading(true);
        setError(false);
        try {
            const data = await api.getLaws({
                page_size: 50,
                tier: jurisdictionParam || undefined,
            });
            setLaws(data.results);
            setTotalCount(data.count);
        } catch {
            setError(true);
        } finally {
            setLoading(false);
        }
    }, [jurisdictionParam]);

    useEffect(() => {
        fetchLaws();
    }, [fetchLaws]);

    return (
        <div className="min-h-screen bg-background">
            {/* Header */}
            <div className="bg-primary text-primary-foreground shadow-xl">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                    <div className="flex justify-between items-start">
                        <div>
                            <h1 className="text-4xl font-bold mb-2">
                                Tezca
                            </h1>
                            <p className="text-xl opacity-80">
                                {t.subtitle}
                            </p>
                        </div>
                        <Link
                            href="/"
                            className="bg-primary-foreground/10 hover:bg-primary-foreground/20 px-4 py-2 rounded-lg transition-colors duration-200"
                        >
                            {t.home}
                        </Link>
                    </div>
                </div>
            </div>

            {/* Content */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {loading ? (
                    <div className="text-center py-16">
                        <div className="animate-pulse space-y-4">
                            <div className="h-8 bg-muted rounded w-48 mx-auto" />
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                {[...Array(6)].map((_, i) => (
                                    <div key={i} className="h-48 rounded-xl bg-muted" />
                                ))}
                            </div>
                        </div>
                        <p className="text-muted-foreground mt-4">{t.loading}</p>
                    </div>
                ) : error ? (
                    <div className="text-center py-16">
                        <p className="text-destructive mb-4">{t.loadError}</p>
                        <button
                            onClick={fetchLaws}
                            className="px-4 py-2 rounded-lg bg-primary text-primary-foreground hover:bg-primary/90 transition-colors"
                        >
                            {t.retry}
                        </button>
                    </div>
                ) : (
                    <>
                        {/* Stats bar */}
                        <div className="mb-8">
                            <div className="flex items-center justify-between mb-6">
                                <h2 className="text-2xl font-bold text-foreground">
                                    {t.browseLaws}
                                    <span className="ml-3 text-lg font-normal text-muted-foreground">
                                        {totalCount} {t.lawsAvailable.toLowerCase()}
                                    </span>
                                </h2>
                                <p className="text-sm text-muted-foreground hidden sm:block">
                                    {t.compareHint}
                                </p>
                            </div>

                            {laws.length === 0 ? (
                                <p className="text-center text-muted-foreground py-12">{t.noLaws}</p>
                            ) : (
                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                    {laws.map((law) => (
                                        <LawCard key={law.id} law={law as never} />
                                    ))}
                                </div>
                            )}
                        </div>
                    </>
                )}
            </div>
        </div>
    );
}
