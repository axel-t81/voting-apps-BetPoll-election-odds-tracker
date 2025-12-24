"""
Bookmaker scrapers for Australian Federal Election odds.

Each scraper uses Playwright to handle JavaScript-rendered SPAs.
"""

from .base import BaseScraper, OddsResult
from .betr import BetrScraper
from .pointsbet import PointsBetScraper
from .ladbrokes import LadbrokesScraper

# List of all available scrapers for the management command
ALL_SCRAPERS = [
    BetrScraper,
    PointsBetScraper,
    LadbrokesScraper,
]

__all__ = [
    "BaseScraper",
    "OddsResult",
    "BetrScraper",
    "PointsBetScraper",
    "LadbrokesScraper",
    "ALL_SCRAPERS",
]
