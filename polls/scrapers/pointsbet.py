"""
PointsBet scraper for Australian Federal Election odds.
"""

import logging
from decimal import Decimal

from .base import BaseScraper, OddsResult

logger = logging.getLogger(__name__)


class PointsBetScraper(BaseScraper):
    """
    Scraper for PointsBet Australian Federal Election betting odds.
    
    URL: https://pointsbet.com.au/sports/politics/Australian-Federal-Politics/2306240
    """
    
    name = "PointsBet"
    url = "https://pointsbet.com.au/sports/politics/Australian-Federal-Politics/2306240"
    
    # CSS Selectors for PointsBet
    CONTAINER_SELECTOR = 'button[data-label^="oddsButton"]'  # Wait for buttons
    OUTCOME_SELECTOR = 'button[data-label^="oddsButton"]'    # Each betting button
    # NAME and ODDS parsed from data-value attribute
    
    async def scrape(self) -> list[OddsResult]:
        """
        Scrape odds from PointsBet.
        
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
                    self.OUTCOME_SELECTOR,
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
                    # Parse data-value attribute: "... - Labor - 1.3"
                    data_value = await outcome.get_attribute('data-value')
                    if not data_value:
                        continue
                    
                    # Split from right to get name and odds
                    parts = data_value.rsplit(' - ', 2)
                    if len(parts) < 3:
                        logger.warning(f"[{self.name}] Unexpected data-value format: {data_value}")
                        continue
                    
                    party_name = parts[-2]  # Second to last part
                    odds_text = parts[-1]   # Last part
                    
                    odds_value = Decimal(odds_text.strip())
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
