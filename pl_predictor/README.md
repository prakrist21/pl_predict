# PL Predictor

A Django web application for predicting English Premier League match scores, integrated with the [football-data.org](https://www.football-data.org/) API.

## Features

### User Authentication
- Custom user model with registration (username, email, password)
- Login / logout via Django's built-in auth views

### Gameweek Browsing
- List view of all 38 Premier League gameweeks
- Detail view showing match fixtures (teams, kickoff times) per gameweek
- "Predict" link for each match to submit a score prediction

### Match Score Predictions
- Submit integer score predictions (home and away goals) for any match
- Update existing predictions seamlessly (no duplicates per user per match)
- Submission timestamps for audit and history
- Points field ready for future scoring logic

### Private Leagues
- **Create League** – Name your league and auto-generate an 8-character invite code
- **Join League** – Enter an invite code to join a private league (max 20 players)
- **My Leagues** – View all leagues you belong to with their invite codes
- Prevents duplicate membership with unique constraints

### External API Integration
- Fetches real Premier League fixture data from football-data.org API v4
- Idempotent seeding via `python manage.py seed_matches` (no duplicates)
- Covers all 38 gameweeks for competition ID: `PL`

### Tech Stack
| Technology | Purpose |
|---|---|
| **Python 3.14** | Runtime |
| **Django 6.0.6** | Web framework |
| **PostgreSQL (Neon)** | Database |
| **dj-database-url** | Database URL parsing |
| **psycopg2-binary** | PostgreSQL adapter |
| **python-dotenv** | Environment variable loading |
| **football-data.org API** | Match fixture data source |
| **requests** | HTTP client |

## Quick Start

1. Clone the repo and create a virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file with:
   ```
   SECRET_KEY=your-secret-key
   DATABASE_URL=your-neon-postgres-url
   DEBUG=True
   FOOTBALL_API_TOKEN=your-football-data-api-token
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

## Routes

| Path | Description |
|---|---|
| `/` | Homepage |
| `/admin/` | Django admin |
| `/accounts/register/` | Register |
| `/accounts/login/` | Login |
| `/accounts/logout/` | Logout |
| `/leagues/create/` | Create a league |
| `/leagues/join/` | Join a league |
| `/leagues/my/` | My leagues |
| `/predictions/gameweeks/` | All gameweeks |
| `/predictions/gameweeks/<gw_number>/` | Gameweek detail |
| `/predictions/match/<match_id>/predict/` | Submit prediction |
