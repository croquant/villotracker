"""Management command to import JCDecaux data into the database."""

from datetime import datetime, timezone

from django.core.management.base import BaseCommand

from app.models import Contract, Park, Stand, Station
from libs.jcdecauxclient import JCDecauxClient


class Command(BaseCommand):
    """Import contracts, stations and parks from the JCDecaux API."""

    help = "Import all JCDecaux data"

    def handle(self, *args, **options):  # pragma: no cover - CLI entry point
        client = JCDecauxClient()

        self.stdout.write("Fetching contracts...")
        contracts = client.get_contracts()
        contract_map = {}
        for contract in contracts:
            obj, _ = Contract.objects.update_or_create(
                name=contract.name,
                defaults={
                    "commercial_name": contract.commercial_name,
                    "country_code": contract.country_code,
                    "cities": contract.cities,
                },
            )
            contract_map[contract.name] = obj
        self.stdout.write(f"Imported {len(contract_map)} contracts")

        self.stdout.write("Fetching stations...")
        stations = client.list_stations()
        for station in stations:
            contract = contract_map.get(station.contractName)
            if contract is None:
                continue

            dt = datetime.fromtimestamp(
                int(station.lastUpdate) / 1000, tz=timezone.utc
            )

            station_obj, _ = Station.objects.update_or_create(
                contract=contract,
                number=station.number,
                defaults={
                    "name": station.name,
                    "address": station.address,
                    "position_latitude": station.position.latitude,
                    "position_longitude": station.position.longitude,
                    "banking": station.banking,
                    "bonus": station.bonus,
                    "status": station.status,
                    "last_update": dt,
                    "connected": station.connected,
                    "overflow": station.overflow,
                },
            )

            stand_map = {
                Stand.Kind.TOTAL: station.totalStands,
                Stand.Kind.MAIN: station.mainStands,
                Stand.Kind.OVERFLOW: station.overflowStands,
            }
            for kind, stands in stand_map.items():
                if stands is None:
                    Stand.objects.filter(station=station_obj, kind=kind).delete()
                    continue
                Stand.objects.update_or_create(
                    station=station_obj,
                    kind=kind,
                    defaults={
                        "bikes": stands.bikes,
                        "stands": stands.stands,
                        "mechanical_bikes": stands.mechanicalBikes,
                        "electrical_bikes": stands.electricalBikes,
                        "electrical_internal_battery_bikes": stands.electricalInternalBatteryBikes,
                        "electrical_removable_battery_bikes": stands.electricalRemovableBatteryBikes,
                        "capacity": stands.capacity,
                    },
                )

        self.stdout.write("Fetching parks...")
        for name, contract in contract_map.items():
            try:
                parks = client.list_parks(name)
            except ValueError:
                continue
            for park in parks:
                Park.objects.update_or_create(
                    contract=contract,
                    number=park.number,
                    defaults={
                        "name": park.name,
                        "status": park.status,
                        "position_latitude": park.position.latitude,
                        "position_longitude": park.position.longitude,
                        "access_type": park.accessType,
                        "locker_type": park.lockerType,
                        "has_surveillance": park.hasSurveillance,
                        "is_free": park.isFree,
                        "address": park.address,
                        "zip_code": park.zipCode,
                        "city": park.city,
                        "is_off_street": park.isOffStreet,
                        "has_electric_support": park.hasElectricSupport,
                        "has_physical_reception": park.hasPhysicalReception,
                    },
                )

        self.stdout.write(self.style.SUCCESS("Import completed"))

