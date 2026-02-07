'use client';

import { useLang } from '@/components/providers/LanguageContext';
import type { Lang } from '@/components/providers/LanguageContext';

export function LanguageToggle() {
  const { lang, setLang } = useLang();

  const options: { value: Lang; label: string; ariaLabel: string }[] = [
    { value: 'es', label: 'ES', ariaLabel: 'Cambiar a español' },
    { value: 'en', label: 'EN', ariaLabel: 'Switch to English' },
    { value: 'nah', label: 'NAH', ariaLabel: 'Xicpati nāhuatl' },
  ];

  return (
    <div className="inline-flex items-center rounded-md border border-border bg-muted/50 p-0.5" role="group" aria-label="Language">
      {options.map((opt) => (
        <button
          key={opt.value}
          onClick={() => setLang(opt.value)}
          className={`px-2 py-1 text-xs sm:text-sm font-medium rounded transition-colors ${
            lang === opt.value
              ? 'bg-primary-600 text-white shadow-sm'
              : 'text-muted-foreground hover:text-foreground'
          }`}
          aria-label={opt.ariaLabel}
          aria-pressed={lang === opt.value}
        >
          {opt.label}
        </button>
      ))}
    </div>
  );
}
