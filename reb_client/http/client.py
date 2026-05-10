"""HTTP client for 한국부동산원 R-ONE OpenAPI — one method per endpoint."""

from __future__ import annotations

import xmltodict

from .. import config
from .base_http_client import BaseHttpClient

_LIST_STAT_TABLES = "https://www.reb.or.kr/r-one/openapi/SttsApiTbl.do"

_LIST_STAT_ITEMS = "https://www.reb.or.kr/r-one/openapi/SttsApiTblItm.do"

_GET_STAT_DATA = "https://www.reb.or.kr/r-one/openapi/SttsApiTblData.do"


def _p(d: dict) -> dict:
    """Drop None values — keeps API calls clean."""
    return {k: v for k, v in d.items() if v is not None}


def _parse_reb_xml(raw: str, root_element: str) -> dict:
    """Parse REB XML into a normalised dict with code/message/total_count/rows."""
    parsed = xmltodict.parse(raw, force_list=("row",))
    root = parsed.get(root_element, {})
    head = root.get("head", {})
    result = head.get("RESULT", {})
    return {
        "code": result.get("CODE", "INFO-000"),
        "message": result.get("MESSAGE", ""),
        "total_count": int(head.get("list_total_count", 0) or 0),
        "rows": root.get("row") or [],
    }


class RebClient(BaseHttpClient):
    """
    Client for 한국부동산원 R-ONE OpenAPI.
    Auth: KEY query param, injected automatically.
    Returns normalised dict.
    """

    def _call(
        self,
        url: str,
        params: dict,
        response_root: str | None = None,
    ) -> dict:
        extra = {
            "Type": "xml",
        }
        all_params = {
            "KEY": self._api_key or config.API_KEY,
            **extra,
            **params,
        }
        raw = self._raw_get(url, all_params)

        data = _parse_reb_xml(raw, response_root or "") if response_root else xmltodict.parse(raw)
        self._check_result_code(data)

        return data

    def list_stat_tables(
        self,
        statbl_id: str | None = None,
        page: int = 1,
        page_size: int = 100,
    ) -> dict:
        """서비스 통계목록 — OpenAPI 대상 통계목록을 제공합니다.


        Args:

            statbl_id (str, optional): 통계표ID

            page (int): Page number, 1-based.
            page_size (int): Results per page (default 100).



        Returns:
            dict with fields:

                STATBL_ID (string): 통계표ID

                STATBL_NM (string): 통계표명

                DTACYCLE_CD (string): 주기코드

                DTACYCLE_NM (string): 주기명

                STAT_ID (string): 통계메타ID

                TOP_ORG_NM (string): 제공기관

                OPEN_STATE (string): 공개여부

                DATA_START_YY (string): 통계자료 시작년도


                ... 5 more fields.




        Raises:

            300: 필수 값이 누락되어 있습니다. 요청인자를 참고 하십시오.

            290: 인증키가 유효하지 않습니다. 인증키가 없는 경우, 홈페이지에서 인증키를 신청하십시오.

            336: 데이터요청은 한번에 최대 1,000건을 넘을 수 없습니다.

            337: 일별 트래픽 제한을 넘은 호출입니다. 오늘은 더이상 호출할 수 없습니다.

            333: 요청위치 값의 타입이 유효하지 않습니다.요청위치 값은 정수를 입력하세요.


        """
        return self._call(
            _LIST_STAT_TABLES,
            _p(
                {
                    "STATBL_ID": statbl_id,
                    "pIndex": page,
                    "pSize": page_size,
                }
            ),
            response_root="SttsApiTbl",
        )

    def list_stat_items(
        self,
        statbl_id: str,
        itm_tag: str | None = None,
        page: int = 1,
        page_size: int = 100,
    ) -> dict:
        """통계 세부항목 목록 — 서비스 대상 통계의 세부 통계 항목을 제공합니다.


        Args:

            statbl_id (str): 통계표 ID

            itm_tag (str, optional): 항목정보

            page (int): Page number, 1-based.
            page_size (int): Results per page (default 100).



        Returns:
            dict with fields:

                STATBL_ID (string): 통계표 ID

                ITM_TAG (string): 항목정보

                ITM_ID (integer): 항목 ID

                PAR_ITM_ID (integer): 상위항목 ID

                ITM_NM (string): 항목명

                ITM_FULLNM (string): 항목전체명

                UI_NM (string): 단위명

                ITM_CMMT_IDTFR (string): 항목 주석 식별자


                ... 2 more fields.




        Raises:

            300: 필수 값이 누락되어 있습니다. 요청인자를 참고 하십시오.

            290: 인증키가 유효하지 않습니다. 인증키가 없는 경우, 홈페이지에서 인증키를 신청하십시오.

            336: 데이터요청은 한번에 최대 1,000건을 넘을 수 없습니다.

            337: 일별 트래픽 제한을 넘은 호출입니다. 오늘은 더이상 호출할 수 없습니다.

            333: 요청위치 값의 타입이 유효하지 않습니다.요청위치 값은 정수를 입력하세요.


        """
        return self._call(
            _LIST_STAT_ITEMS,
            _p(
                {
                    "STATBL_ID": statbl_id,
                    "ITM_TAG": itm_tag,
                    "pIndex": page,
                    "pSize": page_size,
                }
            ),
            response_root="SttsApiTblItm",
        )

    def get_stat_data(
        self,
        statbl_id: str,
        dtacycle_cd: str,
        wrttime_idtfr_id: str | None = None,
        grp_id: str | None = None,
        cls_id: str | None = None,
        itm_id: str | None = None,
        start_wrttime: str | None = None,
        end_wrttime: str | None = None,
        page: int = 1,
        page_size: int = 100,
    ) -> dict:
        """통계 조회 조건 설정 — 데이터 이용을 위한 조회조건 설정방법(통계코드, 통계명, 세부 항목명, 기간 등)을 제공합니다.


        Args:

            statbl_id (str): 통계표 ID

            dtacycle_cd (str): 주기코드

            wrttime_idtfr_id (str, optional): 자료작성 시점

            grp_id (str, optional): 그룹ID

            cls_id (str, optional): 분류ID

            itm_id (str, optional): 항목ID

            start_wrttime (str, optional): 자료작성 시점 시작일

            end_wrttime (str, optional): 자료작성 시점 종료일

            page (int): Page number, 1-based.
            page_size (int): Results per page (default 100).



        Returns:
            dict with fields:

                STATBL_ID (string): 통계표 ID

                DTACYCLE_CD (string): 주기코드

                WRTTIME_IDTFR_ID (string): 자료작성 시점

                GRP_ID (integer): 그룹ID

                GRP_NM (string): 그룹명

                CLS_ID (integer): 분류ID

                CLS_NM (string): 분류명

                ITM_ID (integer): 항목ID


                ... 7 more fields.




        Raises:

            300: 필수 값이 누락되어 있습니다. 요청인자를 참고 하십시오.

            290: 인증키가 유효하지 않습니다. 인증키가 없는 경우, 홈페이지에서 인증키를 신청하십시오.

            336: 데이터요청은 한번에 최대 1,000건을 넘을 수 없습니다.

            337: 일별 트래픽 제한을 넘은 호출입니다. 오늘은 더이상 호출할 수 없습니다.

            333: 요청위치 값의 타입이 유효하지 않습니다.요청위치 값은 정수를 입력하세요.


        """
        return self._call(
            _GET_STAT_DATA,
            _p(
                {
                    "STATBL_ID": statbl_id,
                    "DTACYCLE_CD": dtacycle_cd,
                    "WRTTIME_IDTFR_ID": wrttime_idtfr_id,
                    "GRP_ID": grp_id,
                    "CLS_ID": cls_id,
                    "ITM_ID": itm_id,
                    "START_WRTTIME": start_wrttime,
                    "END_WRTTIME": end_wrttime,
                    "pIndex": page,
                    "pSize": page_size,
                }
            ),
            response_root="SttsApiTblData",
        )
