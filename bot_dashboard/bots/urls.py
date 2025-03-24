from django.urls import path
from .views import bot_settings

urlpatterns = [
    path('settings/', bot_settings, name="bot_settings"),
]
