import os
import sys
import asyncio
import nest_asyncio
import google.generativeai as genai
from asgiref.sync import sync_to_async
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# ✅ Load Django settings properly
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bot_dashboard.settings")

import django
django.setup()

from django.conf import settings
from bots.utils import get_group_settings  # Ensure this path is correct

# ✅ Apply nest_asyncio to prevent event loop conflicts
nest_asyncio.apply()

# ✅ Configure Google Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)
MODEL = "gemini-2.0-flash"

# ✅ Convert get_group_settings to async
@sync_to_async
def fetch_group_settings(chat_id):
    return get_group_settings(chat_id)

async def is_spam(text: str) -> bool:
    """Check if the text is spam using Google Gemini AI."""
    try:
        model = genai.GenerativeModel(MODEL)
        response = await asyncio.to_thread(model.generate_content, f"Is this spam? Reply 'Yes' or 'No'.\n\n{text}")
        return "yes" in response.text.strip().lower()
    except Exception as e:
        print(f"Error in AI spam detection: {e}")
        return False  # Assume not spam in case of failure

async def handle_messages(update: Update, context: CallbackContext):
    """Handles messages and applies group settings."""
    message = update.message
    chat_id = message.chat_id
    user = message.from_user  # Get the user who sent the message

    # ✅ Fetch group settings asynchronously
    group_settings = await fetch_group_settings(chat_id)
    group_settings = await group_settings

    # ✅ Check for links restriction
    if not group_settings["allow_links"] and "http" in message.text:
        try:
            await message.delete()
            warning_text = f"🚨 *Warning!* 🚨\nLinks are not allowed, {user.mention_markdown()}!\nNext time, you may be removed."
            await context.bot.send_message(chat_id=chat_id, text=warning_text, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            print(f"Error deleting message: {e}")
        return

    # ✅ Check for spam
    if group_settings["block_spam"] and await is_spam(message.text):
        try:
            await message.delete()

            # ✅ Get group admins
            admins = await context.bot.get_chat_administrators(chat_id)
            admin_mentions = [f"@{admin.user.username}" for admin in admins if admin.user.username]

            warning_text = f"🚨 *Spam detected!* 🚨\nMessage from {user.mention_markdown()} was removed.\n"
            warning_text += "Next time, we will remove you from the group!\n"
            if admin_mentions:
                warning_text += "Admins notified: " + ", ".join(admin_mentions)

            await context.bot.send_message(chat_id=chat_id, text=warning_text, parse_mode=ParseMode.MARKDOWN)

        except Exception as e:
            print(f"Error deleting spam message: {e}")

async def main():
    """Starts the Telegram bot."""
    app = Application.builder().token(settings.BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))

    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped.")
