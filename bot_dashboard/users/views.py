from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from bots.models import Bot, GroupSettings
from bots.models import Bot, Group, GroupSettings , FlaggedMessage
from django.contrib import messages
from django.core.paginator import Paginator

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user
            messages.success(request, "Signup successful! Redirecting to Dashboard.")
            return redirect('dashboard')
        else:
            messages.error(request, "Signup failed. Please check the form.")
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful! Redirecting to Dashboard.")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    bots = Bot.objects.all()
    groups = Group.objects.all()

    # Count flagged messages for each group dynamically
    total_bots = bots.count()
    total_active_users = sum(group.active_users for group in groups)

    # Sum the message_count from GroupSettings, if available
    total_messages = 0
    for group in groups:
        group_settings = getattr(group, 'groupsettings', None)
        if group_settings:
            total_messages += group_settings.message_count

    flagged_messages = FlaggedMessage.objects.all()

    # Pagination for flagged messages
    paginator = Paginator(flagged_messages, 10)  # Show 10 flagged messages per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard.html', {
        'total_bots': total_bots,
        'total_active_users': total_active_users,
        'total_messages': total_messages,
        'groups': groups,
        'flagged_messages': page_obj.object_list,
        'page': page_obj.number,
        'total_pages': page_obj.paginator.num_pages
    })








def group_settings(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    settings, created = GroupSettings.objects.get_or_create(group=group)

    if request.method == "POST":
        settings.allow_links = "allow_links" in request.POST
        settings.block_spam = "block_spam" in request.POST
        settings.allow_promotions = "allow_promotions" in request.POST
        settings.detect_deepfake = "detect_deepfake" in request.POST
        settings.detect_image_scam = "detect_image_scam" in request.POST
        settings.save()
    
    return render(request, "group_settings.html", {"group": group, "settings": settings})

def create_bot(request):
    if request.method == "POST":
        bot_token = request.POST.get("bot_token")
        if bot_token:
            if Bot.objects.filter(bot_token=bot_token).exists():
                messages.error(request, "Bot token already exists.")
            else:
                Bot.objects.create(owner=request.user, bot_token=bot_token)
                messages.success(request, "Bot created successfully!")
        return redirect("dashboard")
    return render(request, "create_bot.html")


def main_page(request):
    return render(request, "main.html")
