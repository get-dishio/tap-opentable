"""Availability stream class."""

from __future__ import annotations
from datetime import datetime, timedelta
from typing import Optional

from tap_opentable.client import OpenTableStream
from tap_opentable.streams.restaurants import RestaurantsStream


class AvailabilityStream(OpenTableStream):
    """Stream for retrieving availability records from the OpenTable API."""

    name = "availability"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.availability[*]"
    parent_stream_type = RestaurantsStream

    @property
    def path(self) -> str:
        return f"/restaurants/{self.context.get('restaurant_id')}/availability"

    def get_url_params(self, context: Optional[dict], next_page_token: Optional[int]) -> dict:
        """Return a dictionary of values to be used in URL parameterization."""
        params = super().get_url_params(context, next_page_token)
        
        # Default to next 7 days availability
        today = datetime.now().date()
        params.update({
            "start_date": today.strftime("%Y-%m-%d"),
            "end_date": (today + timedelta(days=7)).strftime("%Y-%m-%d"),
            "party_size": 2,  # Default party size
        })

        return params 