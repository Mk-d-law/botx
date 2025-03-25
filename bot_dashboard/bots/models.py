from django.db import models
from users.models import CustomUser

class Bot(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bot_token = models.CharField(max_length=255, unique=True)
    group_count = models.IntegerField(default=0) 

    def __str__(self):
        return f"Bot of {self.owner.username}"

class Group(models.Model):
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="groups")
    group_id = models.BigIntegerField(unique=True)
    group_name = models.CharField(max_length=255)
    total_users = models.IntegerField(default=0)
    active_users = models.IntegerField(default=0)

    def __str__(self):
        return self.group_name

class GroupSettings(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=255)  # ✅ Ensure this field exists
    faq_pdf = models.FileField(upload_to='faq_pdfs/', blank=True, null=True)
    allow_links = models.BooleanField(default=True)
    block_spam = models.BooleanField(default=True)
    allow_promotions = models.BooleanField(default=False)
    detect_deepfake = models.BooleanField(default=False)
    detect_image_scam = models.BooleanField(default=False)
    message_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Settings for {self.group.group_name}"

class FlaggedMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user_id = models.BigIntegerField()
    username = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField()
    reason = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Flagged in {self.group.group_name} - {self.reason}"
    

class MessageSummary(models.Model):
    message_id = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255)
    summary = models.TextField()
    original_text = models.TextField()
    is_image = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Summary for message {self.message_id} from {self.user_id}"
