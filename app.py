from flask import Flask, Response, jsonify, render_template, request

from openrouter_client import DEFAULT_MODEL, chat_completion

app = Flask(__name__)


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask() -> Response:
    data = request.get_json(force=True, silent=True) or {}
    question = (data.get("question") or "").strip()

    if not question:
        return jsonify({"error": "Question is required"}), 400

    try:
        answer = chat_completion(
            question=question,
            model=DEFAULT_MODEL,
        )
    except Exception as exc:  # pragma: no cover - surface backend errors to UI
        return jsonify({"error": str(exc)}), 500

    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(debug=True)
