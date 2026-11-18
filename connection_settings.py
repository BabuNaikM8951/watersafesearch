
import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse

# Load .env from the project directory
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", override=True)


def protocol() -> str:
    return os.getenv("OPENSEARCH_PROTOCOL", "http").strip()


def use_ssl() -> bool:
    return protocol().lower() == "https"


def username() -> str:
    return os.getenv("OPENSEARCH_USERNAME", "").strip()


def password() -> str:
    return os.getenv("OPENSEARCH_PASSWORD", "")


def connection_url() -> str:
    url = os.getenv("OPENSEARCH_URL", "").strip()

    if not url:
        raise ValueError("OPENSEARCH_URL is missing from .env")

    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("Invalid OPENSEARCH_URL")

    return url.rstrip("/") + "/"


def auth():
    if username() and password():
        return (username(), password())
    return None


def index_prefix() -> str:
    if username() and password():
        return f"{username()}-"
    return ""
