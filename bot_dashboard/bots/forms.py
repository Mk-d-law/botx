from django import forms
from .models import BotSettings  # Ensure this model exists in bots/models.py

class GroupSettingsForm(forms.ModelForm):
    class Meta:
        model = BotSettings
        fields = ['group_name', 'moderation_level', 'auto_delete_spam']
