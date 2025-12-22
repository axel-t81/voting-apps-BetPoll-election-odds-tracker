"""
Base scraper class providing Playwright browser lifecycle management.
All bookmaker scrapers inherit from this class.
"""

import logging
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import TypedDict

from playwright.async_api import async_playwright, Browser, Page

logger = logging.getLogger(__name__)


class OddsResult(TypedDict):
    """Structure for scraped odds data."""
    party: str  # Party code: ALP, LNP, or OTH
    odds: Decimal


class BaseScraper(ABC):
    """
    Abstract base class for bookmaker scrapers.
    
    Handles Playwright browser lifecycle and provides common configuration.
    Subclasses must implement the `scrape()` method.
    """
    
    # Override in subclasses
    name: str = "base"
    url: str = ""
    
    # Browser configuration
    HEADLESS = True
    TIMEOUT = 30000  # 30 seconds
    USER_AGENT = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    
    def __init__(self):
        self._playwright = None
        self._browser: Browser | None = None
    
    async def __aenter__(self):
        """Set up Playwright browser on context entry."""
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            headless=self.HEADLESS
        )
        logger.info(f"[{self.name}] Browser launched")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up browser resources on context exit."""
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()
        logger.info(f"[{self.name}] Browser closed")
        return False  # Don't suppress exceptions
    
    async def get_page(self) -> Page:
        """Create a new page with configured settings."""
        if not self._browser:
            raise RuntimeError("Browser not initialized. Use 'async with' context.")
        
        context = await self._browser.new_context(
            user_agent=self.USER_AGENT,
            viewport={"width": 1920, "height": 1080},
        )
        page = await context.new_page()
        page.set_default_timeout(self.TIMEOUT)
        return page
    
    @abstractmethod
    async def scrape(self) -> list[OddsResult]:
        """
        Scrape odds from the bookmaker's website.
        
        Returns:
            List of OddsResult dicts with party codes and decimal odds.
            Party codes should be: ALP, LNP, or OTH
        
        Raises:
            Exception: If scraping fails for any reason.
        """
        pass
    
    def map_party_name(self, bookmaker_name: str) -> str:
        """
        Map bookmaker-specific party names to standard codes.
        
        Override in subclass if bookmaker uses different naming.
        
        Args:
            bookmaker_name: The party name as displayed on the bookmaker site.
        
        Returns:
            Standard party code: ALP, LNP, or OTH
        """
        name_lower = bookmaker_name.lower().strip()
        
        # Labor variations
        if any(term in name_lower for term in ["labor", "alp", "albanese"]):
            return "ALP"
        
        # Coalition variations
        if any(term in name_lower for term in [
            "coalition", "liberal", "lnp", "l/np", 
            "ley", "national"
        ]):
            return "LNP"
        
        # Everything else (Greens, independents, etc.)
        return "OTH"

