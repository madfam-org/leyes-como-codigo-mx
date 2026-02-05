
'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { LawArticleResponse } from "@leyesmx/lib";
import { Card, Badge, Button } from "@leyesmx/ui";
import Link from 'next/link';
import { ArrowLeft, Loader2, Map } from 'lucide-react';

interface ComparisonViewProps {
    lawIds: string[];
}

interface LawStructureNode {
    label: string;
    children: LawStructureNode[];
}

interface LawData {
    details: LawArticleResponse;
    structure: LawStructureNode[];
}

export default function ComparisonView({ lawIds }: ComparisonViewProps) {
    const [data, setData] = useState<LawData[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // Initial load
    useEffect(() => {
        async function fetchData() {
            if (lawIds.length < 2) {
                setLoading(false); 
                return;
            }

            try {
                setLoading(true);
                const promises = lawIds.map(async (id) => {
                    const [articles, structureData] = await Promise.all([
                        api.getLawArticles(id),
                        api.getLawStructure(id)
                    ]);
                    return {
                        details: articles,
                        structure: structureData.structure
                    };
                });

                const results = await Promise.all(promises);
                setData(results);
            } catch (err) {
                console.error("Comparison fetch error", err);
                setError("No se pudieron cargar las leyes.");
            } finally {
                setLoading(false);
            }
        }
        fetchData();
    }, [lawIds]);

    if (loading) {
        return (
            <div className="flex h-[80vh] items-center justify-center flex-col">
                <Loader2 className="h-10 w-10 animate-spin text-primary mb-4" />
                <h2 className="text-xl font-medium">Analizando estructura legal...</h2>
                <p className="text-muted-foreground text-sm mt-2">Comparando {lawIds.length} documentos</p>
            </div>
        );
    }

    if (error) return <div className="text-destructive text-center p-10">{error}</div>;

    if (lawIds.length < 2) {
         return (
            <div className="flex flex-col items-center justify-center py-20">
                <h2 className="text-2xl font-bold mb-4">Selecciona leyes para comparar</h2>
                <p className="text-muted-foreground mb-6 max-w-md text-center">
                    Necesitas al menos dos leyes para usar la herramienta de comparación inteligente.
                </p>
                <Button asChild>
                    <Link href="/search">Ir al Buscador</Link>
                </Button>
            </div>
        );
    }

    return (
        <div className="flex flex-col h-[calc(100vh-80px)]">
            {/* Header */}
            <div className="flex items-center gap-4 py-4 border-b">
                <Button asChild variant="ghost" size="sm">
                    <Link href="/search">
                        <ArrowLeft className="w-4 h-4 mr-2" />
                        Volver
                    </Link>
                </Button>
                <div>
                     <h1 className="text-xl font-bold flex items-center gap-2">
                        <Map className="h-5 w-5 text-primary" />
                        Comparación Estructural
                    </h1>
                </div>
            </div>

            {/* Split View */}
            <div className="flex-1 overflow-hidden">
                <div className="grid grid-cols-2 h-full divide-x">
                    {data.map((law, index) => (
                        <div key={law.details.law_id} className="flex flex-col h-full overflow-hidden">
                            {/* Law Header */}
                            <div className="p-4 bg-muted/30 border-b">
                                <h2 className="font-bold truncate" title={law.details.law_name}>
                                    {law.details.law_name}
                                </h2>
                                <div className="flex gap-2 mt-1">
                                    <Badge variant="outline">{law.details.articles.length} artículos</Badge>
                                </div>
                            </div>
                            
                            {/* Content & Structure */}
                            <div className="flex-1 overflow-hidden flex">
                                {/* Structure Sidebar (Mini) */}
                                <div className="w-1/3 border-r overflow-y-auto bg-muted/10 p-2 hidden lg:block text-xs">
                                     <h3 className="font-semibold mb-2 text-muted-foreground uppercase tracking-wider text-[10px]">Estructura</h3>
                                     <StructureTree nodes={law.structure} />
                                </div>

                                {/* Main Text */}
                                <div className="flex-1 p-4 overflow-y-auto">
                                    <div className="prose dark:prose-invert max-w-none text-sm">
                                        {law.details.articles.map(article => (
                                            <div key={article.article_id} className="mb-4">
                                                <span className="font-bold text-primary block mb-1 sticky top-0 bg-background/90 backdrop-blur z-10">
                                                    {article.article_id}
                                                </span>
                                                <p className="whitespace-pre-wrap text-muted-foreground leading-relaxed">
                                                    {article.text}
                                                </p>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

// Recursive Tree Component
function StructureTree({ nodes, level = 0 }: { nodes: LawStructureNode[], level?: number }) {
    if (!nodes || nodes.length === 0) return <div className="text-muted-foreground italic pl-2">Sin estructura</div>;

    return (
        <ul className={`space-y-1 ${level > 0 ? 'ml-2 border-l pl-2' : ''}`}>
             {nodes.map((node, i) => (
                 <li key={i}>
                     <div className="py-1 px-2 rounded hover:bg-muted cursor-pointer truncate" title={node.label}>
                         {node.label}
                     </div>
                     {node.children && node.children.length > 0 && (
                         <StructureTree nodes={node.children} level={level + 1} />
                     )}
                 </li>
             ))}
        </ul>
    );
}
