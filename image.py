import asyncio
import re
import nest_asyncio
import google.generativeai as genai
import requests
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# Apply nest_asyncio to fix event loop issue
nest_asyncio.apply()

# Set your API keys
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"  # Replace with your Gemini API key
SERPAPI_KEY = "YOUR_SERPAPI_KEY"  # Replace with your SerpAPI key
SENSITY_API_KEY = "YOUR_SENSITY_API_KEY"  # Replace with your Sensity AI key
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # Replace with your Telegram bot token

# Initialize Gemini AI (Using Free Model)
genai.configure(api_key=GEMINI_API_KEY)
MODEL = "gemini-2.0-flash"  # Correct Free Model Name

async def is_spam_gemini(text: str) -> bool:
    """Send the message to Gemini AI for spam detection."""
    try:
        model = genai.GenerativeModel(MODEL)
        response = model.generate_content(f"Is this message spam or a scam? Reply with only 'Yes' or 'No'.\n\n{text}")
        
        # Extract AI response and sanitize
        result = response.text.strip().lower()
        return re.search(r"\b(yes)\b", result) is not None  # Check if 'Yes' is present
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return False  # Default to not spam if API fails

async def reverse_image_search(image_url: str) -> bool:
    """Use SerpAPI for Google Reverse Image Search."""
    try:
        params = {
            "engine": "google_reverse_image",
            "image_url": image_url,
            "api_key": SERPAPI_KEY
        }
        response = requests.get("https://serpapi.com/search", params=params)
        result = response.json()

        # Check if the image has known sources online
        return "visual_matches" in result and len(result["visual_matches"]) > 0
    except Exception as e:
        print(f"SerpAPI Error: {e}")
        return False  # Default to not found if API fails

async def detect_deepfake(image_url: str) -> bool:
    """Use Sensity AI for Deepfake Detection