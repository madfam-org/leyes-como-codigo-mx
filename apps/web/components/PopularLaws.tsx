'use client';

import Link from 'next/link';
import { Badge } from '@tezca/ui';
import { useLang } from '@/components/providers/LanguageContext';

const content = {
    es: {
        title: 'Leyes Populares',
        subtitle: 'Acceso rápido a las leyes más consultadas',
    },
    en: {
        title: 'Popular Laws',
        subtitle: 'Quick access to the most consulted laws',
    },
};

const popularLaws = [
    { id: 'mx-fed-cpeum', name: 'Constitución', href: '/laws/mx-fed-cpeum' },
    { id: 'mx-fed-ccf', name: 'Código Civil Federal', href: '/laws/mx-fed-ccf' },
    { id: 'mx-fed-cpf', name: 'Código Penal Federal', href: '/laws/mx-fed-cpf' },
    { id: 'mx-fed-lisr', name: 'ISR', href: '/laws/mx-fed-lisr' },
    { id: 'mx-fed-liva', name: 'IVA', href: '/laws/mx-fed-liva' },
    { id: 'mx-fed-lft', name: 'Ley Federal del Trabajo', href: '/laws/mx-fed-lft' },
    { id: 'mx-fed-lss', name: 'Seguro Social', href: '/laws/mx-fed-lss' },
    { id: 'mx-fed-amparo', name: 'Amparo', href: '/laws/mx-fed-amparo' },
];

export function PopularLaws() {
    const { lang } = useLang();
    const t = content[lang];

    return (
        <div className="mx-auto max-w-7xl px-6 py-16">
            <div className="mb-8 text-center">
                <h2 className="font-display text-2xl font-bold text-foreground sm:text-3xl">
                    {t.title}
                </h2>
                <p className="mt-2 text-muted-foreground">
                    {t.subtitle}
                </p>
            </div>

            <div className="flex flex-wrap justify-center gap-3">
                {popularLaws.map((law) => (
                    <Link key={law.id} href={law.href}>
                        <Badge
                            variant="secondary"
                            className="cursor-pointer px-6 py-3 text-base font-medium transition-all hover:scale-105 hover:bg-primary-100 hover:text-primary-700 dark:hover:bg-primary-900"
                        >
                            {law.name}
                        </Badge>
                    </Link>
                ))}
            </div>
        </div>
    );
}
