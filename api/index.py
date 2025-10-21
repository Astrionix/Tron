from openrouter_client import DEFAULT_MODEL, chat_completion, ensure_api_key

def handler(request):
    ensure_api_key()
    if request.method != "POST":
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": _html_page(),
        }

    try:
        body = request.get_json() or {}
    except Exception:
        body = {}

    question = (body.get("question") or "").strip()
    if not question:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": '{"error": "Question is required"}',
        }

    try:
        answer = chat_completion(question=question, model=DEFAULT_MODEL)
    except Exception as exc:  # pragma: no cover
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": f'{{"error": "{str(exc)}"}}',
        }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": f'{{"answer": "{answer.replace("\\", "\\\\").replace("\"", "\\\"")}"}}',
    }


def _html_page() -> str:
    with open("templates/index.html", "r", encoding="utf-8") as template:
        return template.read()
