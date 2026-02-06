from rest_framework.throttling import AnonRateThrottle


class SearchRateThrottle(AnonRateThrottle):
    """Stricter throttle for the search endpoint."""

    scope = "search"
