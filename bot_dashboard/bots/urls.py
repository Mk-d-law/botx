from django.urls import path
from .views import bot_list, bot_details
from .views import bot_settings

urlpatterns = [
    path("", bot_list, name="bot_list"),
    path("<int:bot_id>/", bot_details, name="bot_details"),
    path('settings/<int:bot_id>/<int:group_id>/', bot_settings, name="bot_settings"),
]
