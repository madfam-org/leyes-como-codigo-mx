import { laws, getTotalArticles, getAverageQuality } from '@/lib/laws';
import LawCard from '@/components/LawCard';
import Link from 'next/link';

export default function LawsPage() {
    const totalArticles = getTotalArticles();
    const avgQuality = getAverageQuality();

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 dark:from-gray-900 dark:to-blue-950">
            {/* Header */}
            <div className="bg-gradient-to-r from-blue-600 to-blue-800 dark:from-blue-800 dark:to-blue-950 text-white shadow-xl">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                    <div className="flex justify-between items-start">
                        <div>
                            <h1 className="text-4xl font-bold mb-2">
                                🇲🇽 Leyes Como Código
                            </h1>
                            <p className="text-xl text-blue-100">
                                Legislación Federal en Formato Akoma Ntoso
                            </p>
                        </div>
                        <Link
                            href="/"
                            className="bg-white/10 hover:bg-white/20 px-4 py-2 rounded-lg transition-colors"
                        >
                            ← Inicio
                        </Link>
                    </div>
                </div>
            </div>

            {/* Stats */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border-l-4 border-blue-600">
                        <div className="text-sm font-medium text-gray-600 dark:text-gray-400 uppercase tracking-wide">
                            Leyes Disponibles
                        </div>
                        <div className="text-3xl font-bold text-blue-600 dark:text-blue-400 mt-2">
                            {laws.length}
                        </div>
                    </div>

                    <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border-l-4 border-green-600">
                        <div className="text-sm font-medium text-gray-600 dark:text-gray-400 uppercase tracking-wide">
                            Artículos Totales
                        </div>
                        <div className="text-3xl font-bold text-green-600 dark:text-green-400 mt-2">
                            ~{(totalArticles / 1000).toFixed(1)}k
                        </div>
                    </div>

                    <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border-l-4 border-purple-600">
                        <div className="text-sm font-medium text-gray-600 dark:text-gray-400 uppercase tracking-wide">
                            Calificación Promedio
                        </div>
                        <div className="text-3xl font-bold text-purple-600 dark:text-purple-400 mt-2">
                            {avgQuality.toFixed(1)}%
                        </div>
                    </div>

                    <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border-l-4 border-indigo-600">
                        <div className="text-sm font-medium text-gray-600 dark:text-gray-400 uppercase tracking-wide">
                            Validación Schema
                        </div>
                        <div className="text-3xl font-bold text-indigo-600 dark:text-indigo-400 mt-2">
                            100%
                        </div>
                    </div>
                </div>

                {/* Laws Grid */}
                <div className="mb-8">
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                        Leyes Federales
                    </h2>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {laws.map((law) => (
                            <LawCard key={law.id} law={law} />
                        ))}
                    </div>
                </div>

                {/* Info Footer */}
                <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                        Sobre este visor
                    </h3>
                    <p className="text-gray-600 dark:text-gray-400 mb-3">
                        Este visor presenta 10 leyes federales mexicanas convertidas al estándar internacional
                        <strong className="text-gray-900 dark:text-white"> Akoma Ntoso 3.0</strong>,
                        un formato estructurado XML para documentos legales.
                    </p>
                    <div className="flex gap-4 text-sm text-gray-500 dark:text-gray-500">
                        <span>✅ 100% validación de schema</span>
                        <span>✅ ~8,000 artículos procesados</span>
                        <span>✅ Formato machine-readable</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
