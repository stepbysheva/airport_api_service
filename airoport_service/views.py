from rest_framework import mixins
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from airoport_service.models import Airplane, AirplaneType, Airport, Route, Crew, Flight, Order, Ticket
from airoport_service.serializers import AirplaneListSerializer, AirplaneSerializer, AirplaneTypeSerializer, \
    AirportSerializer, RouteSerializer, RouteListSerializer, CrewSerializer, FlightSerializer, FlightListSerializer, \
    FlightDetailSerializer, OrderSerializer, TicketSerializer, OrderDetailSerializer


class DefaultPaginator(PageNumberPagination):
    page_size = 5
    max_page_size = 100


class AirplaneViewSet(ListCreateAPIView):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    authentication_classes = (JWTAuthentication,)
    pagination_class = DefaultPaginator

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        return AirplaneSerializer


class AirplaneTypeViewSet(ListCreateAPIView):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    pagination_class = DefaultPaginator


class AirportViewSet(ListCreateAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    pagination_class = DefaultPaginator


class RouteViewSet(GenericViewSet,
                   ListCreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    pagination_class = DefaultPaginator

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        return RouteSerializer


class CrewViewSet(ListCreateAPIView):
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
                   mixins.RetrieveModelMixin,
                   GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = (JWTAuthentication, )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
