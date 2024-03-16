from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from airoport_service.models import Airplane, AirplaneType, Airport, Route, Crew, Flight, Order, Ticket


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = "__all__"


class AirplaneListSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source="airplane_type.name")

    class Meta:
        model = Airplane
        fields = ("name", "rows", "seats_in_row", "capacity", "type", "capacity")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = "__all__"


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"


class RouteListSerializer(serializers.ModelSerializer):
    destination = serializers.CharField(source="destination.name")
    source = serializers.CharField(source="source.name")

    class Meta:
        model = Route
        fields = ("source", "destination", "distance")


class CrewSerializer(serializers.ModelSerializer):
    flights = serializers.SlugRelatedField(many=True, slug_field="departure_time", read_only=True)

    class Meta:
        model = Crew
        fields = "first_name", "last_name", "flights"


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = "__all__"


class FlightListSerializer(serializers.ModelSerializer):
    crew = serializers.SlugRelatedField(many=True, slug_field="full_name", read_only=True)
    route = serializers.SerializerMethodField()
    airplane = serializers.CharField(source="airplane.name")

    def get_route(self, object):
        return f"{object.route.source} - {object.route.destination}"

    class Meta:
        model = Flight
        fields = "departure_time", "arrival_time", "route", "airplane", "crew"


class FlightDetailSerializer(serializers.ModelSerializer):
    route = RouteListSerializer()
    airplane = AirplaneListSerializer()
    crew = CrewSerializer(many=True)

    class Meta:
        model = Flight
        fields = ("departure_time", "arrival_time", "route", "airplane", "crew")


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = "__all__"
        extra_kwargs = {"order": {"read_only": True}}
        validators = [UniqueTogetherValidator(Ticket.objects.all(), ("seat", "row", "flight"))]


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(read_only=False)

    class Meta:
        model = Order
        fields = "created_at", "tickets"
        extra_kwargs = {"tickets": {"write_only": True}}

    def create(self, validated_data):
        tickets = validated_data.pop("tickets")
        order = super().create(validated_data)
        for ticket in tickets:
            new_ticket = Ticket.objects.create(**ticket)
            new_ticket.order = order
        return order


class OrderDetailSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer

    class Meta:
        model = Order
        fields = "created_at", "tickets"
