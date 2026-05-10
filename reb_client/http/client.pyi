"""Type stubs for RebClient — enables IDE autocompletion."""

from .http.base_http_client import BaseHttpClient

class RebClient(BaseHttpClient):
    def __init__(self, api_key: str | None = None) -> None: ...
    def list_stat_tables(
        self,
        statbl_id: str | None = ...,
        page: int = ...,
        page_size: int = ...,
    ) -> dict: ...
    def list_stat_items(
        self,
        statbl_id: str,
        itm_tag: str | None = ...,
        page: int = ...,
        page_size: int = ...,
    ) -> dict: ...
    def get_stat_data(
        self,
        statbl_id: str,
        dtacycle_cd: str,
        wrttime_idtfr_id: str | None = ...,
        grp_id: str | None = ...,
        cls_id: str | None = ...,
        itm_id: str | None = ...,
        start_wrttime: str | None = ...,
        end_wrttime: str | None = ...,
        page: int = ...,
        page_size: int = ...,
    ) -> dict: ...
