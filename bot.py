import asyncio
import re
import nest_asyncio
import google.generativeai as genai
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# Apply nest_asyncio to fix event loop issue
nest_asyncio.apply()

# Set your API keys
GEMINI_API_KEY = "xxxxx"  # Replace with your Gemini API key
TOKEN = "yyyyy"  # Replace with your Telegram bot token

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
        return False  # Default to not spam if AI fails

async def handle_messages(update: Update, context: CallbackContext):
    message = update.message
    chat_id = message.chat_id
    user = message.from_user

    if await is_spam_gemini(message.text):  # Use AI to check spam
        try:
            await message.delete()
        except Exception as e:
            print(f"Error deleting message: {e}")

        admins = await context.bot.get_chat_administrators(chat_id)
        admin_mentions = [f"@{admin.user.username}" for admin in admins if admin.user.username]

        warning_text = f"🚨 *Spam detected!* 🚨\nMessage from {user.mention_markdown()} was removed.\n"
        warning_text += "Next time, it will lead to a warning or ban.\n"
        if admin_mentions:
            warning_text += "Admins notified: " + ", ".join(admin_mentions)

        await context.bot.send_message(chat_id=chat_id, text=warning_text, parse_mode=ParseMode.MARKDOWN)

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))

    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
