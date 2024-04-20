from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.


class Client(models.Model):
    client_user = models.OneToOneField(User, on_delete=models.CASCADE,  related_name='client_user')
    first_name = models.CharField(max_length=100)  # imię klienta
    last_name = models.CharField(max_length=100)  # nazwisko klienta
    address = models.TextField()  # adres klienta
    email = models.EmailField()  # email klienta
    phone_number = models.CharField(max_length=20)  # numer kontaktowy klienta
    driver_license_number = models.CharField(max_length=20)  # numer prawa jazdy klienta
    max_rental_days = models.PositiveIntegerField(default=3)  # maksymalny okres użyczenia
    is_vip = models.BooleanField(default=False)  # czy klient jest VIP

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Driver(Client):  # Driver dziedziczy po Client
    driver_user = models.OneToOneField(User, on_delete=models.CASCADE,  related_name='driver_user')
    hire_date = models.DateField()  # data zatrudnienia
    years_of_service = models.PositiveIntegerField(default=0)  # ile lat przepracował
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=4000)  # wynagrodzenie kierowcy

    def save(self, *args, **kwargs):  # automatyczna aktualizacja zarobków kierowcy o 3% co roku
        years_since_hire = timezone.now().year - self.hire_date.year
        if years_since_hire > self.years_of_service:
            self.years_of_service = years_since_hire
            self.salary *= 1.03
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class FleetManager(Driver):
    fleet_manager_user = models.OneToOneField(User, on_delete=models.CASCADE,  related_name='fleetmanager_user')
    BASE_SALARY = 5000
    def save(self, *args, **kwargs):
        years_since_hire = timezone.now().year - self.hire_date.year
        if years_since_hire > self.years_of_service:
            self.years_of_service = years_since_hire
            self.salary = self.BASE_SALARY * (1 + 0.035 * self.years_of_service)
        super().save(*args, **kwargs)


class DealerShipNetwork(models.Model):
    name = models.CharField(max_length=100)  # Nazwa sieci dealerskiej
    locations = models.TextField()  # Lista lokalizacji

    def __str__(self):
        return self.name


class DealerShipUser(Client):
    dealer_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dealer_user')
    network = models.ForeignKey(DealerShipNetwork, on_delete=models.CASCADE)  # Sieć dealerska

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.network.name})"


class Car(models.Model):
    BODY_TYPES = [
        ('Hatchback', 'Hatchback'),
        ('Sedan', 'Sedan'),
        ('Liftback', 'Liftback'),
        ('Kombi', 'Kombi'),
        ('SUV', 'SUV'),
        ('Van', 'Van'),
        ('Cupe', 'Cupe'),
        ('Roadster', 'Roadster'),
        ('Cabriolet', 'Cabriolet'),
        ('Pick-up', 'Pick-up'),
    ]

    FUEL_TYPES = [
        ('Benzyna', 'Benzyna'),
        ('Diesel', 'Diesel'),
        ('Hybryda PHEV', 'Hybryda PHEV'),
        ('Hybryda HEV', 'Hybryda HEV'),
        ('Elektryczny', 'Elektryczny'),
        ('Wodór', 'Wodór'),
    ]

    brand = models.CharField(max_length=100)  # nazwa marki
    model = models.CharField(max_length=100)  # nazwa model
    year = models.IntegerField()  # rok produkcji
    model_year = models.IntegerField()  # modelowy rok produkcji
    vin_number = models.CharField(max_length=17)  # numery VIN posiadają 17 znaków
    mileage = models.PositiveIntegerField()  # przebieg - musi być dodatny
    registration_number = models.CharField(max_length=10)  # w polsce standard to 7 znaków, indywidualne więcej
    body_type = models.CharField(max_length=20, choices=BODY_TYPES)  # rodzaj nadwozia z słownika
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPES)  # rodzaj napędu z słownika
    engine_capacity = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # pojemność silnika
    engine_power = models.PositiveIntegerField()  # moc układu napędowego
    fuel_consumption_1 = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # spalanie cykl niski
    fuel_consumption_2 = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # spalanie cykl średni
    fuel_consumption_3 = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # spalanie cykl wysoki
    color = models.CharField(max_length=50)  # kolor nadwozia
    technical_condition = models.TextField()  # stan techniczny czy sprawny lub uszkodzony
    equipment_list = models.TextField()  # dodatkowe wyposażenie
    seats = models.PositiveIntegerField()  # liczba siedzeń
    trunk_space = models.PositiveIntegerField()  # pojemność bagażnika
    catalog_price = models.DecimalField(max_digits=10, decimal_places=2)  # cena katalogowa w momencie produkcji
    last_service_date = models.DateField(null=True, blank=True)  # data ostatniego przeglądu
    service_interval_km = models.PositiveIntegerField(default=30000)  # interwał przeglądu w kilometrach
    service_interval_months = models.PositiveIntegerField(default=12)  # interwał przeglądu w miesiącach
    damage = models.TextField(blank=True)  # uszkodzenia samochodu

    def needs_service(self):
        if self.last_service_date is None:
            return True  # Samochód jeszcze nie miał przeglądu
        # Konwertujemy self.last_service_date na obiekt datetime.datetime
        last_service_datetime = timezone.make_aware(
            datetime.combine(self.last_service_date, datetime.min.time())
        )
        # Obliczamy różnicę czasu
        days_since_service = (timezone.now() - last_service_datetime).days
        if days_since_service >= self.service_interval_months * 30:
            return True
        if self.mileage >= self.service_interval_km:
            return True
        return False

    def save(self, *args, **kwargs):
        if self.pk is None:  # Jeśli samochód jest nowo utworzony
            self.last_service_date = timezone.now()  # Ustaw datę ostatniego przeglądu na bieżącą datę
        super().save(*args, **kwargs)

    def is_available(self, start_date, end_date):
        """
        Sprawdza, czy samochód jest dostępny w podanym zakresie dat.
        """
        availability = Availability.objects.filter(
            car=self,
            start_date__lte=start_date,
            end_date__gte=end_date,
            status='Available'
        ).exists()
        return availability

    def __str__(self):
        return f"{self.brand} {self.model}"


class ServiceHistory(models.Model):
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    service_date = models.DateField()  # data serwisu
    description = models.TextField()  # opis napraw/czynności
    cost = models.DecimalField(max_digits=10, decimal_places=2)  # koszt napraw/czynności

    def __str__(self):
        return f"Service for {self.car} on {self.service_date}"

    def save(self, *args, **kwargs):
        if self.pk is None:  # jeśli primarykey nie znajdzie w bazie danych, tworzy nowy samochód i robi przegląd
            car = self.car
            car.last_service_date = self.service_date  # Ustaw datę ostatniego przeglądu na datę serwisu
            car.save()  # Zapisz zmiany w modelu Car
        super().save(*args, **kwargs)


class Availability(models.Model):
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    start_date = models.DateField()  # dostępność początkowa data
    end_date = models.DateField()  # dostępność końcowa data
    status_choices = {
        ('Approved', 'Zatwierdzono'),
        ('Pending', 'Do zatwierdzenia'),
        ('Service', 'Serwis'),
        ('Buffer', 'Dzień buforowy'),
        ('Avaiable', 'Dostępny'),
    }
    status = models.CharField(max_length=20, choices=status_choices, default='Pending')

    def __str__(self):
        return f"Availability of {self.car} from {self.start_date} to {self.end_date}"


class Order(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)  # samochód
    dealership_user = models.ForeignKey(DealerShipUser, on_delete=models.CASCADE, related_name='orders_as_dealership_user')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)  # klient otrzymujący samochód
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='orders_as_driver')  # kierowca wykonujący
    pickup_date = models.DateField()  # data rozpoczęcia zlecenia
    return_date = models.DateField()  # data zakończenia zlecenia
    distance = models.IntegerField()  # odległość w kilometrach
    cost = models.PositiveIntegerField()  # koszt zlecenia
    new_damage = models.BooleanField(default=False)  # nowe uszkodzenia
    settled = models.BooleanField(default=False)  # informacja czy zlecenie zostało rozliczone
