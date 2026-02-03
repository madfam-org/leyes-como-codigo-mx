# Development Roadmap - Leyes Como Código México 🇲🇽

This document outlines the strategic plan for evolving the platform from a "Fiscal Pilot" to a robust "State API".

## Phase 1: Foundation (Completed) ✅
- **Structure**: Monorepo setup (`apps/`, `data/`, `engines/`).
- **Ingestion**: Constitution (CPEUM), Civil Code (CCF), Income Tax (LISR) -> Akoma Ntoso XML.
- **Engine**: OpenFisca integration (Mocked) + Catala Source Files.
- **API**: Django REST Framework endpoint (`/api/v1/calculate`).
- **Frontend**: Citizen Viewer (Next.js + Shadcn UI).

## Phase 2: Rigor & Accuracy (Current Focus) 🚧
### 1. Catala Compiler Integration ✅
- **Status**: **COMPLETED** - Catala compiler installed via opam in Docker container.
- **Achievement**: Successfully compiling `lisr.catala_en` to Python using `catala Python` command.
- **Location**: Compilation script at `scripts/compile_catala.sh`.
- **Output**: Generates `engines/catala/lisr_catala.py` with verified Python classes.

### 2. Complete LISR Implementation
- **Goal**: Encode the complete "Tablas de ISR" (Article 96) and "Deducciones Personales" (Article 151).
- **Action**: Expand `engines/catala/lisr.catala_en`.
- **Benefit**: Accurate calculations for real-world scenarios.

### 3. Law Versioning & Currency Strategy ⚡
- **Goal**: Ensure the platform always encodes the **absolute latest** version of Mexican law.
- **Status**: **CRITICAL** - Must be implemented before scaling.
- **Actions**:
  - Add `@valid_from` and `@valid_until` temporal metadata to all Catala scopes
  - Implement DOF scraper to monitor Diario Oficial de la Federación for LISR reforms
  - Create automated alerts when SAT publishes updated tax tables (e.g., Anexo 8)
  - Version Catala source files by publication date (e.g., `lisr_2026-01-01.catala_en`)
  - Maintain git tags for each DOF decree (e.g., `dof-2025-12-28`)
- **Benefit**: **Isomorphism guarantee** - Code is always in sync with the official law.

### 4. Full Law Ingestion Pipeline 🚀
- **Goal**: Build scalable infrastructure to ingest all current Mexican law into Akoma Ntoso XML.
- **Status**: **PHASE A COMPLETE** - POC validated, ready for core pipeline infrastructure.
- **Current State**:
  - ✅ 4 laws ingested (CPEUM, LISR, CCF, **Ley de Amparo**)
  - ✅ DOF **official API** discovered (no scraping needed!)
  - ✅ Working PDF → Akoma Ntoso parser (`apps/parsers/akn_generator.py`)
  - ✅ Full pipeline validated (23 seconds for 119-page law)
  - ✅ Schema-compliant XML (285 articles, 31 chapters)
- **Actions**:
  - **Phase A - Proof of Concept** ✅ **COMPLETED**:
    - ✅ Implemented DOF API client for Ley de Amparo
    - ✅ Built custom parser for Mexican legal structure (Bluebell deferred)
    - ✅ Tested full pipeline: DOF → PDF → Text → Akoma Ntoso → Validation
    - ✅ Documented metrics: <1 min runtime, ~90% accuracy (estimate)
    - 📄 **Deliverables**: [POC Walkthrough](/Users/aldoruizluna/.gemini/antigravity/brain/24129255-6e54-42e3-9545-5588caba8ea2/poc_walkthrough.md) | [DOF Research](/Users/aldoruizluna/.gemini/antigravity/brain/24129255-6e54-42e3-9545-5588caba8ea2/dof_research.md)
  - **Phase B - Core Pipeline** (NEXT - 12 weeks):
    - Build robust PDF text extraction (handle scanned images with OCR)
    - Implement Celery task queue for batch processing
    - Create quality validation checks (XML schema, completeness)
    - Build admin dashboard for monitoring ingestion jobs
  - **Phase C - Scale to 10 Laws** (8 weeks):
    - Ingest priority federal laws: IVA, LFT, CPF, LFPCA, etc.
    - Measure parse accuracy and manual correction requirements
    - Optimize pipeline based on learnings
  - **Phase D - Federal Corpus** (6 months):
    - Ingest ~200 major federal laws
    - Build law change detection (daily DOF monitoring)
    - Implement temporal validity tracking for amendments
- **Benefit**: Complete, auditable, version-controlled corpus of Mexican law.


## Phase 3: Infrastructure & Scale 🚀
### 1. Dockerization
- **Goal**: Containerize Backend (Django), Frontend (Next.js), and Redis/Celery.
- **Action**: Create `Dockerfile` and `docker-compose.yml`.

### 2. Search Engine
- **Goal**: Allow semantic search over the Law (XML).
- **Action**: Index XML files into Elasticsearch/VectorDB.
- **Benefit**: "Chat with the Law" features.

## Phase 4: Expansion 🗳️
- **More Laws**: VAT (IVA), Labor Law (LFT).
- **State Laws**: Civil Codes of CDMX, Nuevo León, etc.
- **Auth**: User accounts to save calculations.

---
> **Note**: This roadmap is living and subject to change based on legislative updates and technical findings.
