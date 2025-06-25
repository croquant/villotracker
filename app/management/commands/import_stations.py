from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from libs.jcdecauxclient import JCDecauxClient
from app.models import Station
import os
from datetime import datetime


class Command(BaseCommand):
    help = "Import all stations from the JCDecaux API into the database"

    def handle(self, *args, **options):
        api_key = os.environ.get("API_KEY")
        if not api_key:
            self.stderr.write(self.style.ERROR("API_KEY environment variable not set"))
            return

        client = JCDecauxClient(api_key)
        contracts = client.get_contracts()
        created = 0
        updated = 0
        for contract in contracts:
            stations = client.list_stations(contract.name)
            for s in stations:
                last_update = parse_datetime(s.lastUpdate)
                if last_update is None:
                    try:
                        ts = int(s.lastUpdate) / 1000.0
                        last_update = datetime.fromtimestamp(ts, tz=timezone.utc)
                    except Exception:
                        last_update = None
                obj, created_flag = Station.objects.update_or_create(
                    contract_name=s.contractName,
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
                        "total_capacity": getattr(s.totalStands, "capacity", None),
                        "main_capacity": getattr(s.mainStands, "capacity", None),
                        "overflow_capacity": getattr(s.overflowStands, "capacity", None)
                        if s.overflowStands
                        else None,
                    },
                )
                if created_flag:
                    created += 1
                else:
                    updated += 1
        self.stdout.write(self.style.SUCCESS(f"Created {created} stations, updated {updated} stations"))

