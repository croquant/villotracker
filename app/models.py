"""Database models for the core application."""

from django.db import models


class TimeStampedModel(models.Model):
    """Abstract base class that adds created and updated fields."""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Contract(TimeStampedModel):
    """A bike rental contract. The primary key is the contract name."""

    name = models.CharField(max_length=100, primary_key=True)
    commercial_name = models.CharField(max_length=255)
    country_code = models.CharField(max_length=10)
    cities = models.JSONField(default=list)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name


class Station(TimeStampedModel):
    """Represent a bike station returned by the JCDecaux API."""

    id = models.CharField(max_length=155, primary_key=True, editable=False)
    number = models.PositiveIntegerField()
    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name="stations",
        null=True,
    )
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    position_latitude = models.FloatField()
    position_longitude = models.FloatField()
    banking = models.BooleanField(default=False)
    bonus = models.BooleanField(default=False)
    status = models.CharField(max_length=50)
    last_update = models.DateTimeField()
    connected = models.BooleanField(default=True)
    overflow = models.BooleanField(default=False)

    class Meta:
        ordering = ["contract", "number"]
        indexes = [models.Index(fields=["contract", "number"])]
        unique_together = ("contract", "number")

    def save(self, *args, **kwargs):
        """Set the primary key based on contract and station number."""
        self.id = f"{self.contract_id}-{self.number}"
        super().save(*args, **kwargs)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.contract_id} {self.number} - {self.name}"


class Stand(TimeStampedModel):
    """Availability and capacity information for a station."""

    class Kind(models.TextChoices):
        TOTAL = "total", "Total"
        MAIN = "main", "Main"
        OVERFLOW = "overflow", "Overflow"

    station = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="stands"
    )
    kind = models.CharField(max_length=8, choices=Kind.choices)
    bikes = models.PositiveIntegerField()
    stands = models.PositiveIntegerField()
    mechanical_bikes = models.PositiveIntegerField()
    electrical_bikes = models.PositiveIntegerField()
    electrical_internal_battery_bikes = models.PositiveIntegerField()
    electrical_removable_battery_bikes = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ("station", "kind")
        indexes = [models.Index(fields=["station", "kind"])]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.station_id} {self.kind}"


class Park(TimeStampedModel):
    """Bike park returned by the JCDecaux API."""

    id = models.CharField(max_length=155, primary_key=True, editable=False)
    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name="parks",
        null=True,
    )
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    position_latitude = models.FloatField()
    position_longitude = models.FloatField()
    access_type = models.CharField(max_length=50)
    locker_type = models.CharField(max_length=50)
    has_surveillance = models.BooleanField()
    is_free = models.BooleanField()
    address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    is_off_street = models.BooleanField()
    has_electric_support = models.BooleanField()
    has_physical_reception = models.BooleanField()

    class Meta:
        ordering = ["contract", "number"]
        indexes = [models.Index(fields=["contract", "number"])]
        unique_together = ("contract", "number")

    def save(self, *args, **kwargs):
        self.id = f"{self.contract_id}-{self.number}"
        super().save(*args, **kwargs)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.contract_id} {self.number} - {self.name}"

