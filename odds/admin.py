from django.contrib import admin
from .models import Bookmaker, Party, ElectionOdds

@admin.register(Bookmaker)
class BookmakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'created_at', 'updated_at')
    list_filter = ('active',)
    search_fields = ('name',)

@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'active', 'created_at', 'updated_at')
    list_filter = ('active',)
    search_fields = ('name',)

@admin.register(ElectionOdds)
class ElectionOddsAdmin(admin.ModelAdmin):
    list_display = ('date', 'party', 'bookmaker', 'odds', 'probability', 'created_at')
    list_filter = ('date', 'party', 'bookmaker')
    search_fields = ('party__name', 'bookmaker__name')
    date_hierarchy = 'date'