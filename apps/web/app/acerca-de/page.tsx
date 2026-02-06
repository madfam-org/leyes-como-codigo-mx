'use client';

import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';
import { useLang } from '@/components/providers/LanguageContext';
import { LanguageToggle } from '@/components/LanguageToggle';

const content = {
  es: {
    back: 'Volver al inicio',
    hero: {
      title: 'Tezca',
      subtitle: 'El Espejo de la Ley',
    },
    sections: [
      {
        numeral: 'I',
        title: 'La Sombra',
        body: 'La ley gobierna cada aspecto de la vida pública mexicana, pero permanece atrapada en formatos que la vuelven inaccesible. Documentos PDF dispersos en decenas de sitios gubernamentales. Gacetas oficiales que desaparecen cuando cambian las administraciones. Textos legislativos que exigen intermediarios especializados para su interpretación. Esta opacidad no es un defecto menor: es una forma estructural de injusticia. Un ciudadano que no puede leer la ley que lo obliga vive bajo la sombra de un sistema que lo excluye.',
      },
      {
        numeral: 'II',
        title: 'El Tezcatl',
        body: 'En náhuatl, tezcatl significa espejo de obsidiana — el instrumento que permite verse a uno mismo con claridad absoluta. Tezca es ese espejo aplicado al sistema jurídico mexicano. No interpretamos la ley; la reflejamos. Cada texto legislativo se transforma en datos estructurados que preservan su significado exacto, su jerarquía normativa y sus conexiones con el resto del marco jurídico. La tecnología no reemplaza el juicio humano: lo habilita al hacer visible lo que antes estaba oculto.',
      },
      {
        numeral: 'III',
        title: 'La Transformación',
        body: 'Nuestro enfoque se basa en el isomorfismo: una correspondencia uno a uno entre el texto legal y su representación computacional. Utilizamos estándares internacionales como Akoma Ntoso para preservar la estructura semántica de cada artículo, fracción y párrafo transitorio. No simplificamos, no resumimos, no omitimos. Cada ley procesada mantiene fidelidad absoluta con su fuente oficial. El resultado es una base de datos donde la legislación puede consultarse, compararse y analizarse con la misma precisión que su publicación en el Diario Oficial de la Federación.',
      },
      {
        numeral: 'IV',
        title: 'Infraestructura, no Especulación',
        body: 'Tezca no es un producto comercial ni una startup buscando inversión. Es infraestructura digital pública. Así como un país necesita carreteras para mover bienes y telecomunicaciones para mover información, necesita una capa computacional para hacer operable su marco jurídico. Construimos lo que debería existir como bien público: un API del Estado mexicano donde cualquier ciudadano, emprendedor, investigador o institución pueda consultar la ley vigente de manera programática, confiable y gratuita.',
      },
      {
        numeral: 'V',
        title: 'El Futuro',
        body: 'Imaginamos un país donde la ley no solo se lee, sino que se compila. Donde un emprendedor puede verificar automáticamente los requisitos regulatorios de su actividad. Donde un ciudadano puede entender sus derechos laborales sin necesidad de contratar un abogado. Donde un investigador puede analizar la evolución de la política fiscal a lo largo de décadas en segundos. La ley como código no es una metáfora: es el destino inevitable de todo sistema jurídico que aspire a ser verdaderamente accesible. Tezca es el primer paso.',
      },
    ],
    cta: 'Bienvenido a Tezca',
    ctaSub: 'El sistema legal mexicano, reflejado con claridad.',
  },
  en: {
    back: 'Back to home',
    hero: {
      title: 'Tezca',
      subtitle: 'The Mirror of the Law',
    },
    sections: [
      {
        numeral: 'I',
        title: 'The Shadow',
        body: 'The law governs every aspect of Mexican public life, yet it remains trapped in formats that render it inaccessible. PDF documents scattered across dozens of government websites. Official gazettes that vanish when administrations change. Legislative texts that demand specialized intermediaries for interpretation. This opacity is not a minor defect: it is a structural form of injustice. A citizen who cannot read the law that binds them lives under the shadow of a system that excludes them.',
      },
      {
        numeral: 'II',
        title: 'The Tezcatl',
        body: 'In Nahuatl, tezcatl means obsidian mirror — the instrument that allows one to see oneself with absolute clarity. Tezca is that mirror applied to the Mexican legal system. We do not interpret the law; we reflect it. Each legislative text is transformed into structured data that preserves its exact meaning, its normative hierarchy, and its connections to the rest of the legal framework. Technology does not replace human judgment: it enables it by making visible what was previously hidden.',
      },
      {
        numeral: 'III',
        title: 'The Transformation',
        body: 'Our approach is based on isomorphism: a one-to-one correspondence between the legal text and its computational representation. We use international standards like Akoma Ntoso to preserve the semantic structure of every article, section, and transitory paragraph. We do not simplify, summarize, or omit. Every processed law maintains absolute fidelity to its official source. The result is a database where legislation can be consulted, compared, and analyzed with the same precision as its publication in the Diario Oficial de la Federación.',
      },
      {
        numeral: 'IV',
        title: 'Infrastructure, not Speculation',
        body: 'Tezca is not a commercial product or a startup seeking investment. It is public digital infrastructure. Just as a country needs highways to move goods and telecommunications to move information, it needs a computational layer to make its legal framework operable. We build what should exist as a public good: a Mexican State API where any citizen, entrepreneur, researcher, or institution can query current law programmatically, reliably, and free of charge.',
      },
      {
        numeral: 'V',
        title: 'The Future',
        body: 'We envision a country where the law is not merely read, but compiled. Where an entrepreneur can automatically verify the regulatory requirements for their business. Where a citizen can understand their labor rights without hiring a lawyer. Where a researcher can analyze the evolution of fiscal policy over decades in seconds. Law as code is not a metaphor: it is the inevitable destiny of every legal system that aspires to be truly accessible. Tezca is the first step.',
      },
    ],
    cta: 'Welcome to Tezca',
    ctaSub: 'The Mexican legal system, reflected with clarity.',
  },
};

export default function AcercaDePage() {
  const { lang } = useLang();
  const t = content[lang];

  return (
    <div className="min-h-screen bg-background">
      {/* Dark hero section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary-900 via-primary-800 to-secondary-900 px-4 sm:px-6 py-20 sm:py-28 lg:py-36">
        <div className="absolute inset-0 bg-grid-pattern opacity-10" />
        <div className="relative mx-auto max-w-3xl text-center">
          <div className="flex items-center justify-between absolute top-0 left-0 right-0 -mt-12 sm:-mt-16 px-0">
          </div>
          <h1 className="font-display text-5xl sm:text-7xl lg:text-8xl font-bold tracking-tight text-white">
            {t.hero.title}
          </h1>
          <p className="mt-4 sm:mt-6 font-serif text-xl sm:text-2xl lg:text-3xl text-primary-200 italic">
            {t.hero.subtitle}
          </p>
        </div>
      </section>

      {/* Navigation bar */}
      <div className="container mx-auto px-4 sm:px-6 py-6 max-w-3xl">
        <div className="flex items-center justify-between">
          <Link
            href="/"
            className="inline-flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            <ArrowLeft className="h-4 w-4" />
            {t.back}
          </Link>
          <LanguageToggle />
        </div>
      </div>

      {/* Manifesto sections */}
      <div className="container mx-auto px-4 sm:px-6 pb-16 sm:pb-24 max-w-3xl">
        <div className="space-y-14 sm:space-y-20">
          {t.sections.map((section) => (
            <section key={section.numeral} className="space-y-4">
              <div className="flex items-baseline gap-4">
                <span className="font-serif text-3xl sm:text-4xl font-bold text-primary-600 dark:text-primary-400 select-none">
                  {section.numeral}
                </span>
                <h2 className="font-serif text-2xl sm:text-3xl font-semibold tracking-tight text-foreground">
                  {section.title}
                </h2>
              </div>
              <p className="font-serif text-base sm:text-lg leading-relaxed text-muted-foreground pl-0 sm:pl-14">
                {section.body}
              </p>
            </section>
          ))}
        </div>

        {/* Closing CTA */}
        <div className="mt-20 sm:mt-28 text-center border-t border-border pt-12">
          <p className="font-serif text-2xl sm:text-3xl font-semibold tracking-tight text-foreground">
            {t.cta}
          </p>
          <p className="mt-3 font-serif text-base sm:text-lg text-muted-foreground italic">
            {t.ctaSub}
          </p>
        </div>
      </div>
    </div>
  );
}
