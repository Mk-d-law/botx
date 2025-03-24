from django.contrib import admin
from django.urls import path, include
from users.views import main_page  # Import main_page view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("bots/", include("bots.urls")),
    path("", main_page, name="main_page"),  # Add this line
]
