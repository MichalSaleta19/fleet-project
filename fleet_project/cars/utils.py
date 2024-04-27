from datetime import date, timedelta, datetime
from .models import Car, Availability
from typing import List, Tuple, Dict


def get_car_availability(car_id: int) -> List[Tuple[datetime.date, datetime.date, str]]:
    """
    Zwraca dostępność samochodu o podanym ID jako listę krotek, gdzie każda krotka zawiera
    trzy elementy: (start_date, end_date, status).

    :param car_id: ID samochodu
    :type car_id: int
    :return: Lista krotek zawierająca dostępność samochodu
    :rtype: List[Tuple[datetime.date, datetime.date, str]]
    """
    try:
        car_availability = Availability.objects.filter(car_id=car_id)
    except Availability.DoesNotExist:
        return None

    availability_dict = {}
    for availability in car_availability:
        availability_dict[(availability.start_date, availability.end_date)] = (
            availability.status
        )

    return availability_dict
