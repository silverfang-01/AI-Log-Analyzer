# backend/ai_pipeline.py (subprocess version)
import subprocess

def query_llm(prompt: str) -> str:
    cmd = ["ollama", "run", "llama3.2:3b", prompt]  # use a small model for speed
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",   # <-- force utf-8
        errors="replace"    # <-- avoid hard crashes on odd bytes
    )
    return result.stdout.strip()
