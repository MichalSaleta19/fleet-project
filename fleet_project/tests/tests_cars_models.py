import pytest
import pytest_django
from cars.models import Car, FleetUser, Client, Driver, FleetManager



@pytest.mark.django_db
def test_create_one_fleet_user(one_fleet_user):
    fleetuser = FleetUser.objects.get(id=one_fleet_user.id)
    assert fleetuser.first_name == "Janek"
    assert fleetuser.last_name == "Dowbor"
    assert fleetuser.address == "Wrocław długa 12b"
    assert fleetuser.email == "janek@example.com"
    assert fleetuser.phone_number == "666555222"
    assert fleetuser.driver_license == "1234/12/123456"


@pytest.mark.django_db
def test_create_three_fleet_users(three_fleet_users):
    FleetUsers = FleetUser.objects.all()
    assert len(FleetUsers) == 3


@pytest.mark.django_db
def test_create_one_client(one_client):
    client = Client.objects.get(id=one_client.id)
    assert client.first_name == "Ania"
    assert client.last_name == "Umimono"
    assert client.address == "Poznań szwedzka 12"
    assert client.email == "ania@example.com"
    assert client.phone_number == "777444888"
    assert client.driver_license == "7894/45/789654"
    assert client.max_rental_days == 7
    assert client.is_vip == True


@pytest.mark.django_db
def test_create_three_clients(three_clients):
    clients = Client.objects.all()
    assert len(clients) == 3


@pytest.mark.django_db
def test_create_one_driver(one_driver):
    driver = Driver.objects.get(id=one_driver.id)
    assert driver.first_name == "Piotr"
    assert driver.last_name == "Segieda"
    assert driver.address == "Żegań wołowska 56"
    assert driver.email == "piotr@example.com"
    assert driver.phone_number == "444111555"
    assert driver.driver_license == "1526/7589/745896"
    assert driver.hire_date == "2020-01-01"



@pytest.mark.django_db
def test_create_three_drivers():
    drivers = Driver.objects.all()
    assert len(drivers) == 3


@pytest.mark.django_db
def test_create_one_fleet_manager(one_fleet_manager):
    fleetmanager = FleetManager.objects.get(id=one_fleet_manager)
    assert fleetmanager.first_name == "Patryk"
    assert fleetmanager.last_name == "Miedziński"
    assert fleetmanager.address == "Włocławek 66c"
    assert fleetmanager.email == "Patryk@example.com"
    assert fleetmanager.phone_number == "999666555"
    assert fleetmanager.driver_license == "1425/3652/265314"


@pytest.mark.django_db
def test_create_three_fleet_managers(three_fleet_managers):
    fleetmanagers = FleetManager.objects.all()
    assert len(fleetmanagers) == 3


@pytest.mark.django_db
def test_create_one_car(one_car):
    car = Car.objects.get(id=one_car.id)
    assert car.brand == "Toyota"
    assert car.model == "Century"
    assert car.year == 1998
    assert car.model_year == 1998
    assert car.vin_number == "CENTURY1972197200"
    assert car.mileage == 178900
    assert car.registration_number == "CENTURY1972"
    assert car.body_type == "Sedan"
    assert car.fuel_type == "Petrol"
    assert car.engine_capacity == 5.0
    assert car.engine_power == 280
    assert car.fuel_consumption_1 == 10
    assert car.fuel_consumption_2 == 12
    assert car.fuel_consumption_3 == 20
    assert car.color == "Black"
    assert car.technical_condition == "Good condition"
    assert car.seats == 4
    assert car.trunk_space == 500
    assert car.catalog_price == 25000.00
    assert car.last_service_date == "2024-01-15"
    assert car.service_interval_km == 30000
    assert car.service_interval_months == 12


@pytest.mark.django_db
def test_create_three_cars(three_cars):
    cars = Car.objects.all()
    assert len(cars) == 3


@pytest.mark.django_db
def test_create_one_service_history(one_service_history):
    service_history = ServiceHistory.objects.get(id=one_service_history.id)
    assert service_history.service_date == "2024-01-15"
    assert service_history.description == "Oil change, break fluid change"
    assert service_history.cost == 600



@pytest.mark.django_db
def test_create_one_order(one_order):
    order = Order.objects.get(id=one_order.id)
    assert order.pickup_date == "2024-03-01"
    assert order.return_date == "2024-03-03"
    assert order.distance == 450
    assert order.cost == 350


@pytest.mark.django_db
def test_create_one_availability(one_availability):
    availability = Availability.objects.get(id=one_availability.id)
    assert availability.start_date == "2024-01-01"
    assert availability.end_date == "2025-01-01"
    assert availability.status == "Available"


@pytest.mark.django_db
def test_create_one_reservation(one_reservation):
    reservation = Reservation.objects.get(id=one_reservation.id)
    assert reservation.start_date == "2024-03-01"
    assert reservation.end_date == "2024-03-03"
    assert reservation.pickup_address == "Wrocław, tymczasowa 154C"
