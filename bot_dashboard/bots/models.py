from django.db import models
from users.models import CustomUser

class Bot(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bot_token = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"Bot of {self.owner.username}"

class GroupSettings(models.Model):
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="group_settings")
    group_id = models.BigIntegerField(unique=True)
    group_name = models.CharField(max_length=255)

    allow_links = models.BooleanField(default=True)
    block_spam = models.BooleanField(default=True)
    allow_promotions = models.BooleanField(default=False)

    def __str__(self):
        return f"Settings for {self.group_name}"
    
class BotSettings(models.Model):
    group_name = models.CharField(max_length=255)
    moderation_level = models.IntegerField(default=1)  # Example: 1 = Low, 2 = Medium, 3 = High
    auto_delete_spam = models.BooleanField(default=True)

    def __str__(self):
        return self.group_name
