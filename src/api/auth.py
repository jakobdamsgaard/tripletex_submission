"""Authentication handling for Tripletex."""

import logging
from typing import Optional
import base64

logger = logging.getLogger(__name__)


def create_basic_auth_header(company_id: str, session_token: str) -> str:
    """Create Basic authentication header.

    Args:
        company_id: Target company ID (0 for own company)
        session_token: Session token from API

    Returns:
        Authorization header value
    """
    auth_string = f"{company_id}:{session_token}"
    encoded = base64.b64encode(auth_string.encode()).decode()
    return f"Basic {encoded}"


def parse_auth_header(auth_header: str) -> tuple[str, str]:
    """Parse Basic authentication header.

    Args:
        auth_header: Authorization header value (e.g., "Basic ...")

    Returns:
        Tuple of (company_id, session_token)

    Raises:
        ValueError: If header is invalid
    """
    if not auth_header.startswith("Basic "):
        raise ValueError("Invalid authentication header format")

    try:
        encoded = auth_header[6:]  # Remove "Basic " prefix
        decoded = base64.b64decode(encoded).decode()
        company_id, session_token = decoded.split(":", 1)
        return company_id, session_token
    except Exception as e:
        raise ValueError(f"Failed to parse authentication header: {e}") from e


class AuthManager:
    """Manage Tripletex authentication tokens."""

    def __init__(self, consumer_token: Optional[str] = None, employee_token: Optional[str] = None):
        """Initialize auth manager.

        Args:
            consumer_token: Consumer token (optional)
            employee_token: Employee token (optional)
        """
        self.consumer_token = consumer_token
        self.employee_token = employee_token
        self._session_token_cache: Optional[str] = None

    async def get_session_token(self, api_client) -> str:
        """Get session token from API.

        Args:
            api_client: Tripletex API client

        Returns:
            Session token
        """
        if self._session_token_cache:
            return self._session_token_cache

        if not self.consumer_token or not self.employee_token:
            raise ValueError("Consumer and employee tokens required")

        # Create session token via API
        # POST /token/session/:create
        # This would need to be implemented in api_client

        logger.info("Session token created")
        return self._session_token_cache

    def clear_cache(self):
        """Clear cached session token."""
        self._session_token_cache = None
