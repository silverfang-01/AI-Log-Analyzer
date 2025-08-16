import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.title("📝 AI Log Analyzer (Free, Local)")

st.subheader("Health")
if st.button("Ping backend"):
    try:
        r = requests.get(f"{BACKEND_URL}/health", timeout=10)
        st.json(r.json())
    except Exception as e:
        st.error(f"Health check failed: {e}")

st.subheader("Upload Logs")
uploaded = st.file_uploader("Choose a .log or .txt file", type=["log","txt"])
if uploaded:
    try:
        files = {"file": (uploaded.name, uploaded.getvalue(), "text/plain")}
        r = requests.post(f"{BACKEND_URL}/upload", files=files, timeout=120)
        st.json(r.json())
    except Exception as e:
        st.error(f"Upload failed: {e}")

st.subheader("Query Logs (LLM)")
q = st.text_input("Ask something about your logs (e.g., What errors occurred?)")
if st.button("Analyze"):
    try:
        r = requests.get(f"{BACKEND_URL}/query", params={"q": q}, timeout=120)
        st.json(r.json())
    except Exception as e:
        st.error(f"Query failed: {e}")

st.subheader("Search Only (no LLM)")
qs = st.text_input("Keyword/semantic search", key="search")
if st.button("Search"):
    try:
        r = requests.get(f"{BACKEND_URL}/search", params={"q": qs, "k": 5}, timeout=60)
        st.json(r.json())
    except Exception as e:
        st.error(f"Search failed: {e}")