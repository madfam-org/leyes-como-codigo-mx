"""Seed RoadmapItem table with the initial expansion roadmap (17 items, 4 phases)."""

from django.core.management.base import BaseCommand

from apps.scraper.dataops.models import RoadmapItem

ROADMAP_ITEMS = [
    # ── Phase 1: Quick Wins ────────────────────────────────────────
    {
        "phase": 1,
        "title": "Fix 4,438 non-legislative parse failures",
        "description": "Retry failed OJN downloads with exponential backoff; OCR pipeline for image-based PDFs. Michoacán 2,291, SLP ~700, EDOMEX ~600, BC ~200.",
        "category": "fix",
        "estimated_laws": 4438,
        "estimated_effort": "medium",
        "priority": 1,
        "sort_order": 1,
    },
    {
        "phase": 1,
        "title": "Build OCR pipeline for scanned PDFs",
        "description": "Tesseract/PaddleOCR pipeline for image-based PDFs that failed text extraction. Integrate into existing parse flow.",
        "category": "infrastructure",
        "estimated_laws": 500,
        "estimated_effort": "medium",
        "priority": 2,
        "sort_order": 2,
    },
    {
        "phase": 1,
        "title": "Build Cámara de Diputados reglamentos scraper",
        "description": "Scrape ~800 federal regulations from diputados.gob.mx/LeyesBiblio/regla.htm. Similar structure to existing federal scraper.",
        "category": "scraper",
        "estimated_laws": 800,
        "estimated_effort": "medium",
        "priority": 2,
        "sort_order": 3,
    },
    {
        "phase": 1,
        "title": "Investigate BC, Durango, QR, Hidalgo low counts",
        "description": "These states have suspiciously low law counts on OJN (1-38 laws). Search state congress portals for alternative sources.",
        "category": "investigation",
        "estimated_laws": 650,
        "estimated_effort": "low",
        "priority": 3,
        "sort_order": 4,
    },
    # ── Phase 2: Institutional Outreach ────────────────────────────
    {
        "phase": 2,
        "title": "Contact SEGOB about 782 dead OJN links",
        "description": "File transparency request (FOIA) with SEGOB about permanent dead links on OJN. Use Escalation Playbook Template 1.",
        "category": "outreach",
        "estimated_laws": 782,
        "estimated_effort": "low",
        "priority": 1,
        "sort_order": 1,
    },
    {
        "phase": 2,
        "title": "State congress outreach for low-count states",
        "description": "Contact congresses of Durango, QR, BC, Hidalgo directly for their full legislative catalogs. Use Template 2.",
        "category": "outreach",
        "estimated_laws": 400,
        "estimated_effort": "medium",
        "priority": 2,
        "sort_order": 2,
    },
    {
        "phase": 2,
        "title": "CONAMER data access request",
        "description": "Request API access or bulk data export from CONAMER CNARTyS catalog (113,373 regulations). Use Template 4.",
        "category": "outreach",
        "estimated_laws": 0,
        "estimated_effort": "low",
        "priority": 2,
        "sort_order": 3,
    },
    {
        "phase": 2,
        "title": "State gazette partnerships (Periódicos Oficiales)",
        "description": "Approach 5 pilot state gazette offices for digital archive access. Start with states that have active transparency institutes.",
        "category": "partnership",
        "estimated_laws": 250,
        "estimated_effort": "high",
        "priority": 3,
        "sort_order": 4,
    },
    # ── Phase 3: New Scrapers ──────────────────────────────────────
    {
        "phase": 3,
        "title": "CONAMER CNARTyS scraper",
        "description": "Build scraper for cnartys.conamer.gob.mx API. 113,373 regulations across federal and state secondary instruments. May overlap with existing data.",
        "category": "scraper",
        "estimated_laws": 113373,
        "estimated_effort": "high",
        "priority": 1,
        "sort_order": 1,
    },
    {
        "phase": 3,
        "title": "DOF daily gazette monitor",
        "description": "Complete the dof_daily.py stub scraper. Monitor daily DOF publications for new/amended laws and regulations.",
        "category": "scraper",
        "estimated_laws": 500,
        "estimated_effort": "medium",
        "priority": 2,
        "sort_order": 2,
    },
    {
        "phase": 3,
        "title": "Municipal tier-2 expansion (15 cities)",
        "description": "Build scrapers for next 15 most important municipalities by population. Estimated 100-200 regulations per city.",
        "category": "scraper",
        "estimated_laws": 2000,
        "estimated_effort": "high",
        "priority": 3,
        "sort_order": 3,
    },
    {
        "phase": 3,
        "title": "NOMs (Normas Oficiales Mexicanas) scraper",
        "description": "Build scraper for official Mexican standards. Source: gob.mx/conamer or sinec.gob.mx. Estimated 4,000+ NOMs.",
        "category": "scraper",
        "estimated_laws": 4000,
        "estimated_effort": "high",
        "priority": 3,
        "sort_order": 4,
    },
    # ── Phase 4: Partnerships ──────────────────────────────────────
    {
        "phase": 4,
        "title": "SCJN judicial corpus partnership",
        "description": "Establish data partnership with SCJN for jurisprudencia (60,000) and tesis aisladas (440,000). Requires institutional agreement.",
        "category": "partnership",
        "estimated_laws": 500000,
        "estimated_effort": "high",
        "priority": 1,
        "sort_order": 1,
    },
    {
        "phase": 4,
        "title": "SRE international treaties scraper",
        "description": "Build scraper for tratados.sre.gob.mx. ~1,500 bilateral and multilateral treaties ratified by Mexico.",
        "category": "scraper",
        "estimated_laws": 1500,
        "estimated_effort": "medium",
        "priority": 2,
        "sort_order": 2,
    },
    {
        "phase": 4,
        "title": "SIL legislative reform tracking",
        "description": "Integrate with Sistema de Información Legislativa for real-time reform tracking. Requires API access from Senado.",
        "category": "partnership",
        "estimated_laws": 0,
        "estimated_effort": "high",
        "priority": 3,
        "sort_order": 3,
    },
    {
        "phase": 4,
        "title": "IIJ-UNAM academic partnership",
        "description": "Establish partnership with Instituto de Investigaciones Jurídicas (UNAM) for curated legal corpus access and quality validation.",
        "category": "partnership",
        "estimated_laws": 0,
        "estimated_effort": "medium",
        "priority": 4,
        "sort_order": 4,
    },
    {
        "phase": 4,
        "title": "Computational law engine integration (Catala/OpenFisca)",
        "description": "Formalize partnership with Catala and OpenFisca teams for Mexican tax/labor law encoding. Experimental/blocked pending upstream support.",
        "category": "infrastructure",
        "estimated_laws": 0,
        "estimated_effort": "high",
        "priority": 5,
        "sort_order": 5,
    },
]


class Command(BaseCommand):
    help = (
        "Seed the RoadmapItem table with initial expansion roadmap (17 items, 4 phases)"
    )

    def handle(self, *args, **options):
        created = 0
        updated = 0

        for item_data in ROADMAP_ITEMS:
            obj, was_created = RoadmapItem.objects.get_or_create(
                phase=item_data["phase"],
                title=item_data["title"],
                defaults={
                    k: v for k, v in item_data.items() if k not in ("phase", "title")
                },
            )
            if was_created:
                created += 1
            else:
                updated += 1

        total = RoadmapItem.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Roadmap bootstrap complete: {created} created, {updated} existing, {total} total"
            )
        )
