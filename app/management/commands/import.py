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
                raw_last_update = s.lastUpdate
                if isinstance(raw_last_update, str):
                    try:
                        last_update = datetime.fromisoformat(
                            raw_last_update.replace("Z", "+00:00")
                        )
                    except ValueError:
                        last_update = datetime.fromtimestamp(
                            int(raw_last_update) / 1000,
                            tz=timezone.utc,
                        )
                else:
                    last_update = datetime.fromtimestamp(
                        raw_last_update / 1000,
                        tz=timezone.utc,
                    )
                Station.objects.update_or_create(
                    contract=contract_obj,
                    number=int(s.number),
                    defaults={
                        "name": s.name,
                        "address": s.address,
                        "position_latitude": float(s.position.latitude),
                        "position_longitude": float(s.position.longitude),
                        "banking": bool(s.banking),
                        "bonus": bool(s.bonus),
                        "status": s.status,
                        "last_update": last_update,
                        "connected": bool(s.connected),
                        "overflow": bool(s.overflow),
                        "total_capacity": (
                            int(s.totalStands.capacity)
                            if s.totalStands.capacity is not None
                            else None
                        ),
                        "main_capacity": (
                            int(s.mainStands.capacity)
                            if s.mainStands.capacity is not None
                            else None
                        ),
                        "overflow_capacity": (
                            int(s.overflowStands.capacity)
                            if getattr(s.overflowStands, "capacity", None) is not None
                            else None
                        ),
                    },
                )

        self.stdout.write(self.style.SUCCESS("Import completed."))
