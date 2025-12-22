"""
Bookmaker scrapers for Australian Federal Election odds.

Each scraper uses Playwright to handle JavaScript-rendered SPAs.
"""

from .base import BaseScraper, OddsResult
from .sportsbet import SportsbetScraper
from .tab import TABScraper
from .ladbrokes import LadbrokesScraper

# List of all available scrapers for the management command
ALL_SCRAPERS = [
    SportsbetScraper,
    TABScraper,
    LadbrokesScraper,
]

__all__ = [
    "BaseScraper",
    "OddsResult",
    "SportsbetScraper",
    "TABScraper",
    "LadbrokesScraper",
    "ALL_SCRAPERS",
]

