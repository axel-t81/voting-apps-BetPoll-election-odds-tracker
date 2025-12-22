"""
Odds calculation utilities for converting betting odds to probabilities.
"""

from decimal import Decimal, ROUND_HALF_UP


def decimal_to_probability(odds: Decimal) -> Decimal:
    """
    Convert decimal odds to implied probability.
    
    Formula: probability = 1 / odds
    
    Args:
        odds: Decimal odds (e.g., 1.85 means $1.85 return per $1 bet)
    
    Returns:
        Implied probability as a decimal (e.g., 0.54 for 54%)
    
    Example:
        >>> decimal_to_probability(Decimal("2.00"))
        Decimal('0.50')
    """
    if odds <= 0:
        raise ValueError("Odds must be positive")
    
    return (Decimal("1") / odds).quantize(
        Decimal("0.0001"),
        rounding=ROUND_HALF_UP
    )


def normalize_probabilities(probabilities: list[Decimal]) -> list[Decimal]:
    """
    Remove the bookmaker's overround (vig) to get fair probabilities.
    
    Bookmaker odds typically sum to >100% (the overround is their margin).
    This normalizes probabilities so they sum to exactly 100%.
    
    Args:
        probabilities: List of implied probabilities from odds.
    
    Returns:
        List of normalized (fair) probabilities that sum to 1.0.
    
    Example:
        >>> probs = [Decimal("0.54"), Decimal("0.48")]  # Sum = 1.02 (2% overround)
        >>> normalize_probabilities(probs)
        [Decimal('0.5294'), Decimal('0.4706')]  # Sum = 1.0
    """
    if not probabilities:
        return []
    
    total = sum(probabilities)
    
    if total == 0:
        raise ValueError("Total probability cannot be zero")
    
    return [
        (prob / total).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
        for prob in probabilities
    ]


def odds_to_fair_probability(odds_list: list[Decimal]) -> list[Decimal]:
    """
    Convert a list of decimal odds to fair (vig-removed) probabilities.
    
    This is a convenience function combining decimal_to_probability
    and normalize_probabilities.
    
    Args:
        odds_list: List of decimal odds for all outcomes in a market.
    
    Returns:
        List of fair probabilities (sum to 1.0).
    
    Example:
        >>> odds = [Decimal("1.85"), Decimal("2.10")]
        >>> odds_to_fair_probability(odds)
        [Decimal('0.5317'), Decimal('0.4683')]
    """
    implied_probs = [decimal_to_probability(odds) for odds in odds_list]
    return normalize_probabilities(implied_probs)


def calculate_overround(odds_list: list[Decimal]) -> Decimal:
    """
    Calculate the bookmaker's overround (margin/vig) from odds.
    
    An overround of 1.02 means a 2% margin for the bookmaker.
    
    Args:
        odds_list: List of decimal odds for all outcomes.
    
    Returns:
        Overround as a decimal (e.g., 1.02 for 2% margin).
    
    Example:
        >>> odds = [Decimal("1.85"), Decimal("2.10")]
        >>> calculate_overround(odds)
        Decimal('1.0176')  # ~1.76% margin
    """
    implied_probs = [decimal_to_probability(odds) for odds in odds_list]
    return sum(implied_probs).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)

