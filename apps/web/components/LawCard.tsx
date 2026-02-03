'use client';

import { Law } from '@/lib/laws';
import { Badge } from '@/components/ui/badge';
import { Card } from '@/components/ui/card';
import Link from 'next/link';

interface LawCardProps {
    law: Law;
}

export default function LawCard({ law }: LawCardProps) {
    const gradeColors = {
        A: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
        B: 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200',
        C: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
    };

    return (
        <Link href={`/laws/${law.id}`}>
            <Card className="p-6 hover:shadow-lg transition-all duration-300 hover:-translate-y-1 hover:border-blue-400 cursor-pointer h-full">
                <h3 className="text-xl font-semibold text-blue-600 dark:text-blue-400 mb-3">
                    {law.name}
                </h3>

                <div className="flex gap-2 flex-wrap mb-3">
                    <Badge className={gradeColors[law.grade]}>
                        Grade {law.grade}
                    </Badge>
                    <Badge variant="outline">
                        Prioridad {law.priority}
                    </Badge>
                </div>

                <div className="text-sm text-gray-600 dark:text-gray-400">
                    <span className="font-semibold text-gray-900 dark:text-gray-100">
                        {law.articles.toLocaleString()}
                    </span> artículos •
                    <span className="font-semibold text-gray-900 dark:text-gray-100 ml-1">
                        {law.score}%
                    </span> calidad
                </div>

                {law.transitorios > 0 && (
                    <div className="text-xs text-gray-500 dark:text-gray-500 mt-2">
                        + {law.transitorios} transitorios
                    </div>
                )}
            </Card>
        </Link>
    );
}
