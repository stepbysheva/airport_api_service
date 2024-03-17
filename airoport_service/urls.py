from django.urls import path, include
from rest_framework import routers

from airoport_service.views import AirplaneViewSet, AirplaneTypeViewSet, AirportViewSet, RouteViewSet, CrewViewSet, \
    FlightViewSet, OrderViewSet

router = routers.DefaultRouter()


router.register("flights", FlightViewSet)
router.register("orders", OrderViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("airplanes/", AirplaneViewSet.as_view()),
    path("airplane_types/", AirplaneTypeViewSet.as_view()),
    path("airports/", AirportViewSet.as_view()),
    path("routes/", RouteViewSet.as_view()),
    path("crews/", CrewViewSet.as_view())

]


app_name = "airoport_service"
