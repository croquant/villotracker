"""Admin configuration for app models."""

from django.contrib import admin

from .models import Station, Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ["name", "commercial_name", "country_code"]


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ["contract", "number", "name", "status", "last_update"]
    list_filter = ["contract", "status", "banking", "bonus"]
    search_fields = ["name", "address", "number"]
