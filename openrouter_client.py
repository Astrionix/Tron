import os
from typing import Any, Dict, Optional
from openai import OpenAI

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "openai/gpt-oss-20b:free"


def create_client() -> OpenAI:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environment variable is not set")
    return OpenAI(base_url=OPENROUTER_BASE_URL, api_key=api_key)


def build_extra_headers(referer: Optional[str], title: Optional[str]) -> Dict[str, str]:
    headers: Dict[str, str] = {}
    if referer:
        headers["HTTP-Referer"] = referer
    if title:
        headers["X-Title"] = title
    return headers


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
