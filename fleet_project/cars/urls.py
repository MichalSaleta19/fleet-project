from django.contrib import admin
from django.urls import path, include
from . import views

from django.contrib.auth.views import LogoutView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("", views.dashboard_view, name="dashboard"),
    # Car URLs
    path("car-add/", views.car_add_view, name="car_add"),
    path("car-delete/<int:car_id>/", views.car_delete_view, name="car_delete"),
    path("car-modify/<int:car_id>/", views.car_modify_view, name="car_modify"),
    path("car-details/<int:car_id>/", views.car_details_view, name="car_details"),
    path("car-list/", views.car_list_view, name="car_list"),
    # Client URLs
    path("client-add/", views.client_add_view, name="client_add"),
    path(
        "client-delete/<int:client_id>/", views.client_delete_view, name="client_delete"
    ),
    path(
        "client-modify/<int:client_id>/", views.client_modify_view, name="client_modify"
    ),
    path(
        "client-details/<int:client_id>/",
        views.client_details_view,
        name="client_details",
    ),
    path("client-list/", views.client_list_view, name="client_list"),
    # Order URLs
    path("order-add/<int:car_id>/", views.order_add_view, name="order_add"),
    path("order-delete/<int:order_id>/", views.order_delete_view, name="order_delete"),
    path("order-modify/<int:order_id>/", views.order_modify_view, name="order_modify"),
    path(
        "order-details/<int:order_id>/", views.order_details_view, name="order_details"
    ),
    path("order-list/", views.order_list_view, name="order_list"),
    # Driver URLs
    path("driver-add/", views.driver_add_view, name="driver_add"),
    path("driver-list/", views.driver_list_view, name="driver_list"),
    path(
        "driver-delete/<int:driver_id>/", views.driver_delete_view, name="driver_delete"
    ),
    path(
        "driver-modify/<int:driver_id>/", views.driver_modify_view, name="driver_modify"
    ),
    path(
        "driver-details/<int:driver_id>/",
        views.driver_details_view,
        name="driver_details",
    ),
    # Fleet Manager URLs
    path("fleetmanager-add/", views.fleet_manager_add_view, name="fleetmanager_add"),
    path("fleetmanager-list/", views.fleet_manager_list_view, name="fleetmanager_list"),
    path(
        "fleetmanager-delete/<int:fleetmanager_id>/",
        views.fleet_manager_delete_view,
        name="fleetmanager_delete",
    ),
    path(
        "fleetmanager-modify/<int:fleetmanager_id>/",
        views.fleet_manager_modify_view,
        name="fleetmanager_modify",
    ),
    path(
        "fleetmanager-details/<int:fleetmanager_id>/",
        views.fleet_manager_details_view,
        name="fleetmanager_details",
    ),
    # Service History URLs
    path(
        "servicehistory-add/", views.service_history_add_view, name="servicehistory_add"
    ),
    path(
        "servicehistory-list/",
        views.service_history_list_view,
        name="servicehistory_list",
    ),
    path(
        "servicehistory-delete/<int:servicehistory_id>/",
        views.service_history_delete_view,
        name="servicehistory_delete",
    ),
    path(
        "servicehistory-modify/<int:servicehistory_id>/",
        views.service_history_modify_view,
        name="servicehistory_modify",
    ),
    path(
        "servicehistory-details/<int:servicehistory_id>/",
        views.service_history_details_view,
        name="servicehistory_details",
    ),
    # Availability URLs
    path("availability-add/", views.availability_add_view, name="availability_add"),
    path("availability-list/", views.availability_list_view, name="availability_list"),
    path(
        "availability-delete/<int:availability_id>/",
        views.availability_delete_view,
        name="availability_delete",
    ),
    path(
        "availability-modify/<int:availability_id>/",
        views.availability_modify_view,
        name="availability_modify",
    ),
    path(
        "availability-details/<int:availability_id>/",
        views.availability_details_view,
        name="availability_details",
    ),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("accounts/login/", views.login_view, name="login"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
]
