from django.contrib import admin
from .models import (
    Car,
    Client,
    Driver,
    FleetManager,
    Order,
    Availability,
    ServiceHistory,
)

# Register your models here.
admin.site.register(Car)
admin.site.register(Client)
admin.site.register(Driver)
admin.site.register(FleetManager)
admin.site.register(Order)
admin.site.register(Availability)
admin.site.register(ServiceHistory)
