from django.core.management.base import BaseCommand
from predictions.models import Match
from dotenv import load_dotenv
import requests
import os

class Command(BaseCommand):
    help = 'Fetch results from football-data.org'

    def handle(self, *args, **kwargs):
        load_dotenv()
        API_TOKEN = os.getenv('FOOTBALL_API_TOKEN')
        headers = {'X-Auth-Token': API_TOKEN}
        BASE_URL = 'https://api.football-data.org/v4'

        for gw in range(1, 39):
            response = requests.get(
                f'{BASE_URL}/competitions/PL/matches?matchday={gw}',
                headers=headers
            )

            if response.status_code != 200:
                continue

            matches = response.json()['matches']

            for m in matches:
                if m['status'] == 'FINISHED':
                    try:
                        match = Match.objects.get(match_id=m['id'])
                        match.home_score = m['score']['fullTime']['home']
                        match.away_score = m['score']['fullTime']['away']
                        match.status = 'FINISHED'
                        match.save()
                    except Match.DoesNotExist:
                        self.stdout.write(f"Match {m['id']} not found in DB")

            self.stdout.write(f'GW {gw} results updated')

        self.stdout.write('All results fetched!')