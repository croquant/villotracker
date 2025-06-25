from dataclasses import dataclass, field
from typing import List, Optional


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
