import { notFound } from 'next/navigation';
import { api } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Calendar, FileText, ExternalLink } from 'lucide-react';

export default async function LawDetailPage({
    params
}: {
    params: { id: string }
}) {
    let law;

    try {
        law = await api.getLaw(params.id);
    } catch (error) {
        notFound();
    }

    return (
        <div className="min-h-screen bg-background">
            {/* Header */}
            <div className="border-b border-border bg-gradient-to-br from-primary-500 to-primary-600 px-6 py-12">
                <div className="mx-auto max-w-5xl">
                    <div className="mb-4 flex items-center gap-3">
                        <Badge variant="secondary" className="bg-white/20 text-white backdrop-blur-sm">
                            {law.id}
                        </Badge>
                        {law.grade && (
                            <Badge
                                className={`
                  ${law.grade === 'A' ? 'bg-grade-a' : ''}
                  ${law.grade === 'B' ? 'bg-grade-b' : ''}
                  ${law.grade === 'C' ? 'bg-grade-c' : ''}
                  ${law.grade === 'D' ? 'bg-grade-d' : ''}
                  ${law.grade === 'F' ? 'bg-grade-f' : ''}
                  text-white
                `}
                            >
                                Grado {law.grade}
                            </Badge>
                        )}
                    </div>

                    <h1 className="font-display text-4xl font-bold text-white sm:text-5xl">
                        {law.name}
                    </h1>

                    {law.short_name && law.short_name !== law.name && (
                        <p className="mt-3 text-lg text-primary-100">
                            {law.short_name}
                        </p>
                    )}
                </div>
            </div>

            {/* Content */}
            <div className="mx-auto max-w-5xl px-6 py-8">
                <div className="grid gap-8 lg:grid-cols-[1fr_350px]">
                    {/* Main Column */}
                    <div className="space-y-6">
                        {/* Metadata */}
                        <Card>
                            <CardHeader>
                                <CardTitle>Información General</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div className="grid gap-4 sm:grid-cols-2">
                                    {law.category && (
                                        <div>
                                            <div className="text-sm font-medium text-muted-foreground">Categoría</div>
                                            <div className="mt-1 text-base">{law.category}</div>
                                        </div>
                                    )}

                                    {law.tier && (
                                        <div>
                                            <div className="text-sm font-medium text-muted-foreground">Nivel</div>
                                            <div className="mt-1 text-base">Tier {law.tier}</div>
                                        </div>
                                    )}

                                    {law.articles !== undefined && (
                                        <div>
                                            <div className="text-sm font-medium text-muted-foreground">Artículos</div>
                                            <div className="mt-1 flex items-center gap-2">
                                                <FileText className="h-4 w-4 text-muted-foreground" />
                                                <span className="text-base font-semibold">{law.articles.toLocaleString('es-MX')}</span>
                                            </div>
                                        </div>
                                    )}

                                    {law.score !== undefined && (
                                        <div>
                                            <div className="text-sm font-medium text-muted-foreground">Calidad</div>
                                            <div className="mt-1 text-base font-semibold text-primary-600">
                                                {law.score}%
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </CardContent>
                        </Card>

                        {/* Version History */}
                        <Card>
                            <CardHeader>
                                <CardTitle>Historial de Versiones</CardTitle>
                            </CardHeader>
                            <CardContent>
                                {law.versions && law.versions.length > 0 ? (
                                    <div className="space-y-4">
                                        {law.versions.map((version, index) => (
                                            <div
                                                key={index}
                                                className="flex items-start justify-between gap-4 rounded-lg border border-border p-4 transition-colors hover:bg-muted/50"
                                            >
                                                <div className="flex-1">
                                                    <div className="flex items-center gap-2">
                                                        <Calendar className="h-4 w-4 text-muted-foreground" />
                                                        <span className="font-medium">
                                                            {new Date(version.publication_date).toLocaleDateString('es-MX', {
                                                                year: 'numeric',
                                                                month: 'long',
                                                                day: 'numeric'
                                                            })}
                                                        </span>
                                                    </div>

                                                    {version.valid_from && (
                                                        <div className="mt-2 text-sm text-muted-foreground">
                                                            Vigente desde: {new Date(version.valid_from).toLocaleDateString('es-MX')}
                                                        </div>
                                                    )}

                                                    {version.xml_file && (
                                                        <div className="mt-2 text-xs font-mono text-muted-foreground">
                                                            {version.xml_file}
                                                        </div>
                                                    )}
                                                </div>

                                                {version.dof_url && (
                                                    <a
                                                        href={version.dof_url}
                                                        target="_blank"
                                                        rel="noopener noreferrer"
                                                        className="flex items-center gap-1 text-sm text-primary-600 hover:text-primary-700"
                                                    >
                                                        DOF
                                                        <ExternalLink className="h-3 w-3" />
                                                    </a>
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                ) : (
                                    <p className="text-muted-foreground">No hay versiones disponibles</p>
                                )}
                            </CardContent>
                        </Card>
                    </div>

                    {/* Sidebar */}
                    <div className="space-y-6">
                        <Card>
                            <CardHeader>
                                <CardTitle>Acciones</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-3">
                                <a
                                    href={`/api/v1/laws/${law.id}/`}
                                    target="_blank"
                                    className="flex w-full items-center justify-center gap-2 rounded-lg bg-primary-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-primary-700"
                                >
                                    <FileText className="h-4 w-4" />
                                    Ver JSON
                                </a>

                                {law.versions && law.versions[0]?.dof_url && (
                                    <a
                                        href={law.versions[0].dof_url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="flex w-full items-center justify-center gap-2 rounded-lg border border-border px-4 py-2 text-sm font-medium transition-colors hover:bg-muted"
                                    >
                                        <ExternalLink className="h-4 w-4" />
                                        Abrir en DOF
                                    </a>
                                )}
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader>
                                <CardTitle>Estadísticas</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-3">
                                <div>
                                    <div className="text-sm text-muted-foreground">Versiones</div>
                                    <div className="text-2xl font-bold">{law.versions?.length || 0}</div>
                                </div>

                                {law.grade && (
                                    <div>
                                        <div className="text-sm text-muted-foreground">Grado de Calidad</div>
                                        <div className="text-2xl font-bold">{law.grade}</div>
                                    </div>
                                )}
                            </CardContent>
                        </Card>
                    </div>
                </div>
            </div>
        </div>
    );
}
