from .models import GroupSettings
from asgiref.sync import sync_to_async

@sync_to_async
def get_group_settings(chat_id):
    try:
        settings = GroupSettings.objects.get(group_id=chat_id)
        return {
            "allow_links": settings.allow_links,
            "block_spam": settings.block_spam,
            "allow_promotions": settings.allow_promotions,
        }
    except GroupSettings.DoesNotExist:
        return {"allow_links": True, "block_spam": True, "allow_promotions": False}
