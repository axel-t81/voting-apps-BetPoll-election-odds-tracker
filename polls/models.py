from django.db import models


class Bookmaker(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Party(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "parties"

    def __str__(self):
        return f"{self.code} - {self.name}"


class OddsReading(models.Model):
    date = models.DateField()
    bookmaker = models.ForeignKey(Bookmaker, on_delete=models.PROTECT)
    party = models.ForeignKey(Party, on_delete=models.PROTECT)
    odds = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['date', 'bookmaker', 'party'],
                name='unique_daily_reading'
            ),
        ]
        indexes = [
            models.Index(fields=['date'], name='idx_odds_date'),
            models.Index(fields=['date', 'party'], name='idx_odds_date_party'),
        ]
        ordering = ['-date', 'party', 'bookmaker']

    def __str__(self):
        return f"{self.date} | {self.bookmaker} | {self.party}: {self.odds}"

    @property
    def implied_probability(self):
        """Calculate implied probability from decimal odds."""
        return 1.0 / float(self.odds) if self.odds else None
