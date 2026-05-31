"""Application configuration."""

import os
from dotenv import load_dotenv

load_dotenv()

# Also check Streamlit secrets
try:
    import streamlit as st
    OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY", ""))
except Exception:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

OPENROUTER_BASE_URL = "https://api.orcarouter.ai/v1"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
LLM_MODEL = "orcarouter/auto"
LLM_TEMPERATURE = 0.3
MAX_TOKENS = 2048
