# Roadmap: Leyes Como Código México 🇲🇽

**Mission**: Transform Mexican federal and state laws into a queryable, provably correct, and beautiful digital platform.

## Phase 1: Foundation (Completed) ✅
**Goal**: Establish the core infrastructure and prove the concept.

- **Structure**: Monorepo setup (`apps/`, `data/`, `engines/`).
- **Ingestion**: Initial pipeline for 4 key laws (CPEUM, LISR, CCF, Ley de Amparo).
- **Engine**: OpenFisca integration (Mocked) + Catala Source Files.
- **Admin**: Basic Console for ingestion control (`apps/admin`).
- **Frontend**: Citizen Viewer v1 (Next.js + Shadcn UI).

---

## Phase 2: Professional Platform & Design System (Current Focus) 🚧
**Goal**: Transform from prototype to a gorgeous, professional-grade legal platform.

### 1. UI/UX Design System (The "Gorgeous" Part)
- [ ] **Audit**: Document current UI pain points and inconsistencies.
- [ ] **Design System**: Define strict tokens for colors, typography, and spacing (Mexican-inspired palette).
- [ ] **Component Library**: Build 15+ reusable, accessible components (Buttons, Cards, Inputs).
- [ ] **Dark Mode**: First-class support for dark/light themes.

### 2. Search & Discovery
- [ ] **Elasticsearch Implementation**: Index full text of all ingested laws.
- [ ] **Search UI**: Autocomplete, facetted filtering (law, date, category), and results highlighting.
- [ ] **Navigation Redesign**: Mega-menus for law categories, breadcrumbs, and directory pages.

### 3. Law Versioning & Rigor (The "Correct" Part)
- [ ] **Temporal Validity**: Implementation of `@valid_from` and `@valid_until` metadata in engines.
- [ ] **Change Detection**: Automated monitoring of DOF (Diario Oficial) for reforms.
- [ ] **Catala Integration**: Complete LISR implementation (Articles 96 & 151) for accurate tax calculations.

---

## Phase 3: Content Expansion & RAG 📚
**Goal**: Reach critical mass of content (25% coverage) and intelligent features.

### 1. Batch Ingestion Scaling
- [ ] **Priority 2 Laws**: Ingest top 40 most-cited federal laws (Fiscal, Labor, Criminal).
- [ ] **Quality Validation**: Automated "Grade" system for parsing quality (A-F).
- [ ] **Manual Correction**: Admin tools to fix parsing errors in "Grade B/C" documents.

### 2. Cross-References & Citations
- [ ] **Citation Parser**: Extract and link references (e.g., "Ver Art. 24") across the corpus.
- [ ] **Graph Database**: Model relationships between laws and articles.

### 3. Smart Features ('Chat with the Law')
- [ ] **Vector Database**: Index articles for semantic search.
- [ ] **LLM Integration**: RAG pipeline for answering natural language questions.

---

## Phase 4: Professional Tools & Ecosystem 🧰
**Goal**: Tools for legal professionals and developers.

### 1. User Features
- [ ] **Personalization**: Bookmarks, reading history, and "My Library".
- [ ] **Export**: PDF, Word, and Markdown export with compliant citations.

### 2. Public API
- [ ] **REST API**: `/api/laws`, `/api/articles`, `/api/search`.
- [ ] **Documentation**: OpenAPI (Swagger) specs and developer guides.

### 3. Mobile Optimization
- [ ] **Responsive Design**: Touch-friendly interfaces and swipe gestures.
- [ ] **PWA**: Offline reading capabilities.

---

## Technical Foundation (Ongoing) 🏗
- **Testing**: maintain >90% coverage.
- **CI/CD**: Automated pipelines for ingestion and deployment.
- **Security**: RBAC for admin tools, secure API access.
- **Performance**: <2s page loads via edge caching and code splitting.
