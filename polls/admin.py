from django.contrib import admin
from .models import Bookmaker, Party, OddsReading


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
