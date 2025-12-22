"""
Sportsbet scraper for Australian Federal Election odds.
"""

import logging
from decimal import Decimal

from .base import BaseScraper, OddsResult

logger = logging.getLogger(__name__)


class SportsbetScraper(BaseScraper):
    """
    Scraper for Sportsbet Australian Federal Election betting odds.
    
    URL: https://www.sportsbet.com.au/events/federal-election
    """
    
    name = "Sportsbet"
    url = "https://www.sportsbet.com.au/events/federal-election"
    
    # CSS Selectors - PLACEHOLDER: Update after inspecting the live site
    # These need to be refined during the "Test scrape locally" phase
    CONTAINER_SELECTOR = "[data-automation-id='market-coupon']"  # Placeholder
    OUTCOME_SELECTOR = "[data-automation-id='outcome']"  # Placeholder
    NAME_SELECTOR = "[data-automation-id='outcome-name']"  # Placeholder
    ODDS_SELECTOR = "[data-automation-id='outcome-price']"  # Placeholder
    
    async def scrape(self) -> list[OddsResult]:
        """
        Scrape odds from Sportsbet.
        
        Returns:
            List of OddsResult dicts with party codes and decimal odds.
        """
        results: list[OddsResult] = []
        
        async with await self.get_page() as page:
            logger.info(f"[{self.name}] Navigating to {self.url}")
            await page.goto(self.url, wait_until="networkidle")
            
            # Wait for odds to load (SPA needs time to render)
            try:
                await page.wait_for_selector(
                    self.CONTAINER_SELECTOR,
                    timeout=self.TIMEOUT
                )
            except Exception as e:
                logger.error(f"[{self.name}] Failed to find market container: {e}")
                raise
            
            # Find all outcome elements
            outcomes = await page.query_selector_all(self.OUTCOME_SELECTOR)
            logger.info(f"[{self.name}] Found {len(outcomes)} outcomes")
            
            for outcome in outcomes:
                try:
                    # Get party name
                    name_el = await outcome.query_selector(self.NAME_SELECTOR)
                    if not name_el:
                        continue
                    party_name = await name_el.inner_text()
                    
                    # Get odds value
                    odds_el = await outcome.query_selector(self.ODDS_SELECTOR)
                    if not odds_el:
                        continue
                    odds_text = await odds_el.inner_text()
                    
                    # Parse odds (e.g., "1.85" or "$1.85")
                    odds_value = Decimal(odds_text.replace("$", "").strip())
                    
                    # Map to standard party code
                    party_code = self.map_party_name(party_name)
                    
                    results.append({
                        "party": party_code,
                        "odds": odds_value,
                    })
                    logger.debug(
                        f"[{self.name}] Parsed: {party_name} -> {party_code} @ {odds_value}"
                    )
                    
                except Exception as e:
                    logger.warning(f"[{self.name}] Failed to parse outcome: {e}")
                    continue
        
        if not results:
            raise ValueError(f"[{self.name}] No odds data scraped")
        
        logger.info(f"[{self.name}] Scraped {len(results)} results")
        return results

