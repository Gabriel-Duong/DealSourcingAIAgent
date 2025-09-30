Project overview and run instructions below.

# Project overview

* Purpose: Local RAG advisory chatbot using Ollama (local LLMs) + Chroma vectors.
* Components:

  * `data/` — source docs (PDF, TXT).
  * `ingest.py` — builds embeddings with `nomic-embed-text` and writes `chroma_db/`.
  * `chroma_db/` — persistent vector DB.
  * `server.py` — FastAPI RAG server (uses `nomic-embed-text` for embeddings and `gemma3:12b` for chat). Returns `{"model","embedding_model","answer"}`.
  * `run.py` — helper that launches uvicorn.
  * `requirements.txt` — Python deps.
  * (Optional) Open WebUI — chat frontend calling `server.py` `/ask` endpoint.

# Minimal `requirements.txt` (recommended)

```
fastapi
uvicorn[standard]
langchain-ollama
langchain-chroma
chromadb
pydantic
python-multipart
```

Adjust versions if you need reproducibility.

# Pre-requisites

1. Python 3.11+ and a virtualenv.
2. Ollama installed and running locally.
3. Open WebUI installed (if you plan to use it).
4. Pull required Ollama models:

```bash
ollama pull nomic-embed-text:latest
ollama pull gemma3:12b
# optional other chat models:
# ollama pull mistral:latest
```

# Setup — one time

```bash
# create virtualenv (if not already)
python -m venv .venv
source .venv/bin/activate

# install python deps
pip install -r requirements.txt
```

# Build vector DB (run every time you add/modify /data)

```bash
python ingest.py
# ingest.py should:
# - read files in ./data
# - create embeddings with model "nomic-embed-text:latest"
# - write persistent Chroma DB to ./chroma_db
```

# Start server

Preferred (uses run.py):

```bash
python run.py
```

Or directly:

```bash
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

# Quick tests

* Swagger UI: open `http://localhost:8000/docs` and try `/ask`.
* Curl:

```bash
curl -s -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"Summarize the fundraising process in my documents"}' | jq
```

Look for `"model"` and `"embedding_model"` fields and check `answer` text is grounded in your docs.

# Connect to Open WebUI

1. In Open WebUI → Settings → External Tools → Add Connection:

   * Type: `OpenAPI`
   * URL/Base URL: `http://localhost:8000`
   * OpenAPI Spec: `openapi.json`
   * Auth: `None`
2. In Open WebUI → Settings → Tools → Add Custom Tool (if needed):

   * Name: `RAG Advisory`
   * Method: `POST`
   * URL: `http://localhost:8000/ask`
   * Body template:

```json
{"question":"{{input}}"}
```

* Response mapping:

```
{{response.answer}}
```

3. Test in WebUI. If answers differ from Swagger, check WebUI tool response mapping and LLM system prompt settings.

# Important behaviors & troubleshooting

* Adding a file to `data/` does **not** auto-update embeddings. Run `python ingest.py` then restart server (or implement a `/reload` endpoint).
* If answers are generic:

  * Confirm `chroma_db/` is non-empty.
  * Confirm `ingest.py` used `nomic-embed-text`.
  * Confirm `server.py` uses the same `chroma_db` path and same embeddings class.
* Common errors:

  * `this model does not support embeddings` → embedding model wrong. Use `nomic-embed-text`.
  * Deprecation warnings → use `langchain-ollama` and `langchain-chroma` imports we discussed. They are warnings, not fatal.
  * Ollama not running or model not pulled → start Ollama and `ollama pull` the models.
* Debugging tips:

  * Compare direct LLM output vs RAG output to confirm grounding:

    ```python
    print("LLM only:", llm.invoke("What is inside my docs?"))
    print("RAG:", qa.invoke("What is inside my docs?"))
    ```
  * Use `--reload` when developing for automatic Python reloads.
