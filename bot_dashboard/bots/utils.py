from telegram import Bot
from django.conf import settings
from .models import Group, GroupSettings, FlaggedMessage
import google.generativeai as genai

# Configure Gemini AI
genai.configure(api_key=settings.GEMINI_API_KEY)

def get_bot_instance(bot_token):
    return Bot(token=bot_token)

def fetch_groups(bot_token):
    """Fetch groups the bot is in."""
    bot = get_bot_instance(bot_token)
    updates = bot.get_updates()
    
    groups = {}
    for update in updates:
        if update.message and update.message.chat.type in ["group", "supergroup"]:
            chat_id = update.message.chat.id
            chat_name = update.message.chat.title

            if chat_id not in groups:
                groups[chat_id] = {"name": chat_name, "users": set(), "messages": []}
            
            groups[chat_id]["users"].add(update.message.from_user.id)
            groups[chat_id]["messages"].append(update.message.text)

    return groups

def get_group_settings(chat_id):
    try:
        # Assuming you're querying a model or fetching from the database
        settings = GroupSettings.objects.get(group_id=chat_id)
        return {
            "detect_deepfakes": settings.detect_deepfake,
            "allow_links": settings.allow_links,
            "block_spam": settings.block_spam,
            "allow_promotions": settings.allow_promotions,
            "faq_pdf": settings.faq_pdf,
        }
    except GroupSettings.DoesNotExist:
        # Return default settings if none are found
        return {
            "detect_deepfakes": False,
            "allow_links": True,
            "block_spam": True,
            "allow_promotions": False,
            "faq_pdf": None,
        }


def update_group_data(bot_token):
    """Update database with group details."""
    groups = fetch_groups(bot_token)
    
    for chat_id, data in groups.items():
        group, created = Group.objects.get_or_create(
            group_id=chat_id,
            defaults={"group_name": data["name"], "bot_id": bot_token}
        )
        group.total_users = len(data["users"])
        group.active_users = min(len(data["messages"]), len(data["users"]))  # Approximate active users
        group.save()

def analyze_message(text):
    """Use Gemini AI to check for spam, vulgarity, and summarize messages."""
    prompt = f"""
    Analyze the chat message:
    - Is it spam? (Yes/No)
    - Does it contain scams or vulgar words? (Yes/No)
    - Extract key topics
    - Summarize if needed

    Message: "{text}"
    """
    response = genai.generate_text(prompt)
    output = response.text.split("\n")

    is_spam = "Yes" in output[0]
    is_vulgar = "Yes" in output[1]
    topics = output[2].replace("Topics: ", "").split(", ")
    summary = output[3].replace("Summary: ", "") if len(output) > 3 else text

    return is_spam, is_vulgar, topics, summary

def moderate_message(bot_token, chat_id, message):
    """Check message against settings and delete if necessary."""
    settings = GroupSettings.objects.filter(group__group_id=chat_id).first()
    if not settings:
        return False, "No settings found."

    is_spam, is_vulgar, topics, summary = analyze_message(message.text)

    bot = get_bot_instance(bot_token)

    if settings.block_spam and is_spam:
        bot.delete_message(chat_id=chat_id, message_id=message.message_id)
        FlaggedMessage.objects.create(
            group=Group.objects.get(group_id=chat_id),
            user_id=message.from_user.id,
            username=message.from_user.username,
            message=message.text,
            reason="Spam detected"
        )
        return True, "Spam removed."
    
    if settings.allow_links is False and "http" in message.text:
        bot.delete_message(chat_id=chat_id, message_id=message.message_id)
        return True, "Link removed."

    if is_vulgar:
        bot.delete_message(chat_id=chat_id, message_id=message.message_id)
        FlaggedMessage.objects.create(
            group=Group.objects.get(group_id=chat_id),
            user_id=message.from_user.id,
            username=message.from_user.username,
            message=message.text,
            reason="Vulgar language detected"
        )
        return True, "Vulgar content removed."

    return False, summary
