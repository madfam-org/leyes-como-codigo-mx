# 🇲🇽📜 Leyes Como Código México (Mexican Open Law Engine)

> **"Code is Law, Law is Code."**
> Transformando el orden jurídico mexicano de texto estático a código ejecutable, abierto e isomórfico.

![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL_v3-blue.svg)
![Standard: Akoma Ntoso](https://img.shields.io/badge/Standard-Akoma_Ntoso_V3-orange)
![Engine: OpenFisca](https://img.shields.io/badge/Engine-OpenFisca-green)

**Leyes Como Código México** is an open-source initiative to digitize, structure, and encode the entirety of the Mexican Legal System. We convert laws from PDF/Word into **Akoma Ntoso** (structure) and **Catala/OpenFisca** (logic), creating a "State API" that machines can execute.

## 📚 Documentation

Detailed documentation has been organized into the `docs/` directory:

- **[🤖 Operational Protocol](docs/AGENTS.md)**: Directives for AI Contributors.
- **[🛠️ Tech Stack](docs/TECH_STACK.md)**: Official languages and standards.
- **[🧠 Domain Model](docs/ONTOLOGY.md)**: Legal concepts and hierarchy.
- **[🏗️ Architecture](docs/ARCHITECTURE.md)**: System design.
- **[🧪 Testing Strategy](docs/TESTING_STRATEGY.md)**: Verification standards.
- **[🗺️ Roadmap](docs/ROADMAP.md)**: Future development plans.
- **[📝 Product Requirements](docs/PRD.md)**: Feature specifications.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Poetry

### 1. Backend (API & Engine)
```bash
# Clone the repo
git clone https://github.com/madfam-org/leyes-como-codigo-mx.git
cd leyes-como-codigo-mx

# Install dependencies
poetry install
poetry run python -m spacy download es_core_news_sm

# Run the Django API
poetry run python manage.py runserver 8000
```

### 2. Frontend (Citizen Viewer)
```bash
cd apps/web
npm install
npm run dev
```
```
Visit `http://localhost:3000` to access the Tax Calculator.

### 3. Catala Compiler (Docker)
```bash
# Build the Docker image with Catala compiler
docker-compose build api

# Compile Catala source to Python
docker-compose run --rm api ./scripts/compile_catala.sh
```
The Catala compiler is installed via `opam` in the Docker container and generates Python code from `.catala_en` source files.

## 🏗️ Architecture

| Layer | Function | Technology | Status |
| --- | --- | --- | --- |
| **1. Structure** | **The "Git for Law".** Version-controlled history of statutes. | **Akoma Ntoso (XML)** | ✅ CPEUM, CCF, LISR Ingested |
| **2. Semantics** | **The "Brain".** Knowledge Graph linking concepts. | **SpaCy NLP** | 📅 Planned |
| **3. Logic** | **The "Engine".** Executable functions (Tax = f(Income)). | **Catala**, **OpenFisca** | ✅ Pilot (LISR) Live |
| **4. Interface** | **The "Viewer".** Public facing tools for citizens. | **Next.js**, **Django** | ✅ Live |

## 🤝 Contributing

We welcome contributions from **Lawyers**, **Developers**, and **Legal Engineers**.

- See **[CONTRIBUTING.md](CONTRIBUTING.md)** for code standards.
- We use **Conventional Commits**.
- All logic changes require a regression test against the "Oracle" (SAT/Government calculators).

## ⚖️ Disclaimer

**This repository is NOT legal advice.**
While we strive for **Isomorphism** (exact correspondence with the law), the official source of truth remains the *Diario Oficial de la Federación*. Use this code for simulation and research, but always consult a qualified attorney.

**License:** GNU Affero General Public License v3.0 (AGPL-3.0).

---

<div align="center">
  <sub>Built with ❤️ by <a href="https://github.com/madfam-org">madfam-org</a> and the Open Source Community.</sub>
  <br>
  <sub><i>"La ignorancia de la ley no exime de su cumplimiento." — Ahora, el código tampoco.</i></sub>
</div>
