'use client';

import { useState, useEffect } from 'react';
import { LawHeader } from './LawHeader';
import { TableOfContents } from './TableOfContents';
import { ArticleViewer } from './ArticleViewer';
import type { LawDetailData } from './types';
import { Loader2 } from 'lucide-react';

interface LawDetailProps {
    lawId: string;
}

export function LawDetail({ lawId }: LawDetailProps) {
    const [data, setData] = useState<LawDetailData | null>(null);
    const [activeArticle, setActiveArticle] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function fetchLaw() {
            try {
                setLoading(true);
                // Note: Using the API URL from environment, or defaulting to localhost for dev
                const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

                // Fetch law metadata
                const lawRes = await fetch(`${apiUrl}/api/v1/laws/${lawId}/`);
                if (!lawRes.ok) throw new Error('No se pudo cargar la ley');
                const lawData = await lawRes.json();

                // Fetch articles
                const articlesRes = await fetch(`${apiUrl}/api/v1/laws/${lawId}/articles/`);
                if (!articlesRes.ok) throw new Error('No se pudieron cargar los artículos');
                const articlesData = await articlesRes.json();

                setData({
                    law: lawData.law || lawData, // Handle both structures if API changes
                    version: lawData.version || (lawData.versions && lawData.versions[0]) || {},
                    articles: articlesData.articles || [],
                    total: articlesData.total || 0,
                });

                // Handle hash navigation on load
                if (window.location.hash) {
                    const articleId = window.location.hash.replace('#article-', '');
                    if (articleId) setActiveArticle(articleId);
                }
            } catch (err) {
                console.error('Failed to fetch law:', err);
                setError(err instanceof Error ? err.message : 'Error desconocido');
            } finally {
                setLoading(false);
            }
        }

        fetchLaw();
    }, [lawId]);

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen bg-background gap-4">
                <Loader2 className="h-10 w-10 animate-spin text-primary" />
                <p className="text-muted-foreground">Cargando ley...</p>
            </div>
        );
    }

    if (error || !data) {
        return (
            <div className="container mx-auto px-4 py-12 flex flex-col items-center justify-center text-center">
                <h1 className="text-2xl font-bold mb-2">Error al cargar la ley</h1>
                <p className="text-muted-foreground mb-6">{error || 'No se encontró la información solicitada'}</p>
                <a
                    href="/search"
                    className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
                >
                    Volver al buscador
                </a>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-background flex flex-col">
            <LawHeader law={data.law} version={data.version} />

            <div className="container mx-auto flex flex-col lg:flex-row gap-8 px-4 py-8 flex-1">
                {/* Left sidebar: TOC */}
                <aside className="lg:w-80 flex-shrink-0 lg:sticky lg:top-24 h-fit max-h-[calc(100vh-8rem)]">
                    <div className="bg-card border rounded-lg p-4 h-full shadow-sm overflow-hidden">
                        {/* Mobile: Collapse logic could go here, for now it's always visible but limited height on mobile via CSS could be added */}
                        <div className="h-full overflow-hidden">
                            <TableOfContents
                                articles={data.articles}
                                activeArticle={activeArticle}
                                onArticleClick={(id) => {
                                    setActiveArticle(id);
                                    // Update URL without scroll
                                    window.history.pushState(null, '', `#article-${id}`);
                                }}
                            />
                        </div>
                    </div>
                </aside>

                {/* Main content: Articles */}
                <main className="flex-1 min-w-0">
                    <ArticleViewer
                        articles={data.articles}
                        activeArticle={activeArticle}
                        onArticleChange={setActiveArticle}
                    />
                </main>
            </div>
        </div>
    );
}
