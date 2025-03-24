from django.urls import path
from .views import signup, login_view, logout_view, dashboard , create_bot

urlpatterns = [
    path('signup/', signup, name="signup"),
    path('login/', login_view, name="login"),  # ✅ Added login
    path('logout/', logout_view, name="logout"),  # ✅ Added logout
    path('dashboard/', dashboard, name="dashboard"),
    path("create-bot/", create_bot, name="create_bot"),
]
