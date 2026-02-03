'use client';

import { useState, useEffect } from 'react';
import { Search as SearchIcon, Loader2 } from 'lucide-react';
import { useSearchParams, useRouter } from 'next/navigation';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { api } from '@/lib/api';
import type { SearchResult } from '@/lib/types';

export default function SearchPage() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const initialQuery = searchParams?.get('q') || '';

    const [query, setQuery] = useState(initialQuery);
    const [results, setResults] = useState<SearchResult[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (initialQuery) {
            performSearch(initialQuery);
        }
    }, [initialQuery]);

    const performSearch = async (searchQuery: string) => {
        if (!searchQuery.trim()) {
            setResults([]);
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const data = await api.search(searchQuery);
            setResults(data.results || []);

            if (data.warning) {
                setError(data.warning);
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Error al buscar');
            setResults([]);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (query.trim()) {
            router.push(`/search?q=${encodeURIComponent(query)}`);
            performSearch(query);
        }
    };

    return (
        <div className="min-h-screen bg-background">
            {/* Search Header */}
            <div className="border-b border-border bg-card">
                <div className="mx-auto max-w-4xl px-6 py-8">
                    <h1 className="mb-6 font-display text-3xl font-bold text-foreground">
                        Buscar Leyes
                    </h1>

                    <form onSubmit={handleSubmit}>
                        <div className="relative flex items-center gap-2 rounded-lg bg-background p-2 shadow-md ring-1 ring-border">
                            <SearchIcon className="ml-2 h-5 w-5 text-muted-foreground" />
                            <Input
                                type="text"
                                value={query}
                                onChange={(e) => setQuery(e.target.value)}
                                placeholder="Buscar en 330 leyes federales..."
                                className="flex-1 border-0 bg-transparent text-base focus-visible:outline-none focus-visible:ring-0"
                                autoFocus
                            />
                            <Button type="submit" disabled={loading}>
                                {loading ? (
                                    <>
                                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                        Buscando...
                                    </>
                                ) : (
                                    'Buscar'
                                )}
                            </Button>
                        </div>
                    </form>
                </div>
            </div>

            {/* Results */}
            <div className="mx-auto max-w-4xl px-6 py-8">
                {error && (
                    <div className="mb-6 rounded-lg bg-error-50 p-4 text-error-700 dark:bg-error-900 dark:text-error-100">
                        ⚠️ {error}
                    </div>
                )}

                {loading && (
                    <div className="flex items-center justify-center py-16">
                        <Loader2 className="h-8 w-8 animate-spin text-primary-500" />
                    </div>
                )}

                {!loading && results.length === 0 && initialQuery && (
                    <div className="py-16 text-center">
                        <p className="text-lg text-muted-foreground">
                            No se encontraron resultados para "{initialQuery}"
                        </p>
                        <p className="mt-2 text-sm text-muted-foreground">
                            Intenta con otros términos de búsqueda
                        </p>
                    </div>
                )}

                {!loading && results.length === 0 && !initialQuery && (
                    <div className="py-16 text-center">
                        <p className="text-lg text-muted-foreground">
                            Ingresa un término de búsqueda para comenzar
                        </p>
                    </div>
                )}

                {!loading && results.length > 0 && (
                    <>
                        <div className="mb-6 text-sm text-muted-foreground">
                            {results.length} resultado{results.length !== 1 ? 's' : ''} para "{initialQuery}"
                        </div>

                        <div className="space-y-4">
                            {results.map((result, index) => (
                                <Card key={result.id || index} className="transition-all hover:shadow-lg">
                                    <CardContent className="p-6">
                                        <div className="flex items-start justify-between gap-4">
                                            {/* Content */}
                                            <div className="flex-1">
                                                <div className="mb-2 flex items-center gap-2">
                                                    <Badge variant="secondary" className="font-mono text-xs">
                                                        {result.law.toUpperCase()}
                                                    </Badge>
                                                    {result.article && (
                                                        <span className="text-sm text-muted-foreground">
                                                            {result.article}
                                                        </span>
                                                    )}
                                                </div>

                                                <div
                                                    className="text-sm text-foreground"
                                                    dangerouslySetInnerHTML={{ __html: result.snippet }}
                                                />

                                                {result.date && (
                                                    <div className="mt-3 text-xs text-muted-foreground">
                                                        Publicación: {new Date(result.date).toLocaleDateString('es-MX')}
                                                    </div>
                                                )}
                                            </div>

                                            {/* Score */}
                                            {result.score && (
                                                <div className="text-right">
                                                    <div className="text-xs text-muted-foreground">Relevancia</div>
                                                    <div className="font-display text-lg font-bold text-primary-600">
                                                        {result.score.toFixed(1)}
                                                    </div>
                                                </div>
                                            )}
                                        </div>
                                    </CardContent>
                                </Card>
                            ))}
                        </div>
                    </>
                )}
            </div>
        </div>
    );
}
