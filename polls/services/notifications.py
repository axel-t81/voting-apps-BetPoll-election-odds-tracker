"""
Notification services for alerting on scrape failures.
"""

import logging
from typing import TypedDict

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


class ScraperFailure(TypedDict):
    """Structure for scraper failure details."""
    name: str
    error: str


def send_scrape_failure_alert(failures: list[ScraperFailure]) -> bool:
    """
    Send an email alert summarising which scrapers failed and why.
    
    Args:
        failures: List of dicts with 'name' and 'error' keys.
    
    Returns:
        True if email sent successfully, False otherwise.
    
    Example:
        >>> failures = [{"name": "Sportsbet", "error": "Timeout waiting for selector"}]
        >>> send_scrape_failure_alert(failures)
        True
    """
    if not failures:
        logger.info("No failures to report")
        return True
    
    recipient = getattr(settings, "ALERT_RECIPIENT", "")
    sender = getattr(settings, "EMAIL_HOST_USER", "")
    
    if not recipient:
        logger.warning("ALERT_RECIPIENT not configured - skipping email alert")
        return False
    
    if not sender:
        logger.warning("EMAIL_HOST_USER not configured - skipping email alert")
        return False
    
    # Build email content
    subject = f"BetPoll Scrape Alert: {len(failures)} scraper(s) failed"
    
    failure_details = "\n".join(
        f"  - {f['name']}: {f['error']}"
        for f in failures
    )
    
    body = f"""BetPoll daily scrape encountered failures.

Failed scrapers:
{failure_details}

Please investigate and update selectors if site structure changed.

---
This is an automated alert from BetPoll.
"""
    
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=sender,
            recipient_list=[recipient],
            fail_silently=False,
        )
        logger.info(f"Failure alert sent to {recipient}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send alert email: {e}")
        return False

