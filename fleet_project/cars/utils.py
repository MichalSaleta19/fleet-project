from datetime import date, timedelta
from .models import Car, Availability


def add_year_availability(car_id, year):
    try:
        car = Car.objects.get(pk=car_id)
    except Car.DoesNotExist:
        return "Samochód o podanym ID nie istnieje."

    # Pobranie początkowej i końcowej daty roku
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)

    # Dodanie wpisu Availabiliti do danego zakresu
    Availability.objects.create(car=car, start_date=start_date, end_date=end_date, status='Available')

    return "Dostępność dla roku {} została dodana.".format(year)
