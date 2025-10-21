import argparse

from openrouter_client import DEFAULT_MODEL, chat_completion


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Query OpenRouter chat completions")
    parser.add_argument("question", nargs="?", help="Question to ask the model")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model identifier to use")
    parser.add_argument("--referer", help="Optional HTTP referer header value")
    parser.add_argument("--title", help="Optional title header value")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    question = args.question or input("Enter your question: ").strip()
    if not question:
        raise RuntimeError("A question must be provided either as an argument or via prompt input")
    answer = chat_completion(
        question=question,
        model=args.model,
        referer=args.referer,
        title=args.title,
    )
    print(answer)


if __name__ == "__main__":
    main()
