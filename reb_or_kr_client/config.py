import os

from dotenv import load_dotenv

load_dotenv()


def _get(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


API_KEY: str = _get("REB_API_KEY")
REQUEST_TIMEOUT_SECONDS: int = int(_get("REQUEST_TIMEOUT_SECONDS", "30"))
MAX_RETRIES: int = int(_get("MAX_RETRIES", "3"))
