"""
Management command to scrape betting odds from all configured bookmakers.

Usage:
    python manage.py scrape_odds
    python manage.py scrape_odds --bookmaker sportsbet
    python manage.py scrape_odds --dry-run
"""

import asyncio
import logging
from datetime import date

from django.core.management.base import BaseCommand, CommandError

from polls.models import Bookmaker, Party, OddsReading
from polls.scrapers import ALL_SCRAPERS, BaseScraper
from polls.services.notifications import send_scrape_failure_alert

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Scrape betting odds from bookmakers and save to database"
    
    def add_arguments(self, parser):
        parser.add_argument(
            "--bookmaker",
            type=str,
            help="Scrape only a specific bookmaker (e.g., sportsbet, tab, ladbrokes)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Run scrapers but don't save to database",
        )
        parser.add_argument(
            "--no-notify",
            action="store_true",
            help="Don't send email notifications on failure",
        )
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting odds scrape..."))
        
        # Filter scrapers if specific bookmaker requested
        scrapers = self._get_scrapers(options.get("bookmaker"))
        
        if not scrapers:
            raise CommandError("No scrapers available")
        
        # Run the async scraping
        results = asyncio.run(self._run_scrapers(scrapers))
        
        # Process results
        successes = results["success"]
        failures = results["failed"]
        
        # Save successful results (unless dry-run)
        if not options.get("dry_run"):
            for result in successes:
                self._save_odds(result["name"], result["data"])
        else:
            self.stdout.write(self.style.WARNING("Dry run - not saving to database"))
        
        # Report summary
        self._report_summary(successes, failures)
        
        # Send failure notification if needed
        if failures and not options.get("no_notify"):
            send_scrape_failure_alert(failures)
            self.stdout.write(self.style.WARNING("Failure notification sent"))
        
        if failures:
            raise CommandError(f"{len(failures)} scraper(s) failed")
    
    def _get_scrapers(self, bookmaker_filter: str | None) -> list[type[BaseScraper]]:
        """Get list of scraper classes to run."""
        if not bookmaker_filter:
            return ALL_SCRAPERS
        
        filter_lower = bookmaker_filter.lower()
        filtered = [
            s for s in ALL_SCRAPERS
            if filter_lower in s.name.lower()
        ]
        
        if not filtered:
            available = ", ".join(s.name for s in ALL_SCRAPERS)
            raise CommandError(
                f"Unknown bookmaker: {bookmaker_filter}. Available: {available}"
            )
        
        return filtered
    
    async def _run_scrapers(self, scraper_classes: list[type[BaseScraper]]) -> dict:
        """Run all scrapers and collect results."""
        results = {
            "success": [],
            "failed": [],
        }
        
        for scraper_class in scraper_classes:
            scraper = scraper_class()
            self.stdout.write(f"  Scraping {scraper.name}...")
            
            try:
                async with scraper:
                    data = await scraper.scrape()
                
                results["success"].append({
                    "name": scraper.name,
                    "data": data,
                })
                self.stdout.write(
                    self.style.SUCCESS(f"    {scraper.name}: {len(data)} results")
                )
                
            except Exception as e:
                error_msg = str(e)
                results["failed"].append({
                    "name": scraper.name,
                    "error": error_msg,
                })
                self.stdout.write(
                    self.style.ERROR(f"    {scraper.name}: FAILED - {error_msg}")
                )
                logger.exception(f"Scraper {scraper.name} failed")
        
        return results
    
    def _save_odds(self, bookmaker_name: str, odds_data: list[dict]) -> None:
        """Save scraped odds to database."""
        today = date.today()
        
        # Get or create bookmaker
        bookmaker, _ = Bookmaker.objects.get_or_create(name=bookmaker_name)
        
        saved_count = 0
        for item in odds_data:
            party_code = item["party"]
            odds_value = item["odds"]
            
            # Get party (must already exist in DB)
            try:
                party = Party.objects.get(code=party_code)
            except Party.DoesNotExist:
                logger.warning(f"Party not found: {party_code} - skipping")
                continue
            
            # Update or create the odds reading for today
            _, created = OddsReading.objects.update_or_create(
                date=today,
                bookmaker=bookmaker,
                party=party,
                defaults={"odds": odds_value},
            )
            
            action = "Created" if created else "Updated"
            logger.debug(f"{action} {bookmaker_name}/{party_code}: {odds_value}")
            saved_count += 1
        
        self.stdout.write(f"    Saved {saved_count} records for {bookmaker_name}")
    
    def _report_summary(self, successes: list, failures: list) -> None:
        """Print summary of scrape results."""
        self.stdout.write("")
        self.stdout.write(self.style.NOTICE("=" * 50))
        self.stdout.write(self.style.NOTICE("SCRAPE SUMMARY"))
        self.stdout.write(self.style.NOTICE("=" * 50))
        
        total = len(successes) + len(failures)
        
        if successes:
            self.stdout.write(
                self.style.SUCCESS(f"  Successful: {len(successes)}/{total}")
            )
            for s in successes:
                self.stdout.write(f"    - {s['name']}: {len(s['data'])} results")
        
        if failures:
            self.stdout.write(
                self.style.ERROR(f"  Failed: {len(failures)}/{total}")
            )
            for f in failures:
                self.stdout.write(f"    - {f['name']}: {f['error']}")
        
        self.stdout.write(self.style.NOTICE("=" * 50))

