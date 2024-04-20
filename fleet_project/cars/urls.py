from django.contrib import admin
from django.urls import path, include
from .views import (DashboardView, CarAddView, CarDeleteView, CarModifyView, CarListView,  CarDetailsView, ClientAddView,
                    ClientDetailsView, ClientDeleteView, ClientModifyView, ClientListView, OrderAddView, OrderDetailsView,
                    OrderDeleteView, OrderModifyView, OrderListView, DriverAddView, DriverDetailsView, DriverDeleteView,
                    DriverModifyView, DriverListView, FleetManagerAddView, FleetManagerDetailsView,
                    FleetManagerDeleteView, FleetManagerModifyView, FleetManagerListView, DealerShipUserAddView,
                    DealerShipUserDetailsView, DealerShipUserDeleteView, DealerShipUserModifyView,
                    DealerShipUserListView, DealerShipNetworkAddView, DealerShipNetworkDetailsView,
                    DealerShipNetworkDeleteView, DealerShipNetworkModifyView, DealerShipNetworkListView,
                    ServiceHistoryAddView, ServiceHistoryDetailsView, ServiceHistoryDeleteView, ServiceHistoryModifyView,
                    ServiceHistoryListView, AvailabilityAddView, AvailabilityDetailsView, AvailabilityDeleteView,
                    AvailabilityModifyView, AvailabilityListView)


urlpatterns = [
#    path('admin/', admin.site.urls),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('', DashboardView.as_view(), name='dashboard'),
    # Car URL's
    path('car-add/', CarAddView.as_view(), name='car_add'),
    path('car-delete/<int:pk>/', CarDeleteView.as_view(), name='car_delete'),
    path('car-modify/<int:pk>/', CarModifyView.as_view(), name="car_modify"),
    path('car-details/<int:pk>/', CarDetailsView.as_view(), name='car_details'),
    path('car-list/', CarListView.as_view(), name='car_list'),
    # Client URL's
    path('clients/<int:car_id>/', ClientListView.as_view(), name='client_list'),
    path('client-add/', ClientAddView.as_view(), name='client_add'),
    path('client-delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('client-modify/<int:pk>/', ClientModifyView.as_view(), name='client_modify'),
    path('client-details/<int:pk>/', ClientDetailsView.as_view(), name='client_details'),
    path('client-list/', ClientListView.as_view(), name='client_list'),
    # Order URL's
    path('order-add/<int:car_id>/', OrderAddView.as_view(), name='order_add'),
    #path('order-add/<int:car_id>/<int:client_id>/', OrderAddView.as_view(), name='order_add'),
    path('order-delete/<int:pk>/', OrderDeleteView.as_view(), name='order_delete'),
    path('order-modify/<int:pk>/', OrderModifyView.as_view(), name='order_modify'),
    path('order-details/<int:pk>/', OrderDetailsView.as_view(), name='order_details'),
    path('order-list/', OrderListView.as_view(), name='order_list'),
    # Driver URL's
    path('driver-add/', DriverAddView.as_view(), name='driver_add'),
    path('driver-list/', DriverListView.as_view(), name='driver_list'),
    path('driver-delete/<int:pk>/', DriverDeleteView.as_view(), name='driver_delete'),
    path('driver-modify/<int:pk>/', DriverModifyView.as_view(), name='driver_modify'),
    path('driver-details/<int:pk>/', DriverDetailsView.as_view(), name='driver_details'),
    # Fleet manager URL's
    path('fleetmanager-add/', FleetManagerAddView.as_view(), name='fleetmanager_add'),
    path('fleetmanager-list/', FleetManagerListView.as_view(), name='fleetmanager_list'),
    path('fleetmanager-delete/<int:pk>/', FleetManagerDeleteView.as_view(), name='fleetmanager_delete'),
    path('fleetmanager-modify/<int:pk>/', FleetManagerModifyView.as_view(), name='fleetmanager_modify'),
    path('fleetmanager-details/<int:pk>/', FleetManagerDetailsView.as_view(), name='fleetmanager_details'),
    # dealer ship user URL's
    path('dealershipuser-add/', DealerShipUserAddView.as_view(), name='dealershipuser_add'),
    path('dealershipuser-list/', DealerShipUserListView.as_view(), name='dealershipuser_list'),
    path('dealershipuser-delete/<int:pk>/', DealerShipUserDeleteView.as_view(), name='dealershipuser_delete'),
    path('dealershipuser-modify/<int:pk>/', DealerShipUserModifyView.as_view(), name='dealershipuser_modify'),
    path('dealershipuser-details/<int:pk>/', DealerShipUserDetailsView.as_view(), name='dealershipuser_details'),
    # dealer ship network URL's
    path('dealershipnetwork-add/', DealerShipNetworkAddView.as_view(), name='dealershipnetwork_add'),
    path('dealershipnetwork-list/', DealerShipNetworkListView.as_view(), name='dealershipnetwork_list'),
    path('dealershipnetwork-delete/<int:pk>/', DealerShipNetworkDeleteView.as_view(), name='dealershipnetwork_delete'),
    path('dealershipnetwork-modify/<int:pk>/', DealerShipNetworkModifyView.as_view(), name='dealershipnetwork_modify'),
    path('dealershipnetwork-details/<int:pk>/', DealerShipNetworkDetailsView.as_view(), name='dealershipnetwork_details'),
    # service history URL's
    path('servicehistory-add/', ServiceHistoryAddView.as_view(), name='servicehistory_add'),
    path('servicehistory-list/', ServiceHistoryListView.as_view(), name='servicehistory_list'),
    path('servicehistory-delete/<int:pk>/', ServiceHistoryDeleteView.as_view(), name='servicehistory_delete'),
    path('servicehistory-modify/<int:pk>/', ServiceHistoryModifyView.as_view(), name='servicehistory_modify'),
    path('servicehistory-details/<int:pk>/', ServiceHistoryDetailsView.as_view(), name='servicehistory_details'),
    # availability URL's
    path('availability-add/', AvailabilityAddView.as_view(), name='availability_add'),
    path('availability-list/', AvailabilityListView.as_view(), name='availability_list'),
    path('availability-delete/<int:pk>/', AvailabilityDeleteView.as_view(), name='availability_delete'),
    path('availability-modify/<int:pk>/', AvailabilityModifyView.as_view(), name='availability_modify'),
    path('availability-details/<int:pk>/', AvailabilityDetailsView.as_view(), name='availability_details'),
]
