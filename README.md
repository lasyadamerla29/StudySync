# StudySync — Student Productivity & Habit Tracker

StudySync is a Django web app for students to manage daily habits, assignments, study sessions, and weekly productivity reports.

## Features
- Student registration, login, and logout
- Personal dashboard with task, habit, and study summaries
- Create and complete daily habits
- Add, complete, reopen, and delete tasks
- Record study sessions by subject, date, and minutes
- Seven-day study report and task/habit summaries
- Per-user data ownership
- Django admin panel
- SQLite database for easy local setup

## Tech stack
Python, Django, SQLite, HTML, CSS, Bootstrap 5.

## Run locally (Windows)
1. Install Python 3.11 or newer and Git.
2. Open this folder in VS Code.
3. In the VS Code terminal run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

4. Open http://127.0.0.1:8000/
5. Register a student account or log in.
6. Admin page: http://127.0.0.1:8000/admin/

If PowerShell blocks activation, use Command Prompt and run:
```bat
.venv\Scripts\activate.bat
```

## Run tests
```powershell
python manage.py test
```

## GitHub upload
Create an empty repository on GitHub named `studysync-django` (do not initialize it with a README if you already have this README locally). Then run:

```powershell
git init
git add .
git commit -m "Build StudySync Django tracker"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/studysync-django.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username.

## Important notes
- `db.sqlite3` is intentionally excluded from Git. Each developer creates their own local database using migrations.
- Never commit passwords, API keys, or real student data.
- This starter is for local development. Before deploying publicly, set `DEBUG = False`, use an environment-based secret key, configure allowed hosts, HTTPS, and production static files.
