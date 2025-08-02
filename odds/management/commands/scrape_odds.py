from django.core.management.base import BaseCommand
from django.utils import timezone
from odds.models import Party, Bookmaker, ElectionOdds
from django.db import transaction
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Scrape election odds from various bookmakers'

    def scrape_sportsbet(self):
        """Simulates scraping odds from Sportsbet."""
        return {"Labor": 1.50, "Coalition": 2.60}

    def scrape_betr(self):
        """Simulates scraping odds from Betr."""
        return {"Labor": 1.52, "Coalition": 2.55}

    def scrape_pointsbet(self):
        """Simulates scraping odds from Pointsbet."""
        return {"Labor": 1.48, "Coalition": 2.65}

    def add_random_variation(self, odds):
        """Add small random variation to odds."""
        return round(odds + (random.random() - 0.5) * 0.1, 2)

    @transaction.atomic
    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        
        # Get all active parties and bookmakers
        parties = Party.objects.filter(active=True)
        bookmakers = Bookmaker.objects.filter(active=True)
        
        # Scraping functions mapping
        scraping_functions = {
            'Sportsbet': self.scrape_sportsbet,
            'Betr': self.scrape_betr,
            'Pointsbet': self.scrape_pointsbet,
        }
        
        # Scrape current odds
        for bookmaker in bookmakers:
            if bookmaker.name in scraping_functions:
                odds_data = scraping_functions[bookmaker.name]()
                
                for party in parties:
                    if party.name in odds_data:
                        odds_value = odds_data[party.name]
                        
                        # Create or update odds
                        ElectionOdds.objects.update_or_create(
                            date=today,
                            party=party,
                            bookmaker=bookmaker,
                            defaults={'odds': odds_value}
                        )
                        
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Successfully updated odds for {party.name} from {bookmaker.name}: {odds_value}'
                            )
                        )
        
        # Generate some historical data if none exists
        for i in range(1, 10):  # Past 9 days
            past_date = today - timedelta(days=i)
            
            for bookmaker in bookmakers:
                if bookmaker.name in scraping_functions:
                    base_odds = scraping_functions[bookmaker.name]()
                    
                    for party in parties:
                        if party.name in base_odds:
                            # Add some random variation to historical data
                            historical_odds = self.add_random_variation(base_odds[party.name])
                            
                            # Only create if doesn't exist
                            ElectionOdds.objects.get_or_create(
                                date=past_date,
                                party=party,
                                bookmaker=bookmaker,
                                defaults={'odds': historical_odds}
                            )