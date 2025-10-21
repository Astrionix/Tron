import os
import sys
from getpass import getpass
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from openai import OpenAI

ENV_FILE = Path(".env")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "openai/gpt-oss-20b:free"


def create_client() -> OpenAI:
    api_key = ensure_api_key()
    return OpenAI(base_url=OPENROUTER_BASE_URL, api_key=api_key)


def build_extra_headers(referer: Optional[str], title: Optional[str]) -> Dict[str, str]:
    headers: Dict[str, str] = {}
    if referer:
        headers["HTTP-Referer"] = referer
    if title:
        headers["X-Title"] = title
    return headers


def ensure_api_key() -> str:
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key:
        return api_key

    if sys.stdin.isatty():
        api_key = getpass("Enter OPENROUTER_API_KEY: ").strip()
        if not api_key:
            raise RuntimeError("OPENROUTER_API_KEY is required to continue")
        os.environ["OPENROUTER_API_KEY"] = api_key
        persist_api_key(api_key)
        return api_key

    raise RuntimeError("OPENROUTER_API_KEY environment variable is not set")


def persist_api_key(api_key: str) -> None:
    if not api_key:
        return

    existing: Dict[str, str] = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            if not line or line.strip().startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            existing[key.strip()] = value.strip()

    existing["OPENROUTER_API_KEY"] = api_key

    serialized = "\n".join(f"{key}={value}" for key, value in existing.items()) + "\n"
    ENV_FILE.write_text(serialized, encoding="utf-8")


def chat_completion(
    *,
    question: str,
    model: str = DEFAULT_MODEL,
    referer: Optional[str] = None,
    title: Optional[str] = None,
    extra_body: Optional[Dict[str, Any]] = None,
) -> str:
    client = create_client()
    completion = client.chat.completions.create(
        extra_headers=build_extra_headers(referer, title),
        extra_body=extra_body or {},
        model=model,
        messages=[{"role": "user", "content": question}],
    )
    return completion.choices[0].message.content
