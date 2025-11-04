import os
import streamlit as st
from dotenv import load_dotenv

# Load .env locally only (ignored on Streamlit Cloud)
if os.path.exists(".env"):
    load_dotenv()

# Read GEMINI_API_KEY from environment variables (local or cloud)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Check if key exists
if not GEMINI_API_KEY:
    st.error(
        "Gemini API key not configured!\n"
        "Local: create a .env file with GEMINI_API_KEY=your_api_key_here\n"
        "Cloud: add GEMINI_API_KEY in Streamlit Secrets"
    )
else:
    st.success("Gemini API key loaded successfully!")

