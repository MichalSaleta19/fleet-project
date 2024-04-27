import pytest
from cars.models import (
    FleetUser,
    Client,
    Driver,
    FleetManager,
    Car,
    ServiceHistory,
    Availability,
    Order,
    Reservation,
)


@pytest.fixture
def one_fleet_user():
    return FleetUser.objects.create(
        first_name="Janek",
        last_name="Dowbor",
        address="Wrocław długa 12b",
        email="janek@example.com",
        phone_number="666555222",
        driver_license="1234/12/123456",
    )


@pytest.fixture
def three_fleet_users():
    return (
        FleetUser.objects.create(
            first_name="Janek",
            last_name="Dowbor",
            address="Wrocław długa 12b",
            email="janek@example.com",
            phone_number="666555222",
            driver_license="1234/12/123456",
        ),
        FleetUser.objects.create(
            first_name="Brajanek",
            last_name="Bowbor",
            address="Wrocław krótka 128c",
            email="Brajanek@example.com",
            phone_number="626555222",
            driver_license="1244/12/123456",
        ),
        FleetUser.objects.create(
            first_name="Urszula",
            last_name="Cukier",
            address="Gdańsk wywrotna 2",
            email="urszula@example.com",
            phone_number="444555222",
            driver_license="8234/18/193256",
        ),
    )


@pytest.fixture
def one_client():
    return Client.objects.create(
        first_name="Ania",
        last_name="Umimono",
        address="Poznań szwedzka 12",
        email="ania@example.com",
        phone_number="777444888",
        driver_license="7894/45/789654",
        max_rental_days=7,
        is_vip=True,
    )


@pytest.fixture
def three_clients():
    return (
        Client.objects.create(
            first_name="Jan",
            last_name="Kowalski",
            address="Kraków ul. Wiejska 12",
            email="jan@example.com",
            phone_number="123456789",
            driver_license="7894/44/749644",
            max_rental_days=3,
            is_vip=False,
        ),
        Client.objects.create(
            first_name="Anna",
            last_name="Nowak",
            address="Warszawa ul. Północna 5",
            email="anna@example.com",
            phone_number="987654321",
            driver_license="7294/25/789254",
            max_rental_days=7,
            is_vip=True,
        ),
        Client.objects.create(
            first_name="Katarzyna",
            last_name="Wiśniewska",
            address="Gdańsk ul. Morska 8",
            email="kasia@example.com",
            phone_number="111222333",
            driver_license="7894/41/719624",
            max_rental_days=3,
            is_vip=False,
        ),
    )


@pytest.fixture
def one_driver():
    return Driver.objects.create(
        first_name="Piotr",
        last_name="Segieda",
        address="Żegań wołowska 56",
        email="piotr@example.com",
        phone_number="444111555",
        driver_license="1526/7589/745896",
        hire_date="2020-01-01",
    )


@pytest.fixture
def three_drivers():
    return (
        Driver.objects.create(
            first_name="Piotr",
            last_name="Żesławski",
            address="Olsztyn wioślarzy 22",
            email="piotr2@example.com",
            phone_number="224111555",
            driver_license="2226/4589/745896",
            hire_date="2021-01-01",
        ),
        Driver.objects.create(
            first_name="Mariusz",
            last_name="Polak",
            address="Rzeszów spokojna 1",
            email="mariusz@example.com",
            phone_number="224211355",
            driver_license="2246/449/745896",
            hire_date="2022-01-01",
        ),
        Driver.objects.create(
            first_name="Amelia",
            last_name="Cook",
            address="Warszawa zatracenia 65b",
            email="ameliamaycook@example.com",
            phone_number="274181225",
            driver_license="1426/41489/245896",
            hire_date="2016-01-01",
        ),
    )


@pytest.fixture
def one_fleet_manager():
    return FleetManager.objects.create(
        first_name="Patryk",
        last_name="Miedziński",
        address="Włocławek 66c",
        email="Patryk@example.com",
        phone_number="999666555",
        driver_license="1425/3652/265314",
    )


@pytest.fixture
def three_fleet_managers():
    return (
        FleetManager.objects.create(
            first_name="Patryk",
            last_name="Miedziński",
            address="Włocławek 66c",
            email="patryk@example.com",
            phone_number="999666555",
            driver_license="1425/3652/265314",
        ),
        FleetManager.objects.create(
            first_name="Joanna",
            last_name="Dark",
            address="Łódź centralna 4/16",
            email="joanna@example.com",
            phone_number="9339666555",
            driver_license="1225/3212/261914",
        ),
        FleetManager.objects.create(
            first_name="Tomasz",
            last_name="Moderski",
            address="Śrem 2a",
            email="tomaszk@example.com",
            phone_number="111666555",
            driver_license="2125/2152/665314",
        ),
    )


@pytest.fixture
def one_car():
    return Car.objects.create(
        brand="Toyota",
        model="Century",
        year=1998,
        model_year=1998,
        vin_number="CENTURY1972197200",
        mileage=178900,
        registration_number="CENTURY1972",
        body_type="Sedan",
        fuel_type="Petrol",
        engine_capacity=5.0,
        engine_power=280,
        fuel_consumption_1=10,
        fuel_consumption_2=12,
        fuel_consumption_3=20,
        color="Black",
        technical_condition="Good condition",
        seats=4,
        trunk_space=500,
        catalog_price=25000.00,
        last_service_date="2024-01-15",
        service_interval_km=30000,
        service_interval_months=12,
    )


@pytest.fixture
def three_cars():
    return (
        Car.objects.create(
            brand="Toyota",
            model="Supra",
            year=2004,
            model_year=2004,
            vin_number="SUPRA2JZ30I6GTE00",
            mileage=248900,
            registration_number="THATS SUPRA",
            body_type="Cabriolet",
            fuel_type="Petrol",
            engine_capacity=3.0,
            engine_power=280,
            fuel_consumption_1=10,
            fuel_consumption_2=12,
            fuel_consumption_3=20,
            color="Orange",
            technical_condition="Good condition",
            seats=2,
            trunk_space=200,
            catalog_price=13000.00,
            last_service_date="2024-03-25",
            service_interval_km=20000,
            service_interval_months=12,
        ),
        Car.objects.create(
            brand="BMW",
            model="M3",
            year=2004,
            model_year=2003,
            vin_number="BMWM3M40972197200",
            mileage=298900,
            registration_number="BMW2004CSL",
            body_type="Coupe",
            fuel_type="Petrol",
            engine_capacity=4.0,
            engine_power=420,
            fuel_consumption_1=8,
            fuel_consumption_2=12,
            fuel_consumption_3=28,
            color="Purple",
            technical_condition="Good condition",
            seats=4,
            trunk_space=500,
            catalog_price=55000.00,
            last_service_date="2024-03-25",
            service_interval_km=20000,
            service_interval_months=6,
        ),
        Car.objects.create(
            brand="Datsun",
            model="240Z",
            year=1972,
            model_year=1971,
            vin_number="DATSUN41362393151",
            mileage=18903,
            registration_number="D240Z",
            body_type="Coupe",
            fuel_type="Petrol",
            engine_capacity=2.4,
            engine_power=151,
            fuel_consumption_1=11,
            fuel_consumption_2=15,
            fuel_consumption_3=25,
            color="White",
            technical_condition="Good condition",
            seats=4,
            trunk_space=350,
            catalog_price=45000.00,
            last_service_date="2024-03-25",
            service_interval_km=10000,
            service_interval_months=6,
        ),
    )


@pytest.fixture
def one_service_history(one_car):
    return ServiceHistory.objects.create(
        car=one_car,
        service_date="2024-01-15",
        description="Oil change, break fluid change",
        cost=600,
    )


@pytest.fixture
def one_order(one_car, one_client, one_driver):
    return Order.objects.create(
        car=one_car,
        client=one_client,
        driver=one_driver,
        pickup_date="2024-03-01",
        return_date="2024-03-03",
        distance=450,
        cost=350,
    )


@pytest.fixture
def one_availability(car):
    return Availability.objects.create(
        car=car, start_date="2024-01-01", end_date="2025-01-01", status="Available"
    )


@pytest.fixture
def one_reservation(one_car, one_client):
    return Reservation.objects.create(
        car=one_car,
        start_date="2024-03-01",
        end_date="2024-03-03",
        pickup_address="Wrocław, tymczasowa 154C",
        created_by_client=one_client,
    )
