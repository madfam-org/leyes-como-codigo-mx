'use client';

import { Printer } from 'lucide-react';
import { useLang } from '@/components/providers/LanguageContext';

const labels = {
    es: 'Imprimir / PDF',
    en: 'Print / PDF',
};

export function PDFExportButton() {
    const { lang } = useLang();

    return (
        <button
            onClick={() => window.print()}
            className="inline-flex items-center gap-2 rounded-md border border-input bg-background px-4 py-2 text-sm font-medium hover:bg-accent hover:text-accent-foreground transition-colors print:hidden"
            title={labels[lang]}
        >
            <Printer className="h-4 w-4" aria-hidden="true" />
            <span className="hidden sm:inline">{labels[lang]}</span>
        </button>
    );
}
