# backend/main.py
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil

from .preprocess import parse_logs
from .vectorstore import add_logs_to_vectorstore, search_logs
from .anomaly import detect_anomalies
from .ai_pipeline import query_llm

app = FastAPI(title="AI Log Analyzer API")

# Allow local frontends (Streamlit/React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Resolve ../data relative to this file
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

@app.post("/upload")
async def upload_log(file: UploadFile):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file name provided.")

    file_path = DATA_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    log_df = parse_logs(str(file_path))
    if log_df.empty:
        raise HTTPException(status_code=400, detail="No logs parsed. Check file format/regex.")

    add_logs_to_vectorstore(log_df)
    anomalies = detect_anomalies(log_df)

    return {
        "status": "ok",
        "rows_ingested": int(len(log_df)),
        "anomalies_detected": int((anomalies == -1).sum()) if len(anomalies) else 0,
    }

@app.get("/query")
def query_logs(q: str, k: int = 5):
    results = search_logs(q, k) or {}
    docs_list = results.get("documents") or []
    top_docs = docs_list[0] if docs_list else []
    context = "\n".join(top_docs) if top_docs else "No relevant logs found."

    prompt = (
        "You are a log analysis assistant. Use ONLY ASCII characters (use '-' for bullets).\n"
        f"Question: {q}\n"
        f"Relevant logs:\n{context}\n\n"
        "Answer concisely. Add likely causes and fixes as short '-' bullets."
    )

    answer = query_llm(prompt)   # or query_llm(prompt, max_tokens=180, timeout_s=30) if you added timeouts
    return {"response": answer, "matches": top_docs}


@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/search")
def search_only(q: str, k: int = 5):
    results = search_logs(q, k)
    docs = results.get("documents") or []
    return {"matches": docs[0] if docs else []}
