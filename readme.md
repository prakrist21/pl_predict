# PL Predictor

A Django web application for predicting Premier League match scores. Users can register, predict scores for upcoming matches across gameweeks, and compete with friends in private leagues.

## Features

- **User Authentication** — Registration, login, and logout
- **Match Predictions** — Predict home/away scores for Premier League matches each gameweek (GW 1–38)
- **Private Leagues** — Create leagues with auto-generated invite codes, join via invite code, and track standings

## Setup

```bash
# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\Activate  # Windows
source .venv/bin/activate  # Linux/macOS

# Install dependencies
pip install Django dj-database-url python-dotenv psycopg2-binary

# Configure environment
# Edit .env with your DATABASE_URL and SECRET_KEY (see .env.example)

# Run migrations
python manage.py migrate

# Start the dev server
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** to use the app.

## Environment Variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Set to `True` for development |

## URLs

| Path | Description |
|---|---|
| `/` | Homepage |
| `/admin/` | Admin interface |
| `/accounts/register/` | Register |
| `/accounts/login/` | Login |
| `/accounts/logout/` | Logout |
| `/leagues/create/` | Create a league |
| `/leagues/join/` | Join a league |
| `/leagues/my/` | My leagues |

## Test Accounts

| Username | Password |
|---|---|
| `testuser` | `testpass123!` |
| `pm` | `pm101010` |
