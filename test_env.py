import os
import streamlit as st
from dotenv import load_dotenv

# -----------------------------
# Load .env for local testing only
# -----------------------------
if os.path.exists(".env"):
    load_dotenv()

# -----------------------------
# Read Gemini API Key from environment
# Works for both local and Streamlit Cloud
# -----------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# -----------------------------
# Check if the key exists
# -----------------------------
if not GEMINI_API_KEY:
    st.error(
        "Gemini API key not configured!\n"
        "Local: create a .env file with:\n"
        "GEMINI_API_KEY=your_api_key_here\n\n"
        "Cloud: add GEMINI_API_KEY in Streamlit Secrets"
    )
    st.stop()  # Stop execution until the key is available
else:
    st.success("Gemini API key loaded successfully!")

# -----------------------------
# Your app logic starts here
# -----------------------------

st.title("Computer Vision Prototype App")

st.write("Your app is now running with the Gemini API key configured properly!")

# Example: Use GEMINI_API_KEY in your API requests
# e.g., response = some_api_function(api_key=GEMINI_API_KEY)


