/**
 * Shared language mock helper for Vitest.
 *
 * `useLang()` returns `{ lang, setLang }` where `lang` is the union
 * `'es' | 'en' | 'nah'`. Declaring a mock as
 *
 *     const mockUseLang = vi.fn(() => ({ lang: 'es' as const, setLang: vi.fn() }));
 *
 * makes TypeScript infer the *literal* `'es'` as the return type, so a later
 * `mockUseLang.mockReturnValue({ lang: 'en', ... })` fails to type-check even
 * though it is exactly what the component under test must handle.
 *
 * Use these typed factories instead so the mock is widened to the real
 * context type up front:
 *
 *   import { makeLangMock, langState } from '../helpers/lang-mock';
 *
 *   const mockUseLang = makeLangMock();              // defaults to 'es'
 *   vi.mock('@/components/providers/LanguageContext', () => ({
 *       useLang: () => mockUseLang(),
 *   }));
 *
 *   // Later, switching language type-checks:
 *   mockUseLang.mockReturnValue(langState('en'));
 */
import { vi } from 'vitest';

import type { useLang } from '@/components/providers/LanguageContext';
import type { Lang } from '@/components/providers/LanguageContext';

/** The exact shape `useLang()` returns, derived from the hook itself. */
export type LangState = ReturnType<typeof useLang>;

/**
 * Build a `LangState` for the given language with a fresh `setLang` mock.
 * Typed as the full union so any language is assignable.
 */
export function langState(lang: Lang = 'es', overrides: Partial<LangState> = {}): LangState {
    return { lang, setLang: vi.fn(), ...overrides };
}

/**
 * Create a `vi.fn()` standing in for `useLang`, typed to return the full
 * `LangState` (not a narrowed literal) so `.mockReturnValue(langState('en'))`
 * type-checks.
 */
export function makeLangMock(lang: Lang = 'es') {
    return vi.fn((): LangState => langState(lang));
}
