# PL Predictor

A Django web application for predicting English Premier League match scores, integrated with the [football-data.org](https://www.football-data.org/) API. Users can register, predict scores for upcoming matches across gameweeks (GW 1–38), and compete with friends in private leagues.

## Features

### User Authentication
- Custom user model with email verification flow
- Registration (username, email, password) — sends verification email via Gmail SMTP
- Login / logout via Django's built-in auth views
- Inactive accounts cannot log in until email is verified

### Gameweek Browsing
- List view of all 38 Premier League gameweeks
- Detail view showing match fixtures (teams, kickoff times) per gameweek
- "Predict" link for each match to submit a score prediction

### Match Score Predictions
- Submit integer score predictions (home and away goals) for any match
- Update existing predictions seamlessly (no duplicates per user per match)
- Submission timestamps for audit and history

### Scoring System (automatic via signal)
| Points | Condition |
|--------|-----------|
| 3 | Exact score match |
| 2 | Correct goal difference |
| 1 | Correct winner / draw direction |
| 0 | Incorrect |

### Private Leagues
- **Create League** – Name your league and auto-generate an 8-character invite code
- **Join League** – Enter an invite code to join a private league (max 20 players)
- **My Leagues** – View all leagues you belong to with their invite codes
- **Gameweek & Season Leaderboards** – Points aggregated per user within a league
- **League Match Detail** – See all members' predictions for a given match
- Prevents duplicate membership with unique constraints

### External API Integration
- Fetches real Premier League fixture data from football-data.org API v4
- Idempotent seeding via `python manage.py seed_matches` (no duplicates)
- Fetches actual results via `python manage.py fetch_results`
- Covers all 38 gameweeks for competition ID: `PL`

### Tech Stack
| Technology | Purpose |
|---|---|
| **Python 3.14** | Runtime |
| **Django 6.0.6** | Web framework |
| **PostgreSQL (Neon)** | Database |
| **Tailwind CSS (CDN)** | Styling |
| **dj-database-url** | Database URL parsing |
| **psycopg2-binary** | PostgreSQL adapter |
| **python-dotenv** | Environment variable loading |
| **gunicorn** | WSGI server (production) |
| **whitenoise** | Static file serving |
| **football-data.org API** | Match fixture data source |
| **requests** | HTTP client |
| **Gmail SMTP** | Email verification |

## Quick Start

1. Clone the repo and create a virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   source .venv/bin/activate  # Linux/macOS
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file:
   ```
   SECRET_KEY=your-secret-key
   DATABASE_URL=your-neon-postgres-url
   DEBUG=True
   FOOTBALL_API_TOKEN=your-football-data-api-token
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   CRON_SECRET=your-cron-secret
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Seed match fixtures:
   ```
   python manage.py seed_matches
   ```

6. Start the development server:
   ```
   python manage.py runserver
   ```

## Management Commands

| Command | Description |
|---|---|
| `python manage.py seed_matches` | Fetch all 38 gameweeks from football-data.org and create Gameweek/Match records |
| `python manage.py fetch_results` | Fetch actual scores for FINISHED matches from the API |
| `python manage.py collectstatic` | Collect static files for deployment |

## Environment Variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string (Neon) |
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Set to `True` for development |
| `FOOTBALL_API_TOKEN` | football-data.org API token |
| `EMAIL_HOST_USER` | Gmail address for sending verification emails |
| `EMAIL_HOST_PASSWORD` | Gmail app password |
| `CRON_SECRET` | Secret key for the cron fetch-results endpoint |

## Routes

| Path | Description |
|---|---|
| `/` | Homepage |
| `/admin/` | Django admin |
| `/accounts/register/` | Register |
| `/accounts/verify/<uidb64>/<token>/` | Email verification |
| `/accounts/verification-sent/` | Verification sent confirmation |
| `/accounts/login/` | Login |
| `/accounts/logout/` | Logout |
| `/predictions/gameweeks/` | All gameweeks |
| `/predictions/gameweeks/<gw_number>/` | Gameweek detail |
| `/predictions/match/<match_id>/predict/` | Submit prediction |
| `/predictions/trigger-fetch/` | Cron endpoint to fetch results |
| `/leagues/create/` | Create a league |
| `/leagues/join/` | Join a league |
| `/leagues/my/` | My leagues |
| `/leagues/<id>/gw/<gw_number>/` | Gameweek leaderboard |
| `/leagues/<id>/season/` | Season leaderboard |
| `/leagues/<id>/gameweeks/` | Gameweeks list (league-scoped) |
| `/leagues/<id>/gameweeks/<gw_number>/` | Gameweek detail (league-scoped) |
| `/leagues/<id>/match/<match_id>/` | Match detail with all members' predictions |
| `/leagues/<id>/match/<match_id>/predict/` | Submit prediction in league context |

## Models

### accounts
- **User** — Extends `AbstractUser` with `is_verified` boolean field

### predictions
- **Gameweek** — Number (1–38)
- **Match** — Home/away team, kickoff time, scores, status, links to Gameweek
- **Prediction** — User's predicted home/away goals, points earned, links to User and Match

### leagues
- **League** — Name, host, invite code, max players (default 20)
- **LeagueMember** — Many-to-many through table with unique (league, user) constraint

## Deployment

The app is configured for deployment on Render:

- **Procfile:** `web: gunicorn core.wsgi:application`
- **build.sh:** Installs dependencies, runs `collectstatic --noinput`, then `migrate`
- **Static files** are served via WhiteNoise (`CompressedManifestStaticFilesStorage`)
- **Database:** Neon PostgreSQL (serverless)
