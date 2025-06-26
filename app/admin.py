"""Admin configuration for app models."""

from django.contrib import admin

from .models import Contract, Position, Stands, Station


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ["name", "commercial_name", "country_code"]


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ["latitude", "longitude"]


@admin.register(Stands)
class StandsAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "bikes",
        "stands",
        "mechanical_bikes",
        "electrical_bikes",
        "capacity",
    ]


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ["contract", "number", "name", "status", "last_update"]
    list_filter = ["contract", "status", "banking", "bonus"]
    search_fields = ["name", "address", "number"]
