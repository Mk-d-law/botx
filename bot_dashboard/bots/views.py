from django.shortcuts import render, redirect , redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Bot, Group, FlaggedMessage
from .utils import fetch_groups, update_group_data
from .models import GroupSettings
from .forms import GroupSettingsForm

@login_required
def bot_list(request):
    """Show all bots owned by the user."""
    bots = Bot.objects.filter(owner=request.user)
    return render(request, "bot_list.html", {"bots": bots})

@login_required
def bot_details(request, bot_id):
    """Show details of a bot, including groups and flagged messages."""
    bot = Bot.objects.get(id=bot_id, owner=request.user)
    update_group_data(bot.bot_token)  # Fetch latest groups

    groups = Group.objects.filter(bot=bot)
    flagged_messages = FlaggedMessage.objects.filter(group__in=groups).order_by("-timestamp")

    return render(request, "bot_details.html", {"bot": bot, "groups": groups, "flagged_messages": flagged_messages})


def bot_settings(request, bot_id, group_id):
    bot = get_object_or_404(Bot, id=bot_id)
    group_settings, created = GroupSettings.objects.get_or_create(bot=bot, group_id=group_id)

    if request.method == "POST":
        form = GroupSettingsForm(request.POST, instance=group_settings)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = GroupSettingsForm(instance=group_settings)

    return render(request, 'bot_settings.html', {'form': form, 'bot': bot, 'group_id': group_id})
