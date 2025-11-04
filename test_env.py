import os
from dotenv import load_dotenv
import streamlit as st

# Load .env only if it exists (for local development)
if os.path.exists(".env"):
    load_dotenv()

# Always read from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Check if the key is present
if not GEMINI_API_KEY:
    st.error(
        "Gemini API key not configured!\n"
        "If running locally, create a .env file with:\n"
        "GEMINI_API_KEY=your_api_key_here\n"
        "If deployed, add the key in Streamlit Secrets."
    )
else:
    st.success("Gemini API key loaded successfully!")
