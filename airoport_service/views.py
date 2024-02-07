from django.shortcuts import render
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from airoport_service.models import Airplane, AirplaneType, Airport, Route, Crew, Flight, Order, Ticket
from airoport_service.serializers import AirplaneListSerializer, AirplaneSerializer, AirplaneTypeSerializer, \
    AirportSerializer, RouteSerializer, RouteListSerializer, CrewSerializer, FlightSerializer, FlightListSerializer, \
    FlightDetailSerializer, OrderSerializer, TicketSerializer


class DefaultPaginator(PageNumberPagination):
    page_size = 5
    max_page_size = 100


class AirplaneViewSet(GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    pagination_class = DefaultPaginator

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        return AirplaneSerializer


class AirplaneTypeViewSet(GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    pagination_class = DefaultPaginator


class AirportViewSet(GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    pagination_class = DefaultPaginator


class RouteViewSet(GenericViewSet,
                   mixins.CreateModelMixin, mixins.ListModelMixin):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    pagination_class = DefaultPaginator

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        return RouteSerializer


class CrewViewSet(GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    pagination_class = DefaultPaginator


class FlightViewSet(ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    pagination_class = DefaultPaginator

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer
        return FlightSerializer


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class TicketViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    GenericViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
