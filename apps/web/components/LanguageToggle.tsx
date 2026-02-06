'use client';

import { useLang } from '@/components/providers/LanguageContext';
import type { Lang } from '@/components/providers/LanguageContext';

export function LanguageToggle() {
  const { lang, setLang } = useLang();

  const options: { value: Lang; label: string }[] = [
    { value: 'es', label: 'ES' },
    { value: 'en', label: 'EN' },
  ];

  return (
    <div className="inline-flex items-center rounded-md border border-border bg-muted/50 p-0.5">
      {options.map((opt) => (
        <button
          key={opt.value}
          onClick={() => setLang(opt.value)}
          className={`px-2 py-1 text-xs sm:text-sm font-medium rounded transition-colors ${
            lang === opt.value
              ? 'bg-primary-600 text-white shadow-sm'
              : 'text-muted-foreground hover:text-foreground'
          }`}
          aria-label={opt.value === 'es' ? 'Cambiar a español' : 'Switch to English'}
          aria-pressed={lang === opt.value}
        >
          {opt.label}
        </button>
      ))}
    </div>
  );
}
