"""
core/models.py
LLM model instances shared across all tools.
"""
from langchain_groq import ChatGroq

import os
from pathlib import Path

# Auto-load .env if available (helpful in local dev and streamlit run environments).
def _load_dotenv(path: Path):
    if not path.is_file():
        return
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key, value = key.strip(), value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value

project_root = Path(__file__).resolve().parent.parent
_load_dotenv(project_root / ".env")

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise EnvironmentError("GROQ_API_KEY is not set. Set it in your environment or .env file.")

summarizer_model = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.2, api_key=api_key)
extractor_model  = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.1, api_key=api_key)
review_model     = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.3, api_key=api_key)
suggest_model    = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.4, api_key=api_key)
planner_model    = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.0, api_key=api_key)