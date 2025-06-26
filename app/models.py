"""Database models for the core application."""

from django.db import models


class Position(models.Model):
    """Geographic position of a station."""

    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        verbose_name_plural = "positions"


class Stands(models.Model):
    """Availability information for a set of station stands."""

    bikes = models.IntegerField()
    stands = models.IntegerField()
    mechanical_bikes = models.IntegerField()
    electrical_bikes = models.IntegerField()
    electrical_internal_battery_bikes = models.IntegerField()
    electrical_removable_battery_bikes = models.IntegerField()
    capacity = models.PositiveIntegerField(null=True, blank=True)


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
    position = models.OneToOneField(
        Position, on_delete=models.CASCADE, related_name="station", null=True, blank=True
    )
    banking = models.BooleanField(default=False)
    bonus = models.BooleanField(default=False)
    status = models.CharField(max_length=50)
    last_update = models.DateTimeField()
    connected = models.BooleanField(default=True)
    overflow = models.BooleanField(default=False)
    total_stands = models.OneToOneField(
        Stands, on_delete=models.CASCADE, related_name="total_station", null=True, blank=True
    )
    main_stands = models.OneToOneField(
        Stands, on_delete=models.CASCADE, related_name="main_station", null=True, blank=True
    )
    overflow_stands = models.OneToOneField(
        Stands,
        on_delete=models.CASCADE,
        related_name="overflow_station",
        null=True,
        blank=True,
    )

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

