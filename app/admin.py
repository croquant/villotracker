"""Admin configuration for app models."""

from django.contrib import admin

from .models import Contract, Park, Stand, Station


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ["name", "commercial_name", "country_code"]


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ["contract", "number", "name", "status", "last_update"]
    list_filter = ["contract", "status", "banking", "bonus"]
    search_fields = ["name", "address", "number"]


@admin.register(Stand)
class StandAdmin(admin.ModelAdmin):
    list_display = ["station", "kind", "capacity", "bikes", "stands"]
    list_filter = ["kind"]
    search_fields = ["station__name"]


@admin.register(Park)
class ParkAdmin(admin.ModelAdmin):
    list_display = ["contract", "number", "name", "status"]
    list_filter = ["contract", "status", "city"]
    search_fields = ["name", "address", "number"]
