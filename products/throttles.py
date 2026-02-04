from rest_framework.throttling import SimpleRateThrottle
from .utils import get_client_ip

class SearchThrottle(SimpleRateThrottle):
    scope = 'search'

    def get_cache_key(self, request, view):
        ident = get_client_ip(request)
        if not ident:
            return None  # DRF skips throttling safely

        # simple string key — DRF will use cache normally
        return f"search-{ident}"
