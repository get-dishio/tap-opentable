"""OpenTable tap class."""

from __future__ import annotations

import typing as t
from pathlib import Path

from singer_sdk import Tap
from singer_sdk import typing as th

from tap_opentable import streams


class TapOpenTable(Tap):
    """OpenTable tap class."""

    name = "tap-opentable"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "client_id",
            th.StringType,
            required=True,
            description="Client ID for OpenTable API",
        ),
        th.Property(
            "client_secret",
            th.StringType,
            required=True,
            secret=True,
            description="Client Secret for OpenTable API",
        ),
        th.Property(
            "is_pre_production",
            th.BooleanType,
            default=True,
            description="Whether to use production or pre-production API",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.OpenTableStream]:
        """Return a list of discovered streams."""
        return [
            streams.RestaurantsStream(self),
            streams.ReservationsStream(self),
            streams.MenusStream(self),
            streams.AvailabilityStream(self),
            streams.ReviewsStream(self),
        ]
