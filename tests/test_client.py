"""Tests for RebClient — endpoint routing, error handling."""

import httpx
import pytest
import respx

from reb_client.exceptions import APIKeyError, RateLimitError
from reb_client.http.client import RebClient
from tests.conftest import (
    FAKE_KEY,
    GET_STAT_DATA_XML,
    INVALID_KEY_XML,
    LIST_STAT_ITEMS_XML,
    LIST_STAT_TABLES_XML,
    RATE_LIMIT_XML,
)


@respx.mock
def test_list_stat_tables_hits_correct_endpoint():
    route = respx.get("https://www.reb.or.kr/r-one/openapi/SttsApiTbl.do").mock(
        return_value=httpx.Response(
            200,
            text=LIST_STAT_TABLES_XML,
        )
    )
    RebClient(FAKE_KEY).list_stat_tables()
    assert route.called


@respx.mock
def test_list_stat_tables_injects_auth_key():
    route = respx.get("https://www.reb.or.kr/r-one/openapi/SttsApiTbl.do").mock(
        return_value=httpx.Response(
            200,
            text=LIST_STAT_TABLES_XML,
        )
    )
    RebClient(FAKE_KEY).list_stat_tables()
    assert "KEY" in dict(route.calls[0].request.url.params)


@respx.mock
def test_list_stat_items_hits_correct_endpoint():
    route = respx.get("https://www.reb.or.kr/r-one/openapi/SttsApiTblItm.do").mock(
        return_value=httpx.Response(
            200,
            text=LIST_STAT_ITEMS_XML,
        )
    )
    RebClient(FAKE_KEY).list_stat_items(
        statbl_id="test_statbl_id",
    )
    assert route.called


@respx.mock
def test_list_stat_items_injects_auth_key():
    route = respx.get("https://www.reb.or.kr/r-one/openapi/SttsApiTblItm.do").mock(
        return_value=httpx.Response(
            200,
            text=LIST_STAT_ITEMS_XML,
        )
    )
    RebClient(FAKE_KEY).list_stat_items(
        statbl_id="test_statbl_id",
    )
    assert "KEY" in dict(route.calls[0].request.url.params)


@respx.mock
def test_get_stat_data_hits_correct_endpoint():
    route = respx.get("https://www.reb.or.kr/r-one/openapi/SttsApiTblData.do").mock(
        return_value=httpx.Response(
            200,
            text=GET_STAT_DATA_XML,
        )
    )
    RebClient(FAKE_KEY).get_stat_data(
        statbl_id="test_statbl_id",
        dtacycle_cd="test_dtacycle_cd",
    )
    assert route.called


@respx.mock
def test_get_stat_data_injects_auth_key():
    route = respx.get("https://www.reb.or.kr/r-one/openapi/SttsApiTblData.do").mock(
        return_value=httpx.Response(
            200,
            text=GET_STAT_DATA_XML,
        )
    )
    RebClient(FAKE_KEY).get_stat_data(
        statbl_id="test_statbl_id",
        dtacycle_cd="test_dtacycle_cd",
    )
    assert "KEY" in dict(route.calls[0].request.url.params)


@respx.mock
def test_raises_rate_limit_error():
    respx.get("https://www.reb.or.kr/r-one/openapi/SttsApiTbl.do").mock(
        return_value=httpx.Response(
            200,
            text=RATE_LIMIT_XML,
        )
    )
    with pytest.raises(RateLimitError):
        RebClient(FAKE_KEY).list_stat_tables()


@respx.mock
def test_raises_api_key_error():
    respx.get("https://www.reb.or.kr/r-one/openapi/SttsApiTbl.do").mock(
        return_value=httpx.Response(
            200,
            text=INVALID_KEY_XML,
        )
    )
    with pytest.raises(APIKeyError):
        RebClient(FAKE_KEY).list_stat_tables()
