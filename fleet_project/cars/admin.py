from django.contrib import admin
from .models import Car, Client, Driver, FleetManager, DealerShipNetwork, DealerShipUser, Order, Availability, ServiceHistory

# Register your models here.
admin.site.register(Car)
admin.site.register(Client)
admin.site.register(Driver)
admin.site.register(FleetManager)
admin.site.register(DealerShipNetwork)
admin.site.register(DealerShipUser)
admin.site.register(Order)
admin.site.register(Availability)
admin.site.register(ServiceHistory)
