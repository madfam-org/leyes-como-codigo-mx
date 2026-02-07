'use client';

import { useEffect, useState } from 'react';
import { Card, Input } from '@tezca/ui';
import { useLang } from '@/components/providers/LanguageContext';

const content = {
    es: {
        loading: 'Cargando artículos...',
        loadError: 'Error al cargar los artículos. Por favor, intenta de nuevo.',
        searchPlaceholder: 'Buscar en artículos...',
        viewArticles: 'Ver Artículos',
        viewTransitorios: (n: number) => `Ver Transitorios (${n})`,
        resultsFound: (n: number) => `${n} resultado${n !== 1 ? 's' : ''} encontrado${n !== 1 ? 's' : ''}`,
        noResults: 'No se encontraron artículos que coincidan con tu búsqueda.',
        contentUnavailable: 'Contenido no disponible',
    },
    en: {
        loading: 'Loading articles...',
        loadError: 'Error loading articles. Please try again.',
        searchPlaceholder: 'Search articles...',
        viewArticles: 'View Articles',
        viewTransitorios: (n: number) => `View Transitory Articles (${n})`,
        resultsFound: (n: number) => `${n} result${n !== 1 ? 's' : ''} found`,
        noResults: 'No articles matched your search.',
        contentUnavailable: 'Content not available',
    },
    nah: {
        loading: 'Motēmoa tlanahuatilli...',
        loadError: 'Tlahtlacōlli ic motēmoa tlanahuatilli. Xicyēyecōlti occēppa.',
        searchPlaceholder: 'Xictēmoa tlanahuatilli...',
        viewArticles: 'Xiquitta Tlanahuatilli',
        viewTransitorios: (n: number) => `Xiquitta Transitorios (${n})`,
        resultsFound: (n: number) => `${n} tlanextīliztli`,
        noResults: 'Ahmo oncah tlanahuatilli ic motlatemoliztli.',
        contentUnavailable: 'Tlamachiliztli ahmo oncah',
    },
};

interface Article {
    id: string;
    number: string;
    content: string;
    type: 'article' | 'transitorio';
}

interface LawData {
    law_id: string;
    articles: Article[];
    total_articles: number;
    total_transitorios: number;
}

interface LawArticlesProps {
    lawId: string;
}

export default function LawArticles({ lawId }: LawArticlesProps) {
    const { lang } = useLang();
    const t = content[lang];
    const [lawData, setLawData] = useState<LawData | null>(null);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');
    const [showTransitorios, setShowTransitorios] = useState(false);

    useEffect(() => {
        async function loadLawData() {
            try {
                const response = await fetch(`/viewer_data/${lawId}.json`);
                if (!response.ok) throw new Error('Failed to load law data');
                const data = await response.json();
                setLawData(data);
            } catch (error) {
                console.error('Error loading law data:', error);
            } finally {
                setLoading(false);
            }
        }

        loadLawData();
    }, [lawId]);

    if (loading) {
        return (
            <Card className="p-8 text-center">
                <div className="animate-pulse">
                    <div className="h-4 bg-muted rounded w-3/4 mx-auto mb-4"></div>
                    <div className="h-4 bg-muted rounded w-1/2 mx-auto"></div>
                </div>
                <p className="text-muted-foreground mt-4">
                    {t.loading}
                </p>
            </Card>
        );
    }

    if (!lawData) {
        return (
            <Card className="p-8 text-center bg-destructive/10">
                <p className="text-destructive">
                    {t.loadError}
                </p>
            </Card>
        );
    }

    const regularArticles = lawData.articles.filter(a => a.type === 'article');
    const transitorios = lawData.articles.filter(a => a.type === 'transitorio');

    const filteredArticles = (showTransitorios ? transitorios : regularArticles).filter(article => {
        if (!searchQuery) return true;
        const query = searchQuery.toLowerCase();
        return (
            article.number.toLowerCase().includes(query) ||
            article.content.toLowerCase().includes(query)
        );
    });

    return (
        <div>
            {/* Search and Filters */}
            <Card className="p-6 mb-6">
                <div className="flex flex-col md:flex-row gap-4">
                    <div className="flex-1">
                        <Input
                            type="text"
                            placeholder={`🔍 ${t.searchPlaceholder}`}
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="w-full"
                        />
                    </div>

                    {transitorios.length > 0 && (
                        <button
                            onClick={() => setShowTransitorios(!showTransitorios)}
                            className={`px-4 py-2 rounded-lg font-medium transition-colors ${showTransitorios
                                    ? 'bg-primary text-primary-foreground'
                                    : 'bg-muted text-muted-foreground hover:text-foreground'
                                }`}
                        >
                            {showTransitorios ? t.viewArticles : t.viewTransitorios(transitorios.length)}
                        </button>
                    )}
                </div>

                {searchQuery && (
                    <div className="mt-3 text-sm text-muted-foreground">
                        {t.resultsFound(filteredArticles.length)}
                    </div>
                )}
            </Card>

            {/* Articles List */}
            <div className="space-y-4">
                {filteredArticles.length === 0 ? (
                    <Card className="p-8 text-center glass border-dashed">
                        <p className="text-muted-foreground">
                            {t.noResults}
                        </p>
                    </Card>
                ) : (
                    filteredArticles.map((article, index) => (
                        <Card key={article.id} className="p-6 hover:shadow-lg transition-all duration-300 glass border-transparent hover:border-primary/20">
                            <div className="flex gap-4">
                                <div className="flex-shrink-0">
                                    <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center shadow-inner">
                                        <span className="text-primary font-bold font-display text-sm">
                                            {index + 1}
                                        </span>
                                    </div>
                                </div>

                                <div className="flex-1 min-w-0">
                                    <h3 className="text-lg font-bold font-display text-primary mb-3">
                                        {article.number}
                                    </h3>

                                    {article.content ? (
                                        <div className="text-foreground leading-relaxed whitespace-pre-wrap font-serif">
                                            {searchQuery ? (
                                                <HighlightedText text={article.content} query={searchQuery} />
                                            ) : (
                                                article.content
                                            )}
                                        </div>
                                    ) : (
                                        <p className="text-muted-foreground italic">
                                            {t.contentUnavailable}
                                        </p>
                                    )}
                                </div>
                            </div>
                        </Card>
                    ))
                )}
            </div>
        </div>
    );
}

function HighlightedText({ text, query }: { text: string; query: string }) {
    if (!query) return <>{text}</>;

    const escaped = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const parts = text.split(new RegExp(`(${escaped})`, 'gi'));

    return (
        <>
            {parts.map((part, i) => (
                part.toLowerCase() === query.toLowerCase() ? (
                    <mark key={i} className="bg-accent text-accent-foreground">
                        {part}
                    </mark>
                ) : (
                    <span key={i}>{part}</span>
                )
            ))}
        </>
    );
}
