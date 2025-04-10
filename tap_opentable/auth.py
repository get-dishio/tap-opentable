
"""OpenTable Authentication."""

from singer_sdk.authenticators import OAuthAuthenticator


class OpenTableAuthenticator(OAuthAuthenticator):
    """Authenticator class for OpenTable."""

    @property
    def oauth_request_body(self) -> dict:
        """Define the OAuth request body for OpenTable."""
        return {
            "grant_type": "client_credentials",
            "client_id": self.config.get("client_id"),
            "client_secret": self.config.get("client_secret"),
            "scope": "public",
        }

    def get_auth_headers(self) -> dict:
        """Return headers with bearer token."""
        return {"Authorization": f"Bearer {self.config.get('auth_token')}"}