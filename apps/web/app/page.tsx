import { Hero } from '@/components/Hero';
import { JurisdictionCards } from '@/components/JurisdictionCards';
import { DashboardStatsGrid, RecentLawsList } from '@/components/DashboardStats';
import { PopularLaws } from '@/components/PopularLaws';
import { DynamicFeatures } from '@/components/DynamicFeatures';
import { DisclaimerBanner } from '@/components/DisclaimerBanner';
import { RecentlyViewed } from '@/components/RecentlyViewed';

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://tezca.mx';

function HomeJsonLd() {
  const webSiteSchema = {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name: 'Tezca',
    alternateName: 'El Espejo de la Ley',
    url: SITE_URL,
    inLanguage: ['es', 'en'],
    potentialAction: {
      '@type': 'SearchAction',
      target: {
        '@type': 'EntryPoint',
        urlTemplate: `${SITE_URL}/busqueda?q={search_term_string}`,
      },
      'query-input': 'required name=search_term_string',
    },
  };

  const organizationSchema = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: 'Tezca',
    url: SITE_URL,
    description: 'Plataforma de legislación mexicana abierta / Open Mexican law platform',
    areaServed: {
      '@type': 'Country',
      name: 'Mexico',
    },
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(webSiteSchema) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationSchema) }}
      />
    </>
  );
}

export default function HomePage() {
  return (
    <div className="min-h-screen bg-background">
      <HomeJsonLd />
      <DisclaimerBanner />
      <Hero />

      <div className="container mx-auto px-4 sm:px-6 -mt-10 relative z-10">
        <DashboardStatsGrid />
      </div>

      <div className="container mx-auto px-4 sm:px-6 py-12 sm:py-16 space-y-12 sm:space-y-16">
        <RecentlyViewed />

        <div className="grid gap-6 sm:gap-8 lg:grid-cols-3">
          <div className="lg:col-span-2 space-y-6 sm:space-y-8">
            <section>
              <h2 className="text-xl sm:text-2xl font-bold tracking-tight mb-4 sm:mb-6">Explorar por Jurisdicción</h2>
              <JurisdictionCards />
            </section>

            <section>
              <PopularLaws />
            </section>
          </div>

          <aside>
            <RecentLawsList />
          </aside>
        </div>

        {/* Features section - dynamically populated from API */}
        <DynamicFeatures />
      </div>
    </div>
  );
}
