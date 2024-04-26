import pytest
import pytest_django
from cars.models import Car, FleetUser, Client, Driver, FleetManager
from fleet_project.views import car_add_view
from django.test import RequestFactory, Client
from django.contrib.auth.models import User, Permission
from django.urls import reverse


@pytest.mark.django_db
def test_unauthorized_access_to_car_modify_view(client: Client, one_car):
    url = reverse('car_modify', args=[one_car.id])
    response = client.get(url)
    assert response.status_code == 302  # is directed somewhere
    assert response.url.startswith(reverse('login'))  # is directed to login page


@pytest.mark.django_db
def test_authorized_access_to_car_modify_view(client: Client, one_car, one_fleet_manager):
    client.force_login(one_fleet_manager)

    url = reverse('car_modify', args=[one_car.id])
    response = client.get(url)
    assert response.status_code == 200  # is view available
    assert 'BODY_TYPES' in response.context  # is context valiable
    assert 'FUEL_TYPES' in response.context
    assert 'TECHNICAL_CONDITION' in response.context
    assert 'car' in response.context


@pytest.mark.django_db
def test_unauthorized_access_to_car_add_view(client: Client):
    url = reverse('car_add')
    response = client.get(url)
    assert response.status_code == 302  # is directed somewhere
    assert response.url.startswith(reverse('login'))  # is directed to login page


@pytest.mark.django_db
def test_authorized_access_to_car_add_view(client: Client, one_fleet_manager):
    client.force_login(one_fleet_manager)

    url = reverse('car_add')
    response = client.get(url)
    assert response.status_code == 200  # is view available
    assert 'BODY_TYPES' in response.context  # is context valiable
    assert 'FUEL_TYPES' in response.context
    assert 'TECHNICAL_CONDITION' in response.context


@pytest.mark.django_db
def test_car_modify_view_form_validation(client: Client, one_car, valid_car_data):
    url = reverse('car_modify', args=[one_car.id])
    response = client.post(url, valid_car_data)
    assert response.status_code == 302  # is redirected somewhere
    assert response.url == reverse('car_list')  # is redirected to car_list


@pytest.mark.django_db
def test_car_add_view_form_validation(client: Client, one_fleet_manager, valid_car_data):
    client.force_login(one_fleet_manager)
    url = reverse('car_add')
    response = client.post(url, valid_car_data)
    assert response.status_code == 302  # is redirected somewhere
    assert response.url == reverse('car_list')  # is redirected to car_list


@pytest.mark.django_db
def test_car_modify_view_save_data(client: Client, one_car):
    url = reverse('car_modify', args=[one_car.id])
    updated_brand = 'BMW'
    updated_color = 'White'
    response = client.post(url, {'brand': updated_brand, 'color': updated_color})
    assert response.status_code == 302  # is redirected somewhere
    assert response.url == reverse('car_list')  # is redirected to car_list
    one_car.refresh_from_db()  # refresh form
    assert one_car.brand == updated_brand  # is updated brand == brand from db
    assert one_car.color == updated_color  # is updated color == color from db

@pytest.mark.django_db
def test_car_add_view_save_data(client: Client, one_fleet_manager):
    client.force_login(one_fleet_manager)
    url = reverse('car_add')
    new_car_data = {
        'brand': 'BMW',
        'model': 'X5',
        'year': 2015,
        'model_year': 2015,
        'vin_number': 'VIN987654321',
        # Pozostałe pola pominięte dla uproszczenia
    }
    response = client.post(url, new_car_data)
    assert response.status_code == 302  # is redirected somewhere
    assert response.url == reverse('car_list')  # is redirected to car_list
    new_car = Car.objects.get(brand='BMW', model='X5')  # taking new car from db
    assert new_car is not None  # checking if new car is created