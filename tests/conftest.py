"""Shared fixtures and response bodies for all test modules."""

FAKE_KEY = "test_api_key_1234"


LIST_STAT_TABLES_XML = """<?xml version="1.0" encoding="UTF-8"?>
<SttsApiTbl>
  <head>
    <RESULT>
      <CODE>INFO-000</CODE>
      <MESSAGE>정상 처리되었습니다.</MESSAGE>
    </RESULT>
    <list_total_count>1</list_total_count>
  </head>
  <row>

    <STATBL_ID>test_value</STATBL_ID>

    <STATBL_NM>test_value</STATBL_NM>

    <DTACYCLE_CD>test_value</DTACYCLE_CD>

  </row>
</SttsApiTbl>"""


LIST_STAT_ITEMS_XML = """<?xml version="1.0" encoding="UTF-8"?>
<SttsApiTblItm>
  <head>
    <RESULT>
      <CODE>INFO-000</CODE>
      <MESSAGE>정상 처리되었습니다.</MESSAGE>
    </RESULT>
    <list_total_count>1</list_total_count>
  </head>
  <row>

    <STATBL_ID>test_value</STATBL_ID>

    <ITM_TAG>test_value</ITM_TAG>

    <ITM_ID>test_value</ITM_ID>

  </row>
</SttsApiTblItm>"""


GET_STAT_DATA_XML = """<?xml version="1.0" encoding="UTF-8"?>
<SttsApiTblData>
  <head>
    <RESULT>
      <CODE>INFO-000</CODE>
      <MESSAGE>정상 처리되었습니다.</MESSAGE>
    </RESULT>
    <list_total_count>1</list_total_count>
  </head>
  <row>

    <STATBL_ID>test_value</STATBL_ID>

    <DTACYCLE_CD>test_value</DTACYCLE_CD>

    <WRTTIME_IDTFR_ID>test_value</WRTTIME_IDTFR_ID>

  </row>
</SttsApiTblData>"""


# REB error fixtures — use the same root element as the first API
RATE_LIMIT_XML = """<?xml version="1.0" encoding="UTF-8"?>
<SttsApiTbl>
  <head>
    <RESULT>
      <CODE>ERROR-337</CODE>
      <MESSAGE>일별 트래픽 제한을 넘은 호출입니다.</MESSAGE>
    </RESULT>
    <list_total_count>0</list_total_count>
  </head>
</SttsApiTbl>"""

INVALID_KEY_XML = """<?xml version="1.0" encoding="UTF-8"?>
<SttsApiTbl>
  <head>
    <RESULT>
      <CODE>ERROR-290</CODE>
      <MESSAGE>인증키가 유효하지 않습니다.</MESSAGE>
    </RESULT>
    <list_total_count>0</list_total_count>
  </head>
</SttsApiTbl>"""
