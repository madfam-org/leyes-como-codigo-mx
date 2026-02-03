import { notFound } from 'next/navigation';
import { getLawById } from '@/lib/laws';
import { Badge } from '@/components/ui/badge';
import { Card } from '@/components/ui/card';
import Link from 'next/link';
import LawArticles from '@/components/LawArticles';

interface PageProps {
    params: Promise<{
        id: string;
    }>;
}

export default async function LawDetailPage({ params }: PageProps) {
    const { id } = await params;
    const law = await getLawById(id);

    if (!law) {
        notFound();
    }

    const gradeColors = {
        A: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
        B: 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200',
        C: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 dark:from-gray-900 dark:to-blue-950">
            {/* Header */}
            <div className="bg-gradient-to-r from-blue-600 to-blue-800 dark:from-blue-800 dark:to-blue-950 text-white shadow-xl">
                <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                    <Link
                        href="/laws"
                        className="inline-flex items-center text-blue-100 hover:text-white mb-4 transition-colors"
                    >
                        ← Volver a todas las leyes
                    </Link>

                    <h1 className="text-3xl font-bold mb-2">
                        {law.fullName}
                    </h1>

                    <div className="flex gap-3 flex-wrap mt-4">
                        <Badge className={`${gradeColors[law.grade]} text-sm`}>
                            Grade {law.grade} ({law.score}%)
                        </Badge>
                        <Badge variant="outline" className="bg-white/10 text-white border-white/30">
                            Prioridad {law.priority}
                        </Badge>
                        <Badge variant="outline" className="bg-white/10 text-white border-white/30">
                            {law.tier}
                        </Badge>
                    </div>
                </div>
            </div>

            {/* Content */}
            <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Stats Card */}
                <Card className="p-6 mb-8 bg-white dark:bg-gray-800">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                        <div>
                            <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                                Artículos
                            </div>
                            <div className="text-2xl font-bold text-gray-900 dark:text-white">
                                {law.articles.toLocaleString()}
                            </div>
                        </div>

                        <div>
                            <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                                Transitorios
                            </div>
                            <div className="text-2xl font-bold text-gray-900 dark:text-white">
                                {law.transitorios}
                            </div>
                        </div>

                        <div>
                            <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                                Calidad
                            </div>
                            <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                                {law.score}%
                            </div>
                        </div>

                        <div>
                            <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                                Formato
                            </div>
                            <div className="text-sm font-semibold text-gray-900 dark:text-white mt-2">
                                Akoma Ntoso 3.0
                            </div>
                        </div>
                    </div>
                </Card>

                {/* Articles */}
                <LawArticles lawId={law.id} />

                {/* Download Section */}
                <Card className="p-6 mt-8 bg-blue-50 dark:bg-blue-950/30 border-blue-200 dark:border-blue-800">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                        Descargar XML
                    </h3>
                    <p className="text-gray-600 dark:text-gray-400 mb-4">
                        Archivo XML en formato Akoma Ntoso 3.0, listo para procesamiento automático.
                    </p>
                    <a
                        href={`/data/federal/${law.file}`}
                        download
                        className="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
                    >
                        📄 Descargar {law.file}
                    </a>
                </Card>

                {/* Version History */}
                {law.versions && law.versions.length > 0 && (
                    <Card className="p-6 mt-8 bg-white dark:bg-gray-800">
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                            Historial de Reformas
                        </h3>
                        <div className="overflow-x-auto">
                            <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                                <thead>
                                    <tr>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha de Publicación</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Archivo XML</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                                    {law.versions.map((ver, idx) => (
                                        <tr key={idx}>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                                                {new Date(ver.publication_date).toLocaleDateString('es-MX')}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                                {ver.xml_file || '-'}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                                {ver.xml_file && (
                                                    <a href={`/data/federal/${ver.xml_file}`} download className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300">
                                                        Descargar
                                                    </a>
                                                )}
                                                {ver.dof_url && (
                                                    <a href={ver.dof_url} target="_blank" rel="noopener noreferrer" className="ml-4 text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300">
                                                        Ver PDF
                                                    </a>
                                                )}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </Card>
                )}
            </div>
        </div>
    );
}
