"""REST client handling, including OpenTableStream base class."""

from __future__ import annotations

import json
import typing as t
from importlib import resources
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream

from tap_opentable.auth import OpenTableAuthenticator
from tap_opentable.pagination import OpenTablePaginator

if t.TYPE_CHECKING:
    from singer_sdk.helpers.types import Auth, Context


# Reference local JSON schema files.
SCHEMAS_DIR = resources.files(__package__) / "schemas"


class OpenTableStream(RESTStream):
    """OpenTable stream class."""

    @property
    def schema(self) -> dict:
        """Return the schema for this stream."""
        schema_path = SCHEMAS_DIR / f"{self.name}.json"
        with schema_path.open("r", encoding="utf-8") as schema_file:
            return json.load(schema_file)

    @property
    def authenticator(self):
        oauth_url = "https://oauth-pp.opentable.com" if self.config.get("is_pre_production") else "https://oauth.opentable.com"
        return OpenTableAuthenticator(self, self.config, auth_endpoint=oauth_url)

    @property
    def url_base(self) -> str:
        """Return the API URL root, using is_pre_production config to determine environment."""
        if self.config.get("is_pre_production"):
            return "https://platform.otqa.com"
        return "https://platform.opentable.com"

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params = {}
        
        # Add pagination if available
        if next_page_token:
            params["offset"] = next_page_token
            
        # Add date filtering if available and stream has a replication key
        if self.replication_key:
            start_date = self.get_starting_timestamp(context)
            if start_date:
                params["start_date"] = start_date.strftime("%Y-%m-%d")
                
        return params

    def get_new_paginator(self) -> OpenTablePaginator:
        """Create a new pagination helper instance."""
        return OpenTablePaginator(start_value=0, page_size=100)

    def parse_response(self, response: requests.Response) -> dict:
        """Parse the response and return an iterator of result records."""
        return response.json()
