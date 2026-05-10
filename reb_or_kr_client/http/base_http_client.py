"""Shared HTTP base: retry logic, XML/JSON parsing, typed error raising."""

import asyncio
import logging
import time
from typing import Any

import httpx
import xmltodict

from ..config import MAX_RETRIES, REQUEST_TIMEOUT_SECONDS
from ..exceptions import (
    APIKeyError,
    APIResponseError,
    InvalidParameterError,
    MissingParameterError,
    NetworkError,
    NoDataFoundError,
    RateLimitError,
    RebError,
    ServerSideError,
)

logger = logging.getLogger(__name__)

_RETRYABLE_STATUS = {429, 500, 502, 503, 504}


def _parse_response(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("<"):
        return xmltodict.parse(raw)

    import json

    return json.loads(raw)


def _check_result_code(data: dict) -> None:
    """Raise typed exceptions for REB error codes.

    Expects data in the normalised form: {code, message, total_count, rows}
    as produced by _parse_reb_xml in client.py.
    """
    code = data.get("code", "INFO-000")
    msg = data.get("message", "")
    if code == "INFO-000":
        return
    if code == "INFO-200":
        raise NoDataFoundError(f"No data found ({code}): {msg}")
    if code in ("INFO-300", "ERROR-290"):
        raise APIKeyError(f"API key error ({code}): {msg}")
    if code == "ERROR-300":
        raise MissingParameterError(f"Required parameter missing ({code}): {msg}")
    if code in ("ERROR-333", "ERROR-336"):
        raise InvalidParameterError(f"Invalid parameter ({code}): {msg}")
    if code == "ERROR-337":
        raise RateLimitError(f"Daily traffic limit exceeded ({code}): {msg}")
    if code == "ERROR-310":
        raise APIResponseError(f"Service not found ({code}): {msg}")
    if code in ("ERROR-500", "ERROR-600", "ERROR-601"):
        raise ServerSideError(f"Server error ({code}): {msg}")
    raise APIResponseError(f"API error ({code}): {msg}")


class BaseHttpClient:
    """Shared retry/parse/error logic. Subclasses inject auth and base URL."""

    def __init__(self, api_key: str | None = None) -> None:
        self._api_key = api_key

    def _raw_get(self, url: str, params: dict[str, Any]) -> str:
        """Execute GET with retry logic. Returns raw response text on success."""
        attempt = 0
        last_exc: Exception | None = None

        while attempt <= MAX_RETRIES:
            try:
                logger.debug("GET %s params=%s attempt=%d", url, params, attempt + 1)
                with httpx.Client(timeout=REQUEST_TIMEOUT_SECONDS) as client:
                    resp = client.get(url, params=params)

                if resp.status_code in _RETRYABLE_STATUS:
                    wait = 2**attempt
                    logger.warning("HTTP %d — retrying in %ds", resp.status_code, wait)
                    time.sleep(wait)
                    attempt += 1
                    continue

                resp.raise_for_status()
                return resp.text

            except (RebError,):
                raise
            except httpx.ConnectError as exc:
                raise NetworkError(f"Network error: could not connect to {url} — {exc}") from exc
            except httpx.TimeoutException as exc:
                raise NetworkError(
                    f"Network error: request to {url} timed out after {REQUEST_TIMEOUT_SECONDS}s — {exc}"
                ) from exc
            except httpx.RemoteProtocolError as exc:
                raise NetworkError(
                    f"Network error: server at {url} returned an invalid response — {exc}"
                ) from exc
            except httpx.HTTPStatusError as exc:
                last_exc = exc
                if exc.response.status_code not in _RETRYABLE_STATUS:
                    raise APIResponseError(str(exc)) from exc
            except httpx.RequestError as exc:
                last_exc = exc
                wait = 2**attempt
                logger.warning("Request error: %s — retrying in %ds", exc, wait)
                time.sleep(wait)

            attempt += 1

        raise NetworkError(f"Network error: {last_exc}") from last_exc

    def _get(self, url: str, params: dict[str, Any]) -> dict:
        raw = self._raw_get(url, params)
        data = _parse_response(raw)
        _check_result_code(data)
        return data

    async def _aget(self, url: str, params: dict[str, Any]) -> dict:
        attempt = 0
        last_exc: Exception | None = None

        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
            while attempt <= MAX_RETRIES:
                try:
                    logger.debug("GET %s params=%s attempt=%d", url, params, attempt + 1)
                    resp = await client.get(url, params=params)

                    if resp.status_code in _RETRYABLE_STATUS:
                        wait = 2**attempt
                        logger.warning("HTTP %d — retrying in %ds", resp.status_code, wait)
                        await asyncio.sleep(wait)
                        attempt += 1
                        continue

                    resp.raise_for_status()
                    data = _parse_response(resp.text)
                    _check_result_code(data)
                    return data

                except (RebError,):
                    raise
                except httpx.ConnectError as exc:
                    raise NetworkError(
                        f"Network error: could not connect to {url} — {exc}"
                    ) from exc
                except httpx.TimeoutException as exc:
                    raise NetworkError(
                        f"Network error: request to {url} timed out after {REQUEST_TIMEOUT_SECONDS}s — {exc}"
                    ) from exc
                except httpx.RemoteProtocolError as exc:
                    raise NetworkError(
                        f"Network error: server at {url} returned an invalid response — {exc}"
                    ) from exc
                except httpx.HTTPStatusError as exc:
                    last_exc = exc
                    if exc.response.status_code not in _RETRYABLE_STATUS:
                        raise APIResponseError(str(exc)) from exc
                except httpx.RequestError as exc:
                    last_exc = exc
                    wait = 2**attempt
                    logger.warning("Request error: %s — retrying in %ds", exc, wait)
                    await asyncio.sleep(wait)

                attempt += 1

        raise NetworkError(f"Network error: {last_exc}") from last_exc

    def _check_result_code(self, data: dict) -> None:
        """Instance method wrapper — delegates to module-level _check_result_code."""
        _check_result_code(data)
