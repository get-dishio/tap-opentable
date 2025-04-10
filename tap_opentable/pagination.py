"""REST API pagination handling."""

from singer_sdk.pagination import BaseOffsetPaginator


class OpenTablePaginator(BaseOffsetPaginator):
    """Paginator for OpenTable API that uses offset-based pagination."""

    def get_next(self, response):
        """Get the next page token from the response."""
        try:
            json_response = response.json()
            if json_response.get("reservations"):
                return self._value + self._page_size
        except Exception:
            return None
        return None
