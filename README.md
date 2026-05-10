# reb-client

Python client for [한국부동산원 R-ONE OpenAPI](https://www.reb.or.kr/r-one/portal/openapi/openApiListPage.do) — one method per endpoint.

Each API endpoint is exposed as a plain Python method with a descriptive English name. No raw URLs, no opaque parameter strings, no need to read Korean documentation to figure out what a call does.

## Install

```bash
pip install reb-client
```

## Setup

Get an API key from [https://www.reb.or.kr/r-one/portal/openapi/openApiListPage.do](https://www.reb.or.kr/r-one/portal/openapi/openApiListPage.do) and set it as an environment variable:

```bash
export REB_API_KEY="your_api_key_here"
```

Or add it to a `.env` file (loaded automatically):

```
REB_API_KEY=your_api_key_here
```

## Usage

```python
from reb_client import RebClient

client = RebClient()

# Each endpoint is a method — results come back as a dict
result = client.list_stat_tables()
print(result)
```

## Available methods

3 methods total — one per endpoint.

| Method | Description |
|--------|-------------|
| `list_stat_tables` | 서비스 통계목록 |
| `list_stat_items` | 통계 세부항목 목록 |
| `get_stat_data` | 통계 조회 조건 설정 |


## Pagination

All list methods accept `page` and `page_size` keyword arguments:

```python
result = client.list_stat_tables(page=2, page_size=100)
```

Default page size: `100`.

## Error handling

```python
from reb_client.exceptions import APIKeyError, RateLimitError, NoDataFoundError

try:
    result = client.list_stat_tables()
except APIKeyError:
    print("Invalid or missing API key")
except RateLimitError:
    print("Rate limit exceeded — retry later")
except NoDataFoundError:
    print("No results for this query")
```

## API docs

Full method reference: [tlee0818.github.io/reb-client](https://tlee0818.github.io/reb-client/)

Source portal: [https://www.reb.or.kr/r-one/portal/openapi/openApiListPage.do](https://www.reb.or.kr/r-one/portal/openapi/openApiListPage.do)
