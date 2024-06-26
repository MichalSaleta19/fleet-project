import pytest
import pytest_django
from cars.models import Car, FleetUser, Client, Driver, FleetManager
from fleet_project.views import car_add_view
from django.test import RequestFactory, Client
from django.contrib.auth.models import User, Permission, Group
from django.urls import reverse


@pytest.fixture
def fleet_manager_group():
    group, created = Group.objects.get_or_create(name='fleet_manager')
    return group


@pytest.fixture
def driver_group():
    group, created = Group.objects.get_or_create(name='driver')
    return group


@pytest.mark.django_db
def test_unauthorized_access_to_car_add_view(client: Client):
    url = reverse("car_add")
    response = client.get(url)
    assert response.status_code == 302  # is directed somewhere
    assert response.url.startswith(reverse("login"))  # is directed to login page


@pytest.mark.django_db
def test_authorized_access_to_car_add_view(client: Client, one_fleet_manager):
    client.force_login(one_fleet_manager)

    url = reverse("car_add")
    response = client.get(url)
    assert response.status_code == 200  # is view available
    assert "BODY_TYPES" in response.context  # is context valiable
    assert "FUEL_TYPES" in response.context
    assert "TECHNICAL_CONDITION" in response.context


@pytest.mark.django_db
def test_car_add_view_form_validation(
    client: Client, one_fleet_manager, valid_car_data
):
    client.force_login(one_fleet_manager)
    url = reverse("car_add")
    response = client.post(url, valid_car_data)
    assert response.status_code == 302  # is redirected somewhere
    assert response.url == reverse("car_list")  # is redirected to car_list


@pytest.mark.django_db
def test_car_add_view_save_data(client: Client, one_fleet_manager, one_car):
    client.force_login(one_fleet_manager)
    url = reverse("car_add")
    new_car_data = {
        "brand": "BMW",
        "model": "X5",
        "year": 2015,
        "model_year": 2015,
        "vin_number": "BMW18504938504921",
        "mileage": 178900,
        # Możesz wykorzystać dane z istniejącego samochodu one_car
        "registration_number": one_car.registration_number,
        "body_type": one_car.body_type,
        "fuel_type": one_car.fuel_type,
        "engine_capacity": one_car.engine_capacity,
        "engine_power": one_car.engine_power,
        "fuel_consumption_1": one_car.fuel_consumption_1,
        "fuel_consumption_2": one_car.fuel_consumption_2,
        "fuel_consumption_3": one_car.fuel_consumption_3,
        "color": one_car.color,
        "technical_condition": one_car.technical_condition,
        "seats": one_car.seats,
        "trunk_space": one_car.trunk_space,
        "catalog_price": one_car.catalog_price,
        "last_service_date": one_car.last_service_date,
        "service_interval_km": one_car.service_interval_km,
        "service_interval_months": one_car.service_interval_months,
    }

    response = client.post(url, new_car_data)
    assert response.status_code == 302  # is redirected somewhere
    assert response.url == reverse("car_list")  # is redirected to car_list
    new_car = Car.objects.get(brand="BMW", model="X5")  # taking new car from db
    assert new_car is not None  # checking if new car is created


@pytest.mark.django_db
def test_unauthorized_access_to_car_modify_view(client: Client, one_car):
    url = reverse("car_modify", args=[one_car.id])
    response = client.get(url)
    assert response.status_code == 302  # is directed somewhere
    assert response.url.startswith(reverse("login"))  # is directed to login page


@pytest.mark.django_db
def test_authorized_access_to_car_modify_view(
    client: Client, one_car, one_fleet_manager
):
    client.force_login(one_fleet_manager)

    url = reverse("car_modify", args=[one_car.id])
    response = client.get(url)
    assert response.status_code == 200  # is view available
    assert "BODY_TYPES" in response.context  # is context valiable
    assert "FUEL_TYPES" in response.context
    assert "TECHNICAL_CONDITION" in response.context
    assert "car" in response.context


@pytest.mark.django_db
def test_car_modify_view_form_validation(client: Client, one_car, valid_car_data):
    url = reverse("car_modify", args=[one_car.id])
    response = client.post(url, valid_car_data)
    assert response.status_code == 302  # is redirected somewhere
    assert response.url == reverse("car_list")  # is redirected to car_list


@pytest.mark.django_db
def test_car_modify_view_save_data(client: Client, one_car):
    url = reverse("car_modify", args=[one_car.id])
    updated_brand = "BMW"
    updated_color = "White"
    response = client.post(url, {"brand": updated_brand, "color": updated_color})
    assert response.status_code == 302  # is redirected somewhere
    assert response.url == reverse("car_list")  # is redirected to car_list
    one_car.refresh_from_db()  # refresh form
    assert one_car.brand == updated_brand  # is updated brand == brand from db
    assert one_car.color == updated_color  # is updated color == color from db


@pytest.mark.django_db
def test_car_list_view_with_one_car(client: Client, one_car):
    url = reverse("car_list")
    response = client.get(url)
    assert response.status_code == 200  # Is response OK/is view available
    assert len(response.context["cars"]) == 1  # Is 1 car in list


@pytest.mark.django_db
def test_car_list_view_with_three_cars(client: Client, three_cars):
    url = reverse("car_list")
    response = client.get(url)
    assert response.status_code == 200  # Is response OK/is view available
    assert len(response.context["cars"]) == 3  # Are 3 cars in list


@pytest.mark.django_db
def test_car_delete_view(client: Client, one_fleet_manager, one_car):
    client.force_login(one_fleet_manager)
    url = reverse("car_delete", args=[one_car.id])

    response = client.get(url)  # GET to go to confirm delete site
    assert response.status_code == 200  # is response OK
    assert one_car in response.context["car"]  # Is car in context

    response = client.post(url)  # POST to delete a car
    assert response.status_code == 302  # Is redirected to somewhere
    assert not Car.objects.filter(pk=one_car.id).exists()  # Is car deleted from db


@pytest.mark.django_db
def test_car_delete_view_without_permission(client: Client, one_car):
    url = reverse("car_delete", args=[one_car.id])

    response = client.get(url)  # GET to get confirm delete site
    assert response.status_code == 403  # Is returning code 403 (no permissions)

    response = client.post(url)  # POST to delete a car
    assert response.status_code == 403  # Is returning code 403 (no permissions)


@pytest.mark.django_db
def test_car_delete_view_with_driver_permission(client: Client, one_car, one_driver):
    user = User.objects.create_user(username="testuser", password="12345")
    user.groups.add(one_driver.driver_group)

    client.login(username="testuser", password="12345")
    url = reverse("car_delete", args=[one_car.id])

    response = client.get(url)  # GET to get confirm delete site
    assert response.status_code == 403  # Is returning code 403 (no permissions)

    response = client.post(url)  # POST to delete a car
    assert response.status_code == 403  # Is returning code 403 (no permissions)


@pytest.mark.django_db
def test_car_details_view(client: Client, one_car):
    url = reverse("car_details", args=[one_car.id])

    response = client.get(url)  # GET to get details site
    assert response.status_code == 200  # Is response OK
    assert "car" in response.context  # Is car in context
    assert (
        response.context["car"] == one_car
    )  # Is car from context same as one_car from fixture


@pytest.mark.django_db
def test_client_list_view_fleet_manager(client: Client, one_client, one_fleet_manager, fleet_manager_group):
    # create user with fleet manager permissions
    user = User.objects.create_user(username='fleetmanager', password='password')
    user.groups.add(fleet_manager_group)

    # Login as fleet manager
    client.login(username='fleetmanager', password='password')

    # Get to list url
    response = client.get(reverse('client_list'))

    # check if response is ok
    assert response.status_code == 200

    # check if client is in context
    assert one_client in response.context['clients']


@pytest.mark.django_db
def test_client_list_view_driver(client: Client, one_client, one_driver, driver_group):
    # create user with driver permission
    user = User.objects.create_user(username='driver', password='password')
    user.groups.add(driver_group)

    # Login as driver
    client.login(username='driver', password='password')

    # GET to list url
    response = client.get(reverse('client_list'))

    # check if response is ok
    assert response.status_code == 200

    # check if client is in context
    assert one_client in response.context['clients']

@pytest.mark.django_db
def test_client_add_view_authenticated_user(client: Client, one_fleet_user):
    # login as normal user
    client.force_login(one_fleet_user)

    # get to list url
    response = client.get(reverse('client_add'))

    # check if response is - no permissions
    assert response.status_code == 403


@pytest.mark.django_db
def test_client_add_view_fleet_manager(client: Client, one_fleet_manager, fleet_manager_group):
    # create user with fleet manager permissions
    user = User.objects.create_user(username='fleetmanager', password='password')
    user.groups.add(fleet_manager_group)

    # login user as fleet manager
    client.login(username='fleetmanager', password='password')

    # get to client add url
    response = client.get(reverse('client_add'))

    # check if response is ok
    assert response.status_code == 200

    # POST to client add view
    response = client.post(reverse('client_add'), {
        'first_name': 'John',
        'last_name': 'Doe',
        'address': 'New York',
        'email': 'john@example.com',
        'phone_number': '123456789',
        'driver_license': '12345/67/890123',
        'max_rental_days': 7,
        'is_vip': False
    })

    # check if response is redirecting to client list
    assert response.status_code == 302
    assert response.url == reverse('client_list')

    # check if new client is in context
    assert Client.objects.filter(first_name='John', last_name='Doe').exists()
