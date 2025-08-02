from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Bookmaker(models.Model):
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Party(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, help_text="Hex color code (e.g., #FF0000)")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "parties"

    def __str__(self):
        return self.name

class ElectionOdds(models.Model):
    date = models.DateField()
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    bookmaker = models.ForeignKey(Bookmaker, on_delete=models.CASCADE)
    odds = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1.01)]
    )
    probability = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Calculated probability (1/odds, normalized)",
        default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "election odds"
        unique_together = ['date', 'party', 'bookmaker']
        ordering = ['-date', 'party']

    def __str__(self):
        return f"{self.party} - {self.bookmaker} - {self.date}"

    def save(self, *args, **kwargs):
        # Calculate raw probability
        raw_prob = Decimal(1) / Decimal(str(self.odds))
        
        # Get all odds for the same date and bookmaker
        same_day_odds = ElectionOdds.objects.filter(
            date=self.date,
            bookmaker=self.bookmaker
        ).exclude(id=self.id)
        
        # Calculate total probability
        total_prob = raw_prob
        for odd in same_day_odds:
            total_prob += Decimal(1) / Decimal(str(odd.odds))
        
        # Normalize probability
        self.probability = raw_prob / total_prob if total_prob else Decimal(1)
        
        # Save the instance
        super().save(*args, **kwargs)
        
        # Update other probabilities
        for odd in same_day_odds:
            other_prob = (Decimal(1) / Decimal(str(odd.odds))) / total_prob
            ElectionOdds.objects.filter(id=odd.id).update(probability=other_prob)