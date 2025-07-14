import os
from dotenv import load_dotenv

# Load .env file (for local development)
load_dotenv()

# Try both env and Streamlit secrets
def get_openai_api_key():
    try:
        import streamlit as st
        return os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
    except Exception:
        return os.getenv("OPENAI_API_KEY")
