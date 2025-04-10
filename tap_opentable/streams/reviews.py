"""Reviews stream class."""

from typing import Optional

from tap_opentable.client import OpenTableStream
from tap_opentable.streams.restaurants import RestaurantsStream
from tap_opentable.pagination import OpenTablePaginator


class ReviewsStream(OpenTableStream):
    """Reviews stream."""

    name = "reviews"
    path = "/restaurants/{restaurant_id}/reviews"
    primary_keys = ["id"]
    replication_key = "dined_at"
    parent_stream_type = RestaurantsStream
    records_jsonpath = "$.reviews[*]"

    def get_new_paginator(self) -> OpenTablePaginator:
        """Create a new pagination helper instance."""
        return OpenTablePaginator() 