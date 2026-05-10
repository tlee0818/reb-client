__all__ = [
    "RebError",
    "APIKeyError",
    "RateLimitError",
    "APIResponseError",
    "InvalidParameterError",
    "MissingParameterError",
    "NoDataFoundError",
    "ServerSideError",
    "NetworkError",
]


class RebError(Exception):
    """Base exception for 한국부동산원 R-ONE OpenAPI client."""


class APIKeyError(RebError):
    """Invalid or missing API key."""


class RateLimitError(RebError):
    """Daily traffic limit exceeded."""


class APIResponseError(RebError):
    """Generic API error response."""


class InvalidParameterError(APIResponseError):
    """Invalid parameter value."""


class MissingParameterError(APIResponseError):
    """Required parameter missing."""


class NoDataFoundError(RebError):
    """No data found for the query."""


class ServerSideError(RebError):
    """Server-side error."""


class NetworkError(RebError):
    """Network or connection error."""
