from django.core.management.base import BaseCommand
from odds.models import Party, Bookmaker
from django.db import transaction

class Command(BaseCommand):
    help = 'Import initial data for parties and bookmakers'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        # Create parties
        parties = [
            {'name': 'Labor', 'color': '#FF0000'},  # Red
            {'name': 'Coalition', 'color': '#0000FF'},  # Blue
        ]
        
        for party_data in parties:
            Party.objects.get_or_create(
                name=party_data['name'],
                defaults={'color': party_data['color']}
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created party "{party_data["name"]}"')
            )

        # Create bookmakers
        bookmakers = ['Sportsbet', 'Betr', 'Pointsbet']
        
        for name in bookmakers:
            Bookmaker.objects.get_or_create(name=name)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created bookmaker "{name}"')
            )