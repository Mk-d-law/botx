import os
import sys
import asyncio
import nest_asyncio
import google.generativeai as genai
from asgiref.sync import sync_to_async
from telegram import Update, PhotoSize
from telegram.constants import ParseMode
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# ✅ Load Django settings properly
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bot_dashboard.settings")

import django
django.setup()

from django.conf import settings
from bots.utils import get_group_settings  # Ensure this path is correct
from bots.models import MessageSummary  # Import the model

# ✅ Apply nest_asyncio to prevent event loop conflicts
nest_asyncio.apply()

# ✅ Configure Google Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)
MODEL = "gemini-2.0-flash"

# ✅ Convert get_group_settings to async
@sync_to_async
def fetch_group_settings(chat_id):
    return get_group_settings(chat_id)

# ✅ Summarization function
async def summarize_text(text: str) -> str:
    """Summarize the provided text using Google Gemini AI."""
    try:
        model = genai.GenerativeModel(MODEL)
        response = await asyncio.to_thread(model.generate_content, f"Please summarize the following text:\n\n{text}")
        return response.text.strip()
    except Exception as e:
        print(f"Error in summarization: {e}")
        return text  # In case of failure, return the original text as fallback

# ✅ Convert storing summary to async
@sync_to_async
def store_summary(message_id, user_id, summary, original_text, is_image):
    MessageSummary.objects.create(
        message_id=message_id,
        user_id=user_id,
        summary=summary,
        original_text=original_text,
        is_image=is_image
    )

async def is_spam(text: str) -> bool:
    """Check if the text is spam using Google Gemini AI."""
    try:
        model = genai.GenerativeModel(MODEL)
        response = await asyncio.to_thread(model.generate_content, f"Is this spam? Reply 'Yes' or 'No'.\n\n{text}")
        return "yes" in response.text.strip().lower()
    except Exception as e:
        print(f"Error in AI spam detection: {e}")
        return False  # Assume not spam in case of failure

async def is_image_spam(image_url: str) -> bool:
    """Check if the image contains spam content using Google Gemini AI."""
    try:
        model = genai.GenerativeModel(MODEL)
        response = await asyncio.to_thread(
            model.generate_content,
            f"Does this image contain spam, inappropriate, or misleading content? Reply 'Yes' or 'No'.\n\n{image_url}",
        )
        return "yes" in response.text.strip().lower()
    except Exception as e:
        print(f"Error in image spam detection: {e}")
        return False

async def is_deepfake(image_url: str) -> bool:
    """Detect if an image is a deepfake using Google Gemini AI."""
    try:
        model = genai.GenerativeModel(MODEL)
        response = await asyncio.to_thread(
            model.generate_content,
            f"Analyze this image and determine if it is a deepfake. Reply 'Yes' or 'No'.\n\n{image_url}",
        )
        return "yes" in response.text.strip().lower()
    except Exception as e:
        print(f"Error in deepfake detection: {e}")
        return False

async def handle_messages(update: Update, context: CallbackContext):
    """Handles messages and applies group settings."""
    message = update.message
    chat_id = message.chat_id
    user = message.from_user  # Get the user who sent the message

    # ✅ Fetch group settings asynchronously
    group_settings = await fetch_group_settings(chat_id)

    # Ensure that group_settings is not None
    if not group_settings:
        group_settings = {
            "detect_deepfakes": False,
            "allow_links": True,
            "block_spam": True,
            "allow_promotions": False,
            "faq_pdf": None,
        }

    print(group_settings)
    
    # ✅ Handle text messages
    if message.text:
        if not group_settings["allow_links"] and "http" in message.text:
            try:
                await message.delete()
                warning_text = f"🚨 Warning! 🚨\nLinks are not allowed, {user.mention_markdown()}!\nNext time, you may be removed."
                await context.bot.send_message(chat_id=chat_id, text=warning_text, parse_mode=ParseMode.MARKDOWN)
            except Exception as e:
                print(f"Error deleting message: {e}")
            return

        if group_settings["block_spam"] and await is_spam(message.text):
            try:
                await message.delete()
                admins = await context.bot.get_chat_administrators(chat_id)
                admin_mentions = [f"@{admin.user.username}" for admin in admins if admin.user.username]

                warning_text = f"🚨 Spam detected! 🚨\nMessage from {user.mention_markdown()} was removed.\n"
                warning_text += "Next time, we will remove you from the group!\n"
                if admin_mentions:
                    warning_text += "Admins notified: " + ", ".join(admin_mentions)

                await context.bot.send_message(chat_id=chat_id, text=warning_text, parse_mode=ParseMode.MARKDOWN)
            except Exception as e:
                print(f"Error deleting spam message: {e}")

        # Summarize text and store in DB
        summary = await summarize_text(message.text)
        await store_summary(message.message_id, str(user.id), summary, message.text, is_image=False)

    # ✅ Handle image messages
    if message.photo:
        largest_photo: PhotoSize = message.photo[-1]
        file = await context.bot.get_file(largest_photo.file_id)
        image_url = file.file_path

        if group_settings["block_spam"] and await is_image_spam(image_url):
            try:
                await message.delete()
                warning_text = f"🚨 Spam Image Detected! 🚨\n{user.mention_markdown()}, your image was removed.\n"
                await context.bot.send_message(chat_id=chat_id, text=warning_text, parse_mode=ParseMode.MARKDOWN)
            except Exception as e:
                print(f"Error deleting spam image: {e}")

        elif group_settings["detect_deepfakes"] and await is_deepfake(image_url):
            try:
                await message.delete()
                warning_text = f"🚨 Deepfake Detected! 🚨\n{user.mention_markdown()}, your image was removed.\n"
                await context.bot.send_message(chat_id=chat_id, text=warning_text, parse_mode=ParseMode.MARKDOWN)
            except Exception as e:
                print(f"Error deleting deepfake image: {e}")

        # Summarize image URL if required (optional, if you want to summarize images as well)
        summary = await summarize_text(image_url)  # Example: summarizing URL, but you might want to check the content
        await store_summary(message.message_id, str(user.id), summary, image_url, is_image=True)

async def main():
    """Starts the Telegram bot."""
    app = Application.builder().token(settings.BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))
    app.add_handler(MessageHandler(filters.PHOTO, handle_messages))  # Handle images

    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped.")
