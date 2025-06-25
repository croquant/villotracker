from datetime import datetime, timezone

from django.core.management.base import BaseCommand

from app.models import Contract, Station
from libs.jcdecauxclient import JCDecauxClient


class Command(BaseCommand):
    """Import contracts and their stations from the JCDecaux API."""

    help = "Import contracts and stations from JCDecaux API"

    def handle(self, *args, **options):
        client = JCDecauxClient()

        self.stdout.write("Fetching contracts...")
        contracts = client.get_contracts()
        for contract in contracts:
            contract_obj, _ = Contract.objects.update_or_create(
                name=contract.name,
                defaults={
                    "commercial_name": contract.commercial_name or "",
                    "country_code": contract.country_code or "",
                    "cities": contract.cities or [],
                },
            )
            self.stdout.write(
                f"Importing stations for contract {contract.name}..."
            )
            stations = client.list_stations(contract.name)

            for s in stations:
                last_update = datetime.fromtimestamp(
                    int(s.lastUpdate) / 1000, tz=timezone.utc
                )
                Station.objects.update_or_create(
                    contract=contract_obj,
                    number=s.number,
                    defaults={
                        "name": s.name,
                        "address": s.address,
                        "position_latitude": s.position.latitude,
                        "position_longitude": s.position.longitude,
                        "banking": s.banking,
                        "bonus": s.bonus,
                        "status": s.status,
                        "last_update": last_update,
                        "connected": s.connected,
                        "overflow": s.overflow,
                        "total_capacity": s.totalStands.capacity,
                        "main_capacity": s.mainStands.capacity,
                        "overflow_capacity": (
                            s.overflowStands.capacity if s.overflowStands else None
                        ),
                    },
                )

        self.stdout.write(self.style.SUCCESS("Import completed."))
