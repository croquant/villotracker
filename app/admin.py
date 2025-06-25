"""Admin configuration for app models."""

from django.contrib import admin

from .models import Station


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ["contract_name", "number", "name", "status", "last_update"]
    list_filter = ["contract_name", "status", "banking", "bonus"]
    search_fields = ["name", "address", "number"]
