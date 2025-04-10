"""Restaurant stream class."""

from __future__ import annotations

from tap_opentable.client import OpenTableStream


class RestaurantsStream(OpenTableStream):
    """Stream for retrieving restaurant records from the OpenTable API."""

    name = "restaurants"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.restaurants[*]"

    @property
    def path(self) -> str:
        return "/restaurants"

    def get_child_context(self, record: dict, context: dict) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "restaurant_id": record.get("id"),
        } 