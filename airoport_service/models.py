from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    @property
    def full_name(self):
        return self.first_name + self.last_name

    def __str__(self):
        return self.first_name


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Airport(models.Model):
    name = models.CharField(max_length=255)
    closest_big_city = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="sources")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="destinations")
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source} - {self.destination}"


class Airplane(models.Model):
    name = models.CharField(max_length=30)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(AirplaneType, on_delete=models.CASCADE)

    @property
    def capacity(self):
        return self.seats_in_row * self.rows

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="flights")
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name="flights")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew, related_name="flights")


class Ticket(models.Model):
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name="tickets"
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="tickets"
    )
    row = models.IntegerField()
    seat = models.IntegerField()

    def __str__(self):
        return (f"{str(self.flight)} "
                f"(row: {self.row}, seat: {self.seat})")

    class Meta:
        unique_together = ("flight", "row", "seat")
        ordering = ["row", "seat"]

