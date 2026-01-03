from django.contrib import admin
from .models import Bookmaker, Party, OddsReading, MarketConsensus


@admin.register(Bookmaker)
class BookmakerAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ["code", "name"]
    search_fields = ["code", "name"]


@admin.register(OddsReading)
class OddsReadingAdmin(admin.ModelAdmin):
    list_display = ["date", "bookmaker", "party", "odds"]
    list_filter = ["date", "bookmaker", "party"]
    search_fields = ["bookmaker__name", "party__name", "party__code"]
    date_hierarchy = "date"


@admin.register(MarketConsensus)
class MarketConsensusAdmin(admin.ModelAdmin):
    list_display = ["timestamp", "party", "fair_probability", "averaged_odds", "bookmaker_count"]
    list_filter = ["party", "timestamp"]
    search_fields = ["party__code", "party__name"]
