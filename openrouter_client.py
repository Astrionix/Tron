from typing import Any, Dict, Optional
import os
from openai import OpenAI

# ------------------ CONFIG ------------------
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "openai/gpt-oss-20b:free"

# Directly set your API key here
API_KEY = os.getenv("OPENROUTER_API_KEY", "")

if not API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is not set")

# ------------------ CLIENT CREATION ------------------
client = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=API_KEY)


# ------------------ HELPERS ------------------
def build_extra_headers(referer: Optional[str], title: Optional[str]) -> Dict[str, str]:
    headers: Dict[str, str] = {}
    if referer:
        headers["HTTP-Referer"] = referer
    if title:
        headers["X-Title"] = title
    return headers


# ------------------ CHAT FUNCTION ------------------
def chat_completion(
    *,
    question: str,
    model: str = DEFAULT_MODEL,
    referer: Optional[str] = None,
    title: Optional[str] = None,
    extra_body: Optional[Dict[str, Any]] = None,
) -> str:
    try:
        completion = client.chat.completions.create(
            extra_headers=build_extra_headers(referer, title),
            extra_body=extra_body or {},
            model=model,
            messages=[{"role": "user", "content": question}],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


# ------------------ TEST ------------------
if __name__ == "__main__":
    question = "Hello! Can you summarize the plot of Romeo and Juliet?"
    response = chat_completion(question=question)
    print("Response from OpenRouter model:\n")
    print(response)
