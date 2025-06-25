"""Database models for the core application."""

from django.db import models


class TimeStampedModel(models.Model):
    """Abstract base class that adds created and updated fields."""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Station(TimeStampedModel):
    """Represent a bike station returned by the JCDecaux API."""

    number = models.PositiveIntegerField()
    contract_name = models.CharField(max_length=100)
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
    total_capacity = models.PositiveIntegerField(null=True, blank=True)
    main_capacity = models.PositiveIntegerField(null=True, blank=True)
    overflow_capacity = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["contract_name", "number"]
        indexes = [models.Index(fields=["contract_name", "number"])]
        unique_together = ("contract_name", "number")

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.contract_name} {self.number} - {self.name}"

