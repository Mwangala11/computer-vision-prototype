import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get your Gemini API key
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Test if it loaded correctly
if gemini_api_key:
    print("Gemini API key loaded successfully!")
else:
    print("Failed to load Gemini API key. Check your .env file.")


