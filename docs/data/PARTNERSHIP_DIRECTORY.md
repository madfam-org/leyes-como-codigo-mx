# Partnership & Contact Directory

**Last Updated**: 2026-02-06
**Purpose**: Institutional contacts, legal obligations, and FOIA reference for data acquisition.

---

## Legal Framework for Data Requests

### Constitutional Basis

| Article | Right | Application |
|---------|-------|-------------|
| Art. 6 Constitucional | Right to information; principio de máxima publicidad | All public information is presumed accessible unless classified |
| Art. 8 Constitucional | Derecho de petición (right to petition) | Any authority must respond to written petitions; response is mandatory |
| Art. 133 Constitucional | Legal hierarchy and supremacy | Establishes what legal instruments exist and their precedence |

### Statutory Basis

| Law / Article | Obligation | Timeline |
|---------------|------------|----------|
| LGTAIP Art. 70, Frac. I | All sujetos obligados must publish their marco normativo | Proactive publication (no request needed) |
| LGTAIP Art. 132 | Response to information requests | 20 business days (+ 10 day extension if notified) |
| LGTAIP Art. 155 | Appeal resolution timeline | 40 business days |
| LFTAIP Art. 116 | Federal entities' response obligations | Same as LGTAIP Art. 132 |

### FOIA Filing Portal

**Plataforma Nacional de Transparencia (PNT)**
- URL: https://www.plataformadetransparencia.org.mx/
- Covers: All 3 levels of government (federal, state, municipal)
- Requirements: Free account; no citizenship requirement
- Tracking: Folio number issued upon submission

### Post-INAI Landscape (March 2025)

**INAI was dissolved in March 2025.** Federal FOIA appeals are now handled by the **Secretaría Anticorrupción y Buen Gobierno** through the "Transparencia para el Pueblo" program.

**19 of 32 state transparency institutes were also dissolved.** For affected states, FOIA appeals should be filed through PNT to the federal successor body.

**States with active transparency institutes (13 confirmed as of Feb 2026)**:

| State | Institute | Status |
|-------|-----------|--------|
| Jalisco | ITEI | Active |
| Nuevo León | COTAI | Active |
| Chihuahua | ICHITAIP | Active |
| Veracruz | IVAI | Active |
| Sonora | ISTAI | Active |
| Guanajuato | IACIP | Active |
| Coahuila | ICAI | Active |
| Yucatán | INAIP | Active |
| Puebla | ITAIP | Active |
| Querétaro | IQCA | Active |
| Oaxaca | IAIP | Active |
| Tabasco | ITAIP | Active |
| Aguascalientes | ITEA | Active |

> **Note**: Status may change. Verify before filing appeals. For states not listed, route appeals through PNT to federal successor body.

---

## Federal Government Institutions

### 1. SEGOB — Dirección General de Compilación y Consulta del OJN

| Field | Value |
|-------|-------|
| **Priority** | 1 (Highest) |
| **Type** | Federal government (Secretaría de Gobernación) |
| **Portal** | https://compilacion.ordenjuridico.gob.mx/ |
| **Known contact** | rnava@segob.gob.mx |
| **Transparency unit** | unidaddetransparencia@segob.gob.mx |
| **PNT sujeto obligado** | Secretaría de Gobernación |
| **Legal obligation** | LGTAIP Art. 70 Frac. I (marco normativo publication) |
| **What we need** | 1) Fix 782 dead links on OJN portal; 2) Bulk API access to law catalog; 3) Quality improvement for poderes 1/3/4 data |
| **Status** | Not yet contacted |

**Notes**: OJN is the most comprehensive source for state-level legislation. The 782 dead links (Michoacán 504, EDOMEX 141, SLP 47) represent permanent data gaps that only SEGOB can resolve. SEGOB also controls the DOF.

---

### 2. Cámara de Diputados — Leyes Vigentes

| Field | Value |
|-------|-------|
| **Priority** | 2 |
| **Type** | Federal legislative (Poder Legislativo) |
| **Portal** | https://www.diputados.gob.mx/LeyesBiblio/ |
| **Reglamentos page** | https://www.diputados.gob.mx/LeyesBiblio/regla.htm |
| **Transparency unit** | transparencia@diputados.gob.mx |
| **PNT sujeto obligado** | Cámara de Diputados |
| **Legal obligation** | LGTAIP Art. 70 Frac. I |
| **What we need** | 1) Reglamentos page scraping access (~800 regulations); 2) Reform history XML; 3) DOF reference cross-links |
| **Status** | Not yet contacted |

**Notes**: Primary source for all 336 federal laws. Reglamentos page is a separate catalog not yet scraped — represents a quick win (~800 instruments).

---

### 3. DOF / SIDOF (Diario Oficial de la Federación)

| Field | Value |
|-------|-------|
| **Priority** | 2 |
| **Type** | Federal government (SEGOB) |
| **Portal** | https://dof.gob.mx/ |
| **API** | https://sidof.segob.gob.mx/ |
| **Transparency unit** | unidaddetransparencia@segob.gob.mx (same as SEGOB) |
| **PNT sujeto obligado** | Secretaría de Gobernación |
| **Legal obligation** | Art. 6 Constitucional; LGTAIP Art. 70 |
| **What we need** | 1) Daily gazette feed API documentation; 2) Historical DOF archive bulk access; 3) Structured metadata |
| **Status** | Not yet contacted |

**Notes**: DOF is the official publication vehicle for ALL federal instruments. SIDOF API exists but documentation is limited. Daily monitoring would enable auto-update functionality.

---

### 4. CONAMER (Comisión Nacional de Mejora Regulatoria)

| Field | Value |
|-------|-------|
| **Priority** | 3 |
| **Type** | Federal government (decentralized body) |
| **Portal** | https://www.gob.mx/conamer |
| **CNARTyS** | https://cnartys.conamer.gob.mx/ |
| **Transparency unit** | transparencia@conamer.gob.mx |
| **PNT sujeto obligado** | Comisión Nacional de Mejora Regulatoria |
| **Legal obligation** | LGMR Art. 76 (regulatory catalog publication); LGTAIP Art. 70 |
| **What we need** | 1) Full regulatory catalog API or bulk download (113,373 regulations); 2) Classification taxonomy; 3) Update frequency data |
| **Status** | Not yet contacted |

**Notes**: CNARTyS is the most comprehensive catalog of Mexican regulations across all levels of government. If a bulk download or API is available, this would be the single largest data acquisition event possible.

---

### 5. Senado de la República

| Field | Value |
|-------|-------|
| **Priority** | 4 |
| **Type** | Federal legislative (Poder Legislativo) |
| **Portal** | https://www.senado.gob.mx/ |
| **SIL** | http://sil.gobernacion.gob.mx/ |
| **Transparency unit** | transparencia@senado.gob.mx |
| **PNT sujeto obligado** | Senado de la República |
| **Legal obligation** | LGTAIP Art. 70 Frac. I |
| **What we need** | 1) International treaties full text; 2) SIL legislative tracking data; 3) Committee reports |
| **Status** | Not yet contacted |

---

### 6. SCJN (Suprema Corte de Justicia de la Nación)

| Field | Value |
|-------|-------|
| **Priority** | 5 |
| **Type** | Federal judicial (Poder Judicial) |
| **SJF** | https://sjf.scjn.gob.mx/ |
| **Buscador Jurídico** | https://bj.scjn.gob.mx/ |
| **JurisLex** | https://jurislex.scjn.gob.mx/ |
| **Transparency unit** | transparencia@cjf.gob.mx |
| **PNT sujeto obligado** | Suprema Corte de Justicia de la Nación |
| **Legal obligation** | Art. 6 Constitucional; LGTAIP Art. 70 |
| **What we need** | 1) Jurisprudencia + tesis aisladas bulk download or API; 2) Epoch-separated data; 3) Structured metadata (materia, instancia, type) |
| **Status** | Not yet contacted |

**Notes**: ~500,000+ judicial instruments. SJF has search functionality but no documented bulk download API. Rate limiting and CAPTCHAs reported by researchers. Partnership approach likely more productive than scraping.

---

### 7. Secretaría Anticorrupción y Buen Gobierno

| Field | Value |
|-------|-------|
| **Priority** | Reference |
| **Type** | Federal government (successor to dissolved INAI) |
| **Program** | "Transparencia para el Pueblo" |
| **Legal obligation** | Handles federal FOIA appeals (former INAI mandate) |
| **What we need** | Understanding of new appeal procedures post-INAI dissolution |
| **Status** | New entity (March 2025) — procedures still being established |

**Notes**: This entity inherited INAI's transparency oversight role. 19 of 32 state transparency bodies were also dissolved. FOIA requests are still filed through PNT, but appeals now route to this body for federal matters.

---

## State Congresses (32 States)

Each state congress is a sujeto obligado under LGTAIP Art. 70 and must publish its marco normativo.

### Congress Portal Directory

| # | State | Congress Portal | OJN Poder 2 Count | Dead Links | Priority |
|---|-------|-----------------|--------------------|------------|----------|
| 1 | Aguascalientes | congresoags.gob.mx | 199 | 0 | 3 |
| 2 | Baja California | congresobc.gob.mx | 253 | 0 | 2 |
| 3 | Baja California Sur | cbcs.gob.mx | 212 | 0 | 3 |
| 4 | Campeche | congresocam.gob.mx | 320 | 0 | 3 |
| 5 | Chiapas | congresochiapas.gob.mx | 356 | 0 | 3 |
| 6 | Chihuahua | congresochihuahua.gob.mx | 415 | 0 | 3 |
| 7 | Ciudad de México | congresocdmx.gob.mx | 501 | 0 | 3 |
| 8 | Coahuila | congresocoahuila.gob.mx | 398 | 0 | 3 |
| 9 | Colima | congresocol.gob.mx | 210 | 0 | 3 |
| 10 | Durango | congresodurango.gob.mx | 295 | 0 | 2 |
| 11 | Estado de México | legislacion.edomex.gob.mx | 612 | 141 | 1 |
| 12 | Guanajuato | congresogto.gob.mx | 356 | 0 | 3 |
| 13 | Guerrero | congresogro.gob.mx | 398 | 0 | 3 |
| 14 | Hidalgo | congreso-hidalgo.gob.mx | 298 | 0 | 2 |
| 15 | Jalisco | congresojal.gob.mx | 478 | 0 | 3 |
| 16 | Michoacán | congresomich.gob.mx | 856 | 504 | 1 |
| 17 | Morelos | congresomorelos.gob.mx | 312 | 0 | 3 |
| 18 | Nayarit | congresonayarit.gob.mx | 245 | 0 | 3 |
| 19 | Nuevo León | hcnl.gob.mx | 456 | 0 | 3 |
| 20 | Oaxaca | congresooaxaca.gob.mx | 398 | 0 | 3 |
| 21 | Puebla | congresopuebla.gob.mx | 478 | 0 | 3 |
| 22 | Querétaro | legislaturaqueretaro.gob.mx | 267 | 0 | 3 |
| 23 | Quintana Roo | congresoqroo.gob.mx | 234 | 0 | 2 |
| 24 | San Luis Potosí | congresosanluis.gob.mx | 356 | 47 | 2 |
| 25 | Sinaloa | congresosinaloa.gob.mx | 312 | 0 | 3 |
| 26 | Sonora | congresoson.gob.mx | 345 | 0 | 3 |
| 27 | Tabasco | congresotabasco.gob.mx | 298 | 0 | 3 |
| 28 | Tamaulipas | congresotamaulipas.gob.mx | 378 | 0 | 3 |
| 29 | Tlaxcala | congresotlaxcala.gob.mx | 234 | 0 | 3 |
| 30 | Veracruz | legisver.gob.mx | 523 | 0 | 3 |
| 31 | Yucatán | congresoyucatan.gob.mx | 345 | 0 | 3 |
| 32 | Zacatecas | congresozac.gob.mx | 256 | 0 | 3 |

### Priority States (for direct outreach)

| Priority | State | Reason | Action |
|----------|-------|--------|--------|
| 1 | Michoacán | 504 dead links (largest gap) | Contact congress transparency unit + SEGOB |
| 1 | Estado de México | 141 dead links | Contact congress transparency unit |
| 2 | Baja California | Only 1 law scraped (253 expected) | Investigate OJN data, contact congress |
| 2 | Durango | Only 1 law scraped (295 expected) | Investigate OJN data, contact congress |
| 2 | Quintana Roo | Only 1 law scraped (234 expected) | Investigate OJN data, contact congress |
| 2 | Hidalgo | Only 38 laws scraped (298 expected) | Investigate OJN data, contact congress |
| 2 | San Luis Potosí | 47 dead links | Contact congress transparency unit |

---

## Academic Partners

### 8. UNAM — Instituto de Investigaciones Jurídicas (IIJ)

| Field | Value |
|-------|-------|
| **Priority** | 3 |
| **Type** | Academic |
| **URL** | https://www.juridicas.unam.mx/ |
| **Library** | Largest Mexican law library (physical + digital) |
| **Key programs** | Biblioteca Jurídica Virtual, InfoJus, editorial |
| **What we need** | 1) Cross-reference validation; 2) Historical legislation access; 3) Academic credibility |
| **Collaboration angle** | Research partnership on computational law, NLP on legal text |

---

### 9. CIDE (Centro de Investigación y Docencia Económicas)

| Field | Value |
|-------|-------|
| **Priority** | 4 |
| **Type** | Academic (CONACYT center) |
| **URL** | https://www.cide.edu/ |
| **Key programs** | Division of Public Administration, regulatory analysis |
| **What we need** | 1) Regulatory analysis datasets; 2) Public policy research collaboration |
| **Collaboration angle** | Regulatory impact analysis, legislative analytics |

---

### 10. ITAM (Instituto Tecnológico Autónomo de México)

| Field | Value |
|-------|-------|
| **Priority** | 4 |
| **Type** | Academic (private) |
| **URL** | https://www.itam.mx/ |
| **Key programs** | Law faculty, computational law interest |
| **What we need** | 1) Student/researcher contributors; 2) Technical validation |
| **Collaboration angle** | Computational law research, student projects |

---

## Civil Society Partners

### 11. Codeando México

| Field | Value |
|-------|-------|
| **Priority** | 3 |
| **Type** | Civil society / open data community |
| **URL** | https://codeandomexico.org/ |
| **What we need** | 1) Community visibility; 2) Contributor pipeline; 3) Open data advocacy support |
| **Collaboration angle** | Shared mission on open government data; community outreach |

---

### 12. Gobierno Fácil

| Field | Value |
|-------|-------|
| **Priority** | 4 |
| **Type** | Civil society / gov transparency tools |
| **URL** | https://gobiernofacil.com/ |
| **What we need** | 1) UX patterns for government data; 2) Cross-promotion |
| **Collaboration angle** | Complementary platforms — they simplify government interactions |

---

### 13. México Abierto

| Field | Value |
|-------|-------|
| **Priority** | 4 |
| **Type** | Civil society / open government advocacy |
| **What we need** | 1) Advocacy for government data openness; 2) Policy connections |
| **Collaboration angle** | Aligned mission on open government and transparency |

---

## Outreach Tracking

### Template Selection Guide

| Scenario | Template | Location |
|----------|----------|----------|
| Missing state legislation (Tier 2-3) | Template 1 | `docs/dataops/ESCALATION_PLAYBOOK.md` |
| Dead OJN links (Tier 2) | Template 2 | `docs/dataops/ESCALATION_PLAYBOOK.md` |
| Academic/institutional partnership (Tier 4) | Template 3 | `docs/dataops/ESCALATION_PLAYBOOK.md` |
| CONAMER regulatory data access | Template 4 | `docs/dataops/ESCALATION_PLAYBOOK.md` |

### Outreach Log

| Date | Institution | Contact Method | Template Used | Folio/Reference | Result |
|------|-------------|----------------|---------------|-----------------|--------|
| — | — | — | — | — | No outreach initiated yet |

> Track all outreach attempts in this table. For FOIA requests, always record the PNT folio number.
