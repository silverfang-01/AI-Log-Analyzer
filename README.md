# 🔎 AI Log Analyzer (Free, Local)

A lightweight **Generative-AI-powered** log analyzer you can run entirely **for free** on your machine.  
Built with **FastAPI + ChromaDB + SentenceTransformers** and a **local LLM (Ollama)** — no paid APIs.

## Features
- **Upload** log files (text)
- **Parse & index** logs into a persistent vector DB (Chroma)
- **Semantic search** over logs (`/search`)
- **AI summaries & likely fixes** via local LLM (`/query`)
- **Structured report** without LLM (`/report`)
- **Idempotent indexing** (no duplicate vectors)
- **All local & free** (Windows-friendly)

## Tech Stack (Free)
- Backend: **FastAPI**, **Uvicorn**
- Embeddings: **SentenceTransformers** (`all-MiniLM-L6-v2`)
- Vector DB: **Chroma** (persistent)
- LLM: **Ollama** (e.g., `llama3.2:3b`) — optional but recommended
- Tooling: **uv** (dependency & env manager)

---

## Project Structure
log-analyzer-ai/
├─ backend/
│ ├─ init.py
│ ├─ main.py # API endpoints
│ ├─ preprocess.py # regex parsing -> DataFrame
│ ├─ vectorstore.py # Chroma persistence + idempotent add
│ ├─ anomaly.py # isolation forest (MVP)
│ ├─ ai_pipeline.py # Ollama HTTP client
├─ scripts/
│ └─ client.py # tiny CLI: upload/search/query
├─ frontend/
│ └─ app.py # (optional) Streamlit UI
├─ data/
│ ├─ init.py
│ └─ sample.log # example logs
├─ .chromadb/ # persisted vectors (ignored by git)
├─ README.md
├─ pyproject.toml
├─ uv.lock
└─ .gitignore

---

## Prerequisites
- **Python 3.11+**
- **uv** (https://docs.astral.sh/uv/)
- **Windows / macOS / Linux**
- Optional (for `/query`): **Ollama**
  - Windows:
    ```powershell
    winget install --id Ollama.Ollama -e
    # then reopen PowerShell
    ollama pull llama3.2:3b
    ollama serve
    ```
  - Verify: `curl http://localhost:11434/api/tags`

---

## Setup (with `uv`)
> Commands shown for **PowerShell**. On bash, drop the `.exe` suffixes.

```powershell
# install deps
uv add fastapi uvicorn chromadb sentence-transformers scikit-learn pandas requests python-multipart

# (optional) Streamlit UI
uv add streamlit


Run the API
uv run uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload


Health check:

curl.exe http://127.0.0.1:8000/health

Ingest & Query (no UI)

Upload

# use provided sample
# data\sample.log
# 2025-08-15 12:30:01 ERROR Database connection failed
# 2025-08-15 12:31:05 INFO  User admin logged in
# 2025-08-15 12:32:10 WARN  High memory usage detected

curl.exe --noproxy "*" -X POST "http://127.0.0.1:8000/upload" -F "file=@data\sample.log;type=text/plain"


Search only (no LLM)

curl.exe --noproxy "*" "http://127.0.0.1:8000/search?q=error"


AI summary (LLM)

# ensure Ollama is running and model is pulled
curl.exe --noproxy "*" "http://127.0.0.1:8000/query?q=What%20errors%20occurred%3F"


Structured report (no LLM)

curl.exe --noproxy "*" http://127.0.0.1:8000/report

(Optional) Streamlit UI
uv run streamlit run frontend/app.py
# then open http://localhost:8501

Config

Environment variables (optional):

OLLAMA_URL (default http://localhost:11434)

OLLAMA_MODEL (default llama3.2:3b)

You can set them permanently on Windows:

setx OLLAMA_MODEL "llama3.2:3b"

Endpoints

GET /health – service status

POST /upload (multipart file) – ingest + index logs

GET /search?q=...&k=5 – semantic search (fast)

GET /query?q=... – AI summary (uses Ollama)

GET /report?top_n=5 – top messages & level counts (no LLM)

Troubleshooting

python-multipart missing → uv add python-multipart

Encoding garbage (• shows as â€¢) → we enforce ASCII bullets; or set console to UTF-8:

chcp 65001; [Console]::OutputEncoding = [System.Text.Encoding]::UTF8


Ollama connection refused → ollama serve then ollama pull llama3.2:3b

Duplicates in matches → we hash IDs & skip repeats; if you already indexed dupes, delete .chromadb and re-upload

First call slow → embedding model warms on first request (subsequent requests are fast)

Roadmap (nice-to-haves)

Parsers for Apache/Nginx/syslog/K8s

Time-window queries & charts

Multi-file uploads & S3 ingestion

Role-based auth & API keys

Export incident report as Markdown/CSV