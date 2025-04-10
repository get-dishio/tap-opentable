"""Reservations stream class."""

from __future__ import annotations
from datetime import datetime
from typing import Optional

from tap_opentable.client import OpenTableStream
from tap_opentable.streams.restaurants import RestaurantsStream


class ReservationsStream(OpenTableStream):
    """Stream for retrieving reservation records from the OpenTable API."""

    name = "reservations"
    primary_keys = ["id"]
    replication_key = "modified_at"
    records_jsonpath = "$.reservations[*]"
    parent_stream_type = RestaurantsStream
    ignore_parent_replication_keys = True

    @property
    def path(self) -> str:
        return f"/restaurants/{self.context.get('restaurant_id')}/reservations"

    def get_url_params(self, context: Optional[dict], next_page_token: Optional[int]) -> dict:
        """Return a dictionary of values to be used in URL parameterization."""
        params = super().get_url_params(context, next_page_token)
        
        # Add date filtering
        start_date = self.get_starting_timestamp(context)
        if start_date:
            params["start_date"] = start_date.strftime("%Y-%m-%d")
            params["end_date"] = datetime.now().strftime("%Y-%m-%d")

        return params 