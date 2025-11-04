import os
from dotenv import load_dotenv
import streamlit as st

# Load .env file only if it exists (for local development)
if os.path.exists(".env"):
    load_dotenv()

# Get the Gemini API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Check if the key is available
if not GEMINI_API_KEY:
    st.error("Gemini API key not configured! Please set it in .env (local) or Streamlit Secrets (cloud).")
else:
    st.success("Gemini API key loaded successfully!")
