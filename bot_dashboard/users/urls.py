from django.urls import path
from .views import signup, login_view, logout_view, dashboard, main_page , group_settings , create_bot


urlpatterns = [
    path('signup/', signup, name="signup"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('dashboard/', dashboard, name="dashboard"),
    path("dashboard/create-bot", create_bot, name="create_bot"),
    path("", main_page, name="main_page"),
    path("group/<int:group_id>/settings/", group_settings, name="group_settings"),
    
]

