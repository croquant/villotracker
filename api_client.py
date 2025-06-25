from dataclasses import dataclass, field
from typing import List, Optional

import requests

API_BASE = "https://api.jcdecaux.com"


@dataclass
class Position:
    latitude: float
    longitude: float


@dataclass
class Stands:
    bikes: int
    stands: int
    mechanicalBikes: int
    electricalBikes: int
    electricalInternalBatteryBikes: int
    electricalRemovableBatteryBikes: int
    capacity: Optional[int] = None


@dataclass
class Station:
    number: int
    contractName: str
    name: str
    address: str
    position: Position
    banking: bool
    bonus: bool
    status: str
    lastUpdate: str
    connected: bool
    overflow: bool
    totalStands: Stands
    mainStands: Stands
    overflowStands: Optional[Stands]


@dataclass
class Contract:
    name: str
    commercial_name: str
    country_code: str
    cities: List[str] = field(default_factory=list)


@dataclass
class Park:
    contractName: str
    name: str
    number: int
    status: str
    position: Position
    accessType: str
    lockerType: str
    hasSurveillance: bool
    isFree: bool
    address: str
    zipCode: str
    city: str
    isOffStreet: bool
    hasElectricSupport: bool
    hasPhysicalReception: bool


class JCDecauxClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.params = {"apiKey": api_key}

    def get_contracts(self) -> List[Contract]:
        url = f"{API_BASE}/vls/v3/contracts"
        resp = self.session.get(url)
        resp.raise_for_status()
        data = resp.json()
        return [Contract(**c) for c in data]

    def get_station(self, station_number: int, contract_name: str) -> Station:
        url = f"{API_BASE}/vls/v3/stations/{station_number}"
        params = {"contract": contract_name}
        resp = self.session.get(url, params=params)
        if resp.status_code == 404:
            raise ValueError(
                f"Station {station_number} not found in contract {contract_name}"
            )
        resp.raise_for_status()
        s = resp.json()
        return self._parse_station(s)

    def list_stations(self, contract_name: Optional[str] = None) -> List[Station]:
        url = f"{API_BASE}/vls/v3/stations"
        params = {}
        if contract_name:
            params["contract"] = contract_name
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        return [self._parse_station(s) for s in data]

    def list_parks(self, contract_name: str) -> List[Park]:
        url = f"{API_BASE}/parking/v1/contracts/{contract_name}/parks"
        resp = self.session.get(url)
        if resp.status_code == 400:
            raise ValueError(
                f"Contract {contract_name} not found or does not support parks API"
            )
        resp.raise_for_status()
        data = resp.json()
        return [self._parse_park(p) for p in data]

    def get_park(self, contract_name: str, park_number: int) -> Park:
        url = f"{API_BASE}/parking/v1/contracts/{contract_name}/parks/{park_number}"
        resp = self.session.get(url)
        if resp.status_code == 404:
            raise ValueError(
                f"Park {park_number} not found in contract {contract_name}"
            )
        resp.raise_for_status()
        return self._parse_park(resp.json())

    def _parse_station(self, data: dict) -> Station:
        pos = Position(**data["position"])

        def make_stands(obj):
            av = obj["availabilities"]
            return Stands(**av, capacity=obj.get("capacity"))

        total = make_stands(data["totalStands"])
        main = make_stands(data["mainStands"])
        overflow = None
        if data.get("overflowStands"):
            overflow = make_stands(data["overflowStands"])
        return Station(
            number=data["number"],
            contractName=data["contractName"],
            name=data["name"],
            address=data["address"],
            position=pos,
            banking=data["banking"],
            bonus=data["bonus"],
            status=data["status"],
            lastUpdate=data["lastUpdate"],
            connected=data["connected"],
            overflow=data["overflow"],
            totalStands=total,
            mainStands=main,
            overflowStands=overflow,
        )

    def _parse_park(self, data: dict) -> Park:
        pos = Position(**data["position"])
        return Park(
            contractName=data["contractName"],
            name=data["name"],
            number=data["number"],
            status=data["status"],
            position=pos,
            accessType=data["accessType"],
            lockerType=data["lockerType"],
            hasSurveillance=data["hasSurveillance"],
            isFree=data["isFree"],
            address=data["address"],
            zipCode=data["zipCode"],
            city=data["city"],
            isOffStreet=data["isOffStreet"],
            hasElectricSupport=data["hasElectricSupport"],
            hasPhysicalReception=data["hasPhysicalReception"],
        )
