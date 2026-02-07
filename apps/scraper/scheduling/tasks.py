"""
Celery tasks for scheduled data operations.

These tasks are registered with Celery Beat via CELERY_BEAT_SCHEDULE
in settings.py.
"""

import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(name="dataops.run_health_checks")
def run_health_checks(sources="critical"):
    """Run health checks on data sources.

    Args:
        sources: "critical" for daily checks, "all" for full audit
    """
    from apps.scraper.dataops.health_monitor import HealthMonitor

    monitor = HealthMonitor()
    critical_only = sources == "critical"
    results = monitor.check_all(critical_only=critical_only)

    summary = monitor.get_summary()
    down_sources = [r.source_name for r in results if r.status == "down"]

    if down_sources:
        logger.warning("Sources DOWN: %s", ", ".join(down_sources))

    logger.info(
        "Health check complete (%s): %d healthy, %d degraded, %d down",
        sources,
        summary["healthy"],
        summary["degraded"],
        summary["down"],
    )
    return summary


@shared_task(name="dataops.detect_staleness")
def detect_staleness(max_age_days=90):
    """Find laws with stale source verification."""
    from apps.scraper.dataops.health_monitor import HealthMonitor

    monitor = HealthMonitor()
    stale = monitor.detect_staleness(max_age_days=max_age_days)
    count = stale.count()

    logger.info("Staleness check: %d laws older than %d days", count, max_age_days)
    return {"stale_count": count, "max_age_days": max_age_days}


@shared_task(name="dataops.retry_transient_failures")
def retry_transient_failures():
    """Retry gaps that are still at Tier 0 (transient failures)."""
    from apps.scraper.dataops.models import GapRecord

    transient_gaps = GapRecord.objects.filter(
        status="open",
        current_tier=0,
        gap_type="dead_link",
    )

    count = transient_gaps.count()
    logger.info("Found %d transient failures to retry", count)

    # Mark them for re-processing (actual retry requires scraper integration)
    for gap in transient_gaps:
        gap.attempts.append(
            {
                "tier": 0,
                "action": "Scheduled retry of transient failure",
                "date": __import__("django").utils.timezone.now().isoformat(),
                "result": "pending",
            }
        )
        gap.save(update_fields=["attempts", "updated_at"])

    return {"retried": count}


@shared_task(name="dataops.generate_coverage_report")
def generate_coverage_report():
    """Generate and log monthly coverage metrics."""
    from apps.scraper.dataops.coverage_dashboard import CoverageDashboard

    dashboard = CoverageDashboard()
    report = dashboard.full_report()

    summary = report["summary"]
    logger.info(
        "Monthly coverage: %d in DB, %d scraped, %d gaps (%d actionable)",
        summary["total_in_db"],
        summary["total_scraped"],
        summary["total_gaps"],
        summary["actionable_gaps"],
    )
    return summary


@shared_task(name="dataops.check_dof_daily")
def check_dof_daily():
    """Check today's DOF edition for law changes.

    Runs daily at 7 AM via Celery Beat. Fetches the DOF index,
    detects reforms/new laws/abrogations, and logs findings.
    """
    import datetime

    from apps.scraper.federal.dof_daily import DofScraper

    scraper = DofScraper(date=datetime.date.today())
    results = scraper.run()

    entries = results.get("entries", [])
    changes = results.get("changes", [])

    # Log to AcquisitionLog
    try:
        from apps.scraper.dataops.models import AcquisitionLog

        log_entry = AcquisitionLog.objects.create(
            operation="dof_daily_check",
            parameters={"date": str(datetime.date.today())},
            found=len(entries),
            downloaded=0,
            failed=0,
            ingested=0,
        )
        if changes:
            log_entry.error_summary = (
                f"{len(changes)} law changes detected: "
                + ", ".join(c.get("change_type", "unknown") for c in changes[:5])
            )
        log_entry.finish()
    except Exception:
        pass

    if changes:
        logger.warning(
            "DOF daily: %d entries, %d law changes detected",
            len(entries),
            len(changes),
        )
        for change in changes[:10]:
            logger.warning(
                "  [%s] %s", change.get("change_type", "?"), change.get("title", "?")
            )
    else:
        logger.info("DOF daily: %d entries, no law changes detected", len(entries))

    return {
        "date": str(datetime.date.today()),
        "total_entries": len(entries),
        "law_changes": len(changes),
        "changes": changes[:20],
    }
