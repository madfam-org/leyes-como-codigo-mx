# Development Roadmap - Leyes Como Código México 🇲🇽

This document outlines the strategic plan for evolving the platform from a "Fiscal Pilot" to a robust "State API".

## Phase 1: Foundation (Completed) ✅
- **Structure**: Monorepo setup (`apps/`, `data/`, `engines/`).
- **Ingestion**: Constitution (CPEUM), Civil Code (CCF), Income Tax (LISR) -> Akoma Ntoso XML.
- **Engine**: OpenFisca integration (Mocked) + Catala Source Files.
- **API**: Django REST Framework endpoint (`/api/v1/calculate`).
- **Frontend**: Citizen Viewer (Next.js + Shadcn UI).

## Phase 2: Rigor & Accuracy (Current Focus) 🚧
### 1. Catala Compiler Integration
- **Goal**: Replace `engines/catala/lisr_catala.py` (Mock) with real Python code compiled from `lisr.catala_en`.
- **Action**: Install `catala` CLI in the CI/CD pipeline and local environment.
- **Benefit**: Provably correct tax logic derived directly from the law.

### 2. Complete LISR Implementation
- **Goal**: Encode the complete "Tablas de ISR" (Article 96) and "Deducciones Personales" (Article 151).
- **Action**: Expand `engines/catala/lisr.catala_en`.
- **Benefit**: Accurate calculations for real-world scenarios.

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
