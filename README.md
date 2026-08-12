# Lunch Time Flask App

A small Flask + SQLite app where people enter their name and select a lunch time.

## Features

- No authentication
- Name-based lunch selection
- SQLite database
- One selection per person per day
- Users can change their selection
- Users can clear their selection
- Today's lunch schedule is visible to everyone
- Responsive UI

## Requirements

Python 3.10+ recommended.

## Setup

### 1. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
python app.py
```

Then open:

http://127.0.0.1:5000

The SQLite database (`lunch.db`) is created automatically on first run.

## Changing lunch times

Edit the time list in `app.py` and `templates/index.html` if you want different slots.

## Production note

For deployment, change `SECRET_KEY`, turn off Flask debug mode, and run behind a production WSGI server such as Gunicorn or Waitress.
