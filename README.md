# 🧠 Telegram Bot Dashboard with Spam Filtering & Link Control (Django + Gemini AI)

This project is a **Telegram bot management dashboard** built with **Django** and powered by **Google Gemini AI**. It allows users to manage group bot settings, auto-moderate spam using AI, and control link sharing behavior.

## 🚀 Features

* 🔐 User Authentication (Signup/Login)
* 🧠 AI-powered spam detection using Gemini API
* ⚙️ Group-specific bot settings (e.g., allow links, block spam)
* 💽 Django Admin & Custom UI Dashboard
* 📩 Telegram bot integration with polling
* 🛡️ Auto-deletes spam messages or links based on settings

---

## 🛠️ Tech Stack

* **Backend:** Django
* **Bot Framework:** `python-telegram-bot`
* **AI Integration:** Google Gemini via `google.generativeai`
* **Database:** SQLite (can be swapped with PostgreSQL/MySQL)
* **Frontend:** Bootstrap (basic styling)

---

## 📁 Project Structure

```
bot_dashboard/
├── bots/
│   ├── bot_handler.py         # Telegram bot runner
│   ├── models.py              # Group settings model
│   ├── utils.py               # Helper functions
│   ├── views.py               # Settings views
│   ├── urls.py                # URLs for bot settings
│   └── templates/             # HTML templates
├── users/
│   ├── models.py              # CustomUser model
│   ├── views.py               # Signup/Login
│   └── urls.py
├── bot_dashboard/
│   └── settings.py            # Django settings
├── manage.py
└── requirements.txt
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/bot-dashboard.git
cd bot-dashboard
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file or export the variables manually:

```env
GEMINI_API_KEY=your_google_gemini_api_key
BOT_TOKEN=your_telegram_bot_token
```

Alternatively, set these in `settings.py` securely or using `os.getenv()`.

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (optional)

```bash
python manage.py createsuperuser
```

### 6. Run the Django Server

```bash
python manage.py runserver
```

### 7. Run the Bot

```bash
python bots/bot_handler.py
```

Ensure you are in the root project directory where `manage.py` is located.

---

## 🔗 Useful Endpoints

* `/users/signup/` - User registration
* `/users/login/` - User login
* `/bots/settings/` - Bot settings dashboard

---

## 📊 Future Improvements

* Admin UI to manage multiple bots
* Dashboard metrics (message count, deleted count)
* Group member management and role permissions
* Scheduled reports and alerts


---

## ✅ License

This project is licensed under the MIT License.
