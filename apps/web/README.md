# Public Portal (Web)

The citizen-facing web application for searching and reading Mexican laws.

## Features
- **Law Search**: Full-text search with filters (Federal, State, Date) and autocomplete typeahead.
- **Law Visualization**: Clean, readable presentation of laws with indices.
- **Comparison**: Side-by-side law comparison with sync scroll, metadata panel, and mobile tabs.
- **Dashboard**: High-level statistics of the legal database.
- **Legal Pages**: Terms & Conditions, Legal Disclaimer, Privacy Policy — trilingual ES/EN/NAH.
- **Site Footer**: Navigation links, official sources, disclaimer bar, copyright notice.
- **Disclaimer Banner**: Dismissable homepage notice with localStorage persistence.
- **Trilingual Support**: ES/EN/NAH (Classical Nahuatl) language toggle across all UI components (law content remains Spanish-only).

## Routes

| Route | Description |
|-------|-------------|
| `/` | Homepage with dashboard, search, and jurisdiction cards |
| `/busqueda` | Advanced law search with filters |
| `/leyes` | Law catalog |
| `/leyes/[id]` | Individual law detail page |
| `/comparar` | Side-by-side law comparison |
| `/categorias` | Browse laws by legal category |
| `/categorias/[category]` | Laws in a specific category |
| `/estados` | Browse laws by Mexican state |
| `/estados/[state]` | Laws in a specific state |
| `/favoritos` | Bookmarked laws |
| `/acerca-de` | About page |
| `/terminos` | Terms & Conditions (trilingual) |
| `/aviso-legal` | Legal Disclaimer (trilingual) |
| `/privacidad` | Privacy Policy (trilingual) |

### Route Redirects

As of Phase 9, all primary routes use Spanish paths. The old English routes (`/search`, `/laws`, `/laws/[id]`, `/compare`) return **301 permanent redirects** to their Spanish equivalents (`/busqueda`, `/leyes`, `/leyes/[id]`, `/comparar`). Existing bookmarks and external links will continue to work.

## Tech Stack
- **Framework**: Next.js 15 (App Router)
- **UI**: React 19, Tailwind CSS 4, @tezca/ui (Shadcn)
- **Search**: Elasticsearch Integration
- **Testing**: Vitest + @testing-library/react (25 test files, 156 tests)

## Development

Start the development server from the root of the monorepo:

```bash
npm run dev --workspace=apps/web
```

The portal will be available at [http://localhost:3000](http://localhost:3000).

## Testing

```bash
cd apps/web && npx vitest run
```
