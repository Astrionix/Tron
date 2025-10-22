# TRON-CHATBOT

TRON Space Console web interface for interacting with OpenRouter-powered chat completions.

## Setup
- **Install dependencies**
  ```bash
  pip install -r requirements.txt
  ```
- **Run locally**
  ```bash
  python app.py
  ```
  The first time the app starts it prompts for `OPENROUTER_API_KEY` if it is not already set. The provided key is saved to `.env` for future runs.
- **Environment variable**
  You can also set the key manually via shell or the `.env` file:
  ```env
  OPENROUTER_API_KEY=sk-or-...
  ```
\
