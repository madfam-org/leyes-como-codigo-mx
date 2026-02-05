import json

from django.db.models import Count
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .ingestion_manager import IngestionManager
from .models import Law


@require_http_methods(["GET"])
def health_check(request):
    """
    Simple health check endpoint.
    Checks database connectivity.
    """
    try:
        # Simple DB check
        Law.objects.first()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
        return JsonResponse({"status": "unhealthy", "database": db_status}, status=503)

    return JsonResponse(
        {
            "status": "healthy",
            "database": db_status,
            "timestamp": timezone.now().isoformat(),
        }
    )


@require_http_methods(["GET"])
def system_metrics(request):
    """
    Returns aggregated system metrics for the dashboard.
    """
    try:
        # Total laws
        total_laws = Law.objects.count()

        # Breakdown by jurisdiction (tier)
        # Federal (tier=0/federal), State (tier=1/state), Municipal (tier=2/municipal)
        # Note: Model uses string values for 'tier' typically

        federal_count = (
            Law.objects.filter(tier="0").count()
            + Law.objects.filter(tier="federal").count()
        )
        state_count = (
            Law.objects.filter(tier="1").count()
            + Law.objects.filter(tier="state").count()
        )
        municipal_count = (
            Law.objects.filter(tier="2").count()
            + Law.objects.filter(tier="municipal").count()
        )

        # Breakdown by category (top 5)
        categories = list(
            Law.objects.values("category")
            .annotate(count=Count("category"))
            .order_by("-count")[:5]
        )

        # Quality distribution - not yet tracked per-law in the database.
        # Returns null to signal the frontend that real data is unavailable.
        quality_distribution = None

        return JsonResponse(
            {
                "total_laws": total_laws,
                "counts": {
                    "federal": federal_count,
                    "state": state_count,
                    "municipal": municipal_count,
                },
                "top_categories": categories,
                "quality_distribution": quality_distribution,
                "last_updated": timezone.now().isoformat(),
            }
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@require_http_methods(["GET"])
def job_status(request):
    """
    Returns the current status of the ingestion job.
    Uses IngestionManager to read the status file.
    """
    try:
        status = IngestionManager.get_status()
        return JsonResponse(status)
    except Exception as e:
        return JsonResponse(
            {
                "status": "error",
                "message": str(e),
                "timestamp": timezone.now().isoformat(),
            },
            status=500,
        )


@require_http_methods(["GET"])
def list_jobs(request):
    """
    Returns a list of recent jobs.
    Currently returns a single-item list with the current status
    since we don't have a persistent job history table yet.
    """
    try:
        current = IngestionManager.get_status()
        # Mocking a 'list' format for the frontend
        jobs = [{"id": "current", **current}]
        return JsonResponse({"jobs": jobs})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
