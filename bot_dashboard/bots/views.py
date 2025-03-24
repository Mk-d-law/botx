from django.shortcuts import render, redirect
from .models import GroupSettings
from .forms import GroupSettingsForm

def bot_settings(request):
    if request.method == "POST":
        form = GroupSettingsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = GroupSettingsForm()

    return render(request, 'bot_settings.html', {'form': form})
