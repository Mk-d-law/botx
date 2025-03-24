from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login after logout

spam_messages = [
    {"text": "Buy now! 50% off!", "group": "Marketing", "sender": "Spammer1", "date": "2025-03-24"},
    {"text": "Win a free iPhone!", "group": "Scam Alerts", "sender": "ScammerX", "date": "2025-03-23"},
    {"text": "Get rich quick!", "group": "Investment", "sender": "FakeInvestor", "date": "2025-03-22"},
]

def dashboard_view(request):
    context = {
        "spam_messages": spam_messages,
        "page": 1,
        "total_pages": 1,  # Set total pages dynamically later if needed
    }
    return render(request, "dashboard.html", context)

def dashboard(request):
    context = {
        "spam_messages": spam_messages,
        "page": 1,
        "total_pages": 1,  # Set total pages dynamically later if needed
    }
    return render(request, "dashboard.html", context)

def create_bot(request):
    if request.method == "POST":
        api_key = request.POST.get("api_key")
        faq_pdf = request.FILES.get("faq_pdf")

        if api_key and faq_pdf:
            fs = FileSystemStorage()
            filename = fs.save(faq_pdf.name, faq_pdf)

            # Process API Key & File (You can add database logic here)
            return HttpResponse(f"Bot Created with API Key: {api_key}, File: {filename}")

    return render(request, "create_bot.html")

def main_page(request):
    return render(request, "main.html")
