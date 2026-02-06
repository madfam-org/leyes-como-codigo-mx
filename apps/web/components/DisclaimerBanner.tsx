'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { AlertTriangle, X } from 'lucide-react';
import { useLang } from '@/components/providers/LanguageContext';

const STORAGE_KEY = 'disclaimer-dismissed';

const content = {
  es: {
    message:
      'Aviso importante: La información en este sitio es meramente informativa y no constituye asesoría legal. Consulta siempre las fuentes oficiales.',
    readMore: 'Leer más',
    dismiss: 'Cerrar aviso',
  },
  en: {
    message:
      'Important notice: The information on this site is for informational purposes only and does not constitute legal advice. Always consult official sources.',
    readMore: 'Read more',
    dismiss: 'Dismiss notice',
  },
};

export function DisclaimerBanner() {
  const { lang } = useLang();
  const t = content[lang];
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    try {
      if (!localStorage.getItem(STORAGE_KEY)) {
        setVisible(true);
      }
    } catch {
      // localStorage unavailable — keep hidden
    }
  }, []);

  const dismiss = () => {
    setVisible(false);
    try {
      localStorage.setItem(STORAGE_KEY, '1');
    } catch {
      // localStorage unavailable
    }
  };

  if (!visible) return null;

  return (
    <div
      role="alert"
      className="bg-warning-50 dark:bg-warning-700/15 border-b border-warning-500/20"
    >
      <div className="container mx-auto px-4 sm:px-6 py-3 flex items-start gap-3">
        <AlertTriangle className="h-5 w-5 text-warning-700 dark:text-warning-500 flex-shrink-0 mt-0.5" />
        <p className="flex-1 text-sm text-warning-700 dark:text-warning-500">
          {t.message}{' '}
          <Link
            href="/aviso-legal"
            className="underline underline-offset-2 font-medium hover:text-warning-700 dark:hover:text-warning-500"
          >
            {t.readMore}
          </Link>
        </p>
        <button
          onClick={dismiss}
          className="flex-shrink-0 p-1 rounded-md text-warning-700 dark:text-warning-500 hover:bg-warning-500/10 transition-colors"
          aria-label={t.dismiss}
        >
          <X className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}
