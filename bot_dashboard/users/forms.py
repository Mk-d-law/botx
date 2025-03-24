from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    bot_token = forms.CharField(required=True, help_text="Enter your Telegram Bot Token")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'bot_token']
