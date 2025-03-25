from django import forms
from .models import GroupSettings

class GroupSettingsForm(forms.ModelForm):
    class Meta:
        model = GroupSettings
        fields = [
            'group_name', 
            'allow_links', 
            'block_spam', 
            'allow_promotions',
            'detect_deepfake',
            'detect_image_scam'
        ]

