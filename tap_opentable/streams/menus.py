"""Menus stream class."""

from __future__ import annotations
from typing import Optional

from tap_opentable.client import OpenTableStream
from tap_opentable.streams.restaurants import RestaurantsStream


class MenusStream(OpenTableStream):
    """Stream for retrieving menu records from the OpenTable API."""

    name = "menus"
    primary_keys = ["id"]
    replication_key = "modified_at"
    records_jsonpath = "$.menus[*]"
    parent_stream_type = RestaurantsStream
    ignore_parent_replication_keys = True

    @property
    def path(self) -> str:
        return f"/restaurants/{self.context.get('restaurant_id')}/menus"

    def get_url_params(self, context: Optional[dict], next_page_token: Optional[int]) -> dict:
        """Return a dictionary of values to be used in URL parameterization."""
        params = super().get_url_params(context, next_page_token)
        return params

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return context for child streams."""
        return {
            "menu_id": record.get("id"),
            "restaurant_id": record.get("restaurant_id"),
        }