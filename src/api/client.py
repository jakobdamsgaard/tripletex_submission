"""Tripletex API client for making authenticated requests."""

import base64
import logging
import re
import unicodedata
from typing import Optional, Dict, Any, List
import httpx
from config.constants import (
    DEFAULT_TIMEOUT_SECONDS,
    STATUS_RATE_LIMIT,
)

logger = logging.getLogger(__name__)


def _clean_credential_value(value: Any) -> str:
    """Remove hidden control characters and surrounding whitespace."""
    if value is None:
        return ""

    text = str(value)
    cleaned_chars = []
    for char in text:
        category = unicodedata.category(char)
        if category.startswith("C"):
            continue
        cleaned_chars.append(char)

    text = "".join(cleaned_chars)
    return text.strip()


def _clean_url_value(value: Any) -> str:
    """Normalize URL values more aggressively than secrets."""
    text = _clean_credential_value(value)
    return re.sub(r"\s+", "", text)


class TripletexClient:
    """HTTP client for Tripletex API v2."""

    def __init__(
        self,
        api_url: str,
        session_token: str,
        company_id: str = "0",
        timeout: int = DEFAULT_TIMEOUT_SECONDS,
    ):
        """Initialize Tripletex client.

        Args:
            api_url: Base URL for Tripletex API
            session_token: Session token for authentication
            company_id: Target company ID (0 for own company)
            timeout: Request timeout in seconds
        """
        cleaned_api_url = _clean_url_value(api_url).rstrip("/")
        cleaned_session_token = _clean_credential_value(session_token)
        cleaned_company_id = _clean_credential_value(company_id) or "0"

        if not cleaned_api_url.startswith(("http://", "https://")):
            raise ValueError("Tripletex API URL must start with http:// or https://")

        self.api_url = cleaned_api_url
        self.session_token = cleaned_session_token
        self.company_id = cleaned_company_id
        self.timeout = timeout
        self._client = httpx.AsyncClient(timeout=timeout)

        # Prepare auth header
        auth_string = f"{self.company_id}:{self.session_token}"
        encoded = base64.b64encode(auth_string.encode()).decode()
        self.auth_header = f"Basic {encoded}"

        logger.info(f"TripletexClient initialized for company_id={self.company_id}")

    async def close(self):
        """Close the async client."""
        await self._client.aclose()

    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Make GET request to Tripletex API.

        Args:
            endpoint: API endpoint (without base URL)
            params: Query parameters
            fields: Fields to return (Tripletex fields parameter)

        Returns:
            Response data
        """
        query_params = params or {}
        if fields:
            query_params["fields"] = fields

        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        return await self._request("GET", url, params=query_params)

    async def post(
        self,
        endpoint: str,
        data: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make POST request to Tripletex API.

        Args:
            endpoint: API endpoint
            data: Request body
            params: Query parameters

        Returns:
            Response data
        """
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        return await self._request("POST", url, json=data, params=params)

    async def put(
        self,
        endpoint: str,
        data: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make PUT request to Tripletex API.

        Args:
            endpoint: API endpoint
            data: Request body
            params: Query parameters

        Returns:
            Response data
        """
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        return await self._request("PUT", url, json=data, params=params)

    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make DELETE request to Tripletex API.

        Args:
            endpoint: API endpoint

        Returns:
            Response data
        """
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        return await self._request("DELETE", url)

    async def _request(
        self,
        method: str,
        url: str,
        **kwargs,
    ) -> Dict[str, Any]:
        """Execute HTTP request with error handling.

        Args:
            method: HTTP method
            url: Full URL
            **kwargs: Additional arguments for httpx

        Returns:
            Response data
        """
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = self.auth_header
        headers["Content-Type"] = "application/json"

        try:
            response = await self._client.request(method, url, headers=headers, **kwargs)

            # Handle rate limiting
            if response.status_code == STATUS_RATE_LIMIT:
                logger.warning("Rate limit hit. Retry-After headers:")
                logger.warning(f"  X-Rate-Limit-Reset: {response.headers.get('X-Rate-Limit-Reset')}")
                raise RateLimitError("API rate limit exceeded")

            # Log rate limit information
            if "X-Rate-Limit-Remaining" in response.headers:
                remaining = response.headers.get("X-Rate-Limit-Remaining")
                logger.debug(f"API calls remaining: {remaining}")

            # Handle errors
            if response.status_code >= 400:
                error_data = response.json() if response.text else {}
                logger.error(
                    f"API Error {response.status_code}: {error_data.get('message', 'Unknown error')}"
                )
                raise APIError(response.status_code, error_data)

            # Return parsed response
            if response.status_code == 204:
                return {}

            return response.json() if response.text else {}

        except httpx.TimeoutException as e:
            logger.error(f"Request timeout: {e}")
            raise TimeoutError(f"Request to {url} timed out") from e
        except httpx.NetworkError as e:
            logger.error(f"Network error: {e}")
            raise ConnectionError(f"Network error: {e}") from e
        except httpx.InvalidURL as e:
            logger.error(f"Invalid URL: {url!r}")
            raise ValueError(f"Invalid Tripletex API URL: {url!r}") from e

    def get_headers(self) -> Dict[str, str]:
        """Get request headers."""
        return {
            "Authorization": self.auth_header,
            "Content-Type": "application/json",
        }


class APIError(Exception):
    """API error response."""

    def __init__(self, status_code: int, data: Dict[str, Any]):
        """Initialize API error.

        Args:
            status_code: HTTP status code
            data: Response data containing error details
        """
        self.status_code = status_code
        self.data = data
        self.code = data.get("code")
        self.message = data.get("message", "Unknown error")
        self.developer_message = data.get("developerMessage")
        self.validation_messages = data.get("validationMessages", [])
        super().__init__(f"API Error {status_code}: {self.message}")


class RateLimitError(Exception):
    """Rate limit exceeded."""

    pass


class TimeoutError(Exception):
    """Request timeout."""

    pass


class ConnectionError(Exception):
    """Connection error."""

    pass
