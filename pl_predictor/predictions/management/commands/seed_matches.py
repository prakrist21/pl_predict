from django.core.management.base import BaseCommand
from predictions.models import Gameweek, Match
import requests
import os

class Command(BaseCommand):
    help = 'Seed matches from football-data.org'

    def handle(self, *args, **kwargs):
        API_TOKEN = os.getenv('FOOTBALL_API_TOKEN')
        headers = {'X-Auth-Token': API_TOKEN}
        BASE_URL = 'https://api.football-data.org/v4'

        for gw in range(1, 39):
            gameweek, _ = Gameweek.objects.get_or_create(number=gw)
            
            response = requests.get(
                f'{BASE_URL}/competitions/PL/matches?matchday={gw}',
                headers=headers
            )

            if response.status_code != 200:
                self.stdout.write(f'GW {gw} failed: {response.status_code}')
                continue
            
            matches = response.json()['matches']
            
            for m in matches:
                Match.objects.get_or_create(
                    match_id=m['id'],
                    defaults={
                        'gameweek': gameweek,
                        'home_team': m['homeTeam']['shortName'],
                        'away_team': m['awayTeam']['shortName'],
                        'kickoff_time': m['utcDate'],
                        'status': m['status'],
                    }
                )
            
            self.stdout.write(f'GW {gw} seeded')
        
        self.stdout.write('All matches seeded!')