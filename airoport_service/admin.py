from django.contrib import admin
from airoport_service.models import Airplane, AirplaneType, Airport, Route, Crew, Flight, Order

admin.site.register(Airport)
admin.site.register(Airplane)
admin.site.register(AirplaneType)
admin.site.register(Route)
admin.site.register(Crew)