"""
Management command to run the full data collection pipeline.

Usage:
    # Dispatch to Celery (detached, survives terminal close)
    docker-compose exec -d api python manage.py run_pipeline

    # Run synchronously (blocks, useful for debugging)
    docker-compose exec api python manage.py run_pipeline --local

    # Skip state scraping (saves ~12 hours)
    docker-compose exec api python manage.py run_pipeline --skip-states

    # Skip all scraping (use existing data)
    docker-compose exec api python manage.py run_pipeline --skip-scrape

    # Federal-only quick test
    docker-compose exec api python manage.py run_pipeline --local --skip-states --skip-municipal
"""

import json

from django.core.management.base import BaseCommand

from apps.api.tasks import PIPELINE_STATUS_FILE, _ensure_paths


class Command(BaseCommand):
    help = "Run the full data collection pipeline (scrape, parse, ingest, index)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--local",
            action="store_true",
            help="Run synchronously (blocks terminal), skip Celery dispatch",
        )
        parser.add_argument(
            "--skip-scrape",
            action="store_true",
            help="Skip all scraping phases (use existing data)",
        )
        parser.add_argument(
            "--skip-states",
            action="store_true",
            help="Skip state law scraping (longest phase, ~8-12 hours)",
        )
        parser.add_argument(
            "--skip-municipal",
            action="store_true",
            help="Skip municipal law scraping",
        )
        parser.add_argument(
            "--skip-index",
            action="store_true",
            help="Skip Elasticsearch indexing",
        )
        parser.add_argument(
            "--workers",
            type=int,
            default=4,
            help="Parallel workers for ingestion (default: 4)",
        )

    def handle(self, *args, **options):
        _ensure_paths()

        # Check if pipeline is already running
        if PIPELINE_STATUS_FILE.exists():
            try:
                with open(PIPELINE_STATUS_FILE, "r") as f:
                    current = json.load(f)
                if current.get("status") == "running":
                    self.stderr.write(
                        self.style.ERROR(
                            "Pipeline is already running! "
                            f"Phase: {current.get('phase', '?')} "
                            f"({current.get('progress', '?')}%)"
                        )
                    )
                    return
            except (json.JSONDecodeError, OSError):
                pass

        params = {
            "skip_scrape": options["skip_scrape"],
            "skip_states": options["skip_states"],
            "skip_municipal": options["skip_municipal"],
            "skip_index": options["skip_index"],
            "workers": options["workers"],
        }

        # Display plan
        self.stdout.write("=" * 60)
        self.stdout.write("DATA COLLECTION PIPELINE")
        self.stdout.write("=" * 60)

        from apps.api.tasks import _build_pipeline_phases

        phases = _build_pipeline_phases(params)
        for i, phase in enumerate(phases, 1):
            self.stdout.write(f"  Phase {i}: {phase['name']}")
        self.stdout.write(f"\nTotal phases: {len(phases)}")
        self.stdout.write(f"Workers: {options['workers']}")
        self.stdout.write(
            f"Mode: {'local (synchronous)' if options['local'] else 'Celery (background)'}"
        )
        self.stdout.write("=" * 60)

        if options["local"]:
            self.stdout.write("\nRunning pipeline locally (synchronous)...")
            from apps.api.tasks import run_full_pipeline

            result = run_full_pipeline(params)
            self.stdout.write(f"\nPipeline {result['status']}:")
            summary = result.get("summary", {})
            self.stdout.write(
                f"  {summary.get('succeeded', 0)}/{summary.get('total_phases', 0)} "
                f"phases succeeded"
            )
            if result.get("duration_human"):
                self.stdout.write(f"  Duration: {result['duration_human']}")

            # Show failed phases
            for pr in result.get("phase_results", []):
                if pr.get("status") != "success":
                    self.stderr.write(
                        self.style.ERROR(
                            f"  FAILED: {pr['phase']} — {pr.get('error', 'exit code ' + str(pr.get('returncode')))}"
                        )
                    )
        else:
            from apps.api.tasks import run_full_pipeline

            task = run_full_pipeline.delay(params)
            self.stdout.write(self.style.SUCCESS(f"\nPipeline dispatched to Celery!"))
            self.stdout.write(f"Task ID: {task.id}")
            self.stdout.write(
                f"\nMonitor progress:"
                f"\n  curl http://localhost:8000/api/v1/admin/pipeline/status/"
                f"\n  tail -f data/logs/pipeline.log"
            )
