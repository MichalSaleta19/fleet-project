from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta
from django.contrib.auth.models import User

# Create your models here.


class FleetUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    driver_license = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Client(FleetUser):
    max_rental_days = models.PositiveIntegerField(default=3)
    is_vip = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Driver(FleetUser):
    hire_date = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class FleetManager(FleetUser):

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Car(models.Model):
    BODY_TYPES = [
        ("Hatchback", "Hatchback"),
        ("Sedan", "Sedan"),
        ("Liftback", "Liftback"),
        ("Kombi", "Kombi"),
        ("SUV", "SUV"),
        ("Van", "Van"),
        ("Cupe", "Cupe"),
        ("Roadster", "Roadster"),
        ("Cabriolet", "Cabriolet"),
        ("Pick-up", "Pick-up"),
    ]

    FUEL_TYPES = [
        ("Petrol", "Petrol"),
        ("Diesel", "Diesel"),
        ("Hybrid PHEV", "HHybrid PHEV"),
        ("Hybrid HEV", "Hybrid HEV"),
        ("Electric", "Electric"),
        ("Hydrogen", "Hydrogen"),
    ]

    TECHNICAL_CONDITION = [
        ("Good condition", "Good condition"),
        ("Need basic service", "Need basic service"),
        ("Need advanced service", "Need advanced service"),
    ]

    brand = models.CharField(max_length=100)  # nazwa marki
    model = models.CharField(max_length=100)  # nazwa model
    year = models.IntegerField()  # rok produkcji
    model_year = models.IntegerField()  # modelowy rok produkcji
    vin_number = models.CharField(max_length=17)  # numery VIN posiadają 17 znaków
    mileage = models.PositiveIntegerField()  # przebieg - musi być dodatny
    registration_number = models.CharField(
        max_length=10
    )  # w polsce standard to 7 znaków, indywidualne więcej
    body_type = models.CharField(
        max_length=20, choices=BODY_TYPES
    )  # rodzaj nadwozia z słownika
    fuel_type = models.CharField(
        max_length=20, choices=FUEL_TYPES
    )  # rodzaj napędu z słownika
    engine_capacity = models.DecimalField(
        max_digits=5, decimal_places=2, null=True
    )  # pojemność silnika
    engine_power = models.PositiveIntegerField()  # moc układu napędowego
    fuel_consumption_1 = models.DecimalField(
        max_digits=6, decimal_places=2
    )  # spalanie cykl niski
    fuel_consumption_2 = models.DecimalField(
        max_digits=6, decimal_places=2
    )  # spalanie cykl średni
    fuel_consumption_3 = models.DecimalField(
        max_digits=6, decimal_places=2
    )  # spalanie cykl wysoki
    color = models.CharField(max_length=50)  # kolor nadwozia
    technical_condition = models.CharField(
        max_length=30, choices=TECHNICAL_CONDITION
    )  # stan techniczny czy sprawny lub uszkodzony
    equipment_list = models.TextField(blank=True, null=True)  # dodatkowe wyposażenie
    seats = models.PositiveIntegerField()  # liczba siedzeń
    trunk_space = models.PositiveIntegerField()  # pojemność bagażnika
    catalog_price = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # cena katalogowa w momencie produkcji
    last_service_date = models.DateField(null=True)  # data ostatniego przeglądu
    service_interval_km = models.PositiveIntegerField(
        default=30000
    )  # interwał przeglądu w kilometrach
    service_interval_months = models.PositiveIntegerField(
        default=12
    )  # interwał przeglądu w miesiącach
    damage = models.TextField(blank=True, null=True)  # uszkodzenia samochodu

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

    def create_year_availability(self):
        current_year = timezone.now().year
        for month in range(1, 13):
            start_date = timezone.datetime(current_year, month, 1)
            end_date = start_date + timedelta(
                days=30
            )  # przy założeniu że miesiąc ma 30 dni
            availability = Availability(
                car=self, start_date=start_date, end_date=end_date, status="Available"
            )
            availability.save()

    def save(self, *args, **kwargs):
        if self.pk is None:  # Jeśli samochód jest nowo utworzony
            super().save(*args, **kwargs)  # zapisanie by uzyskać ID samochodu
            self.create_year_availability()  # utworzenie dostępności na rok od momentu dodania samochodu
            self.last_service_date = (
                timezone.now()
            )  # Ustaw datę ostatniego przeglądu na bieżącą datę
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} {self.model}"


class ServiceHistory(models.Model):
    car = models.ForeignKey("Car", on_delete=models.CASCADE)
    service_date = models.DateField()  # data serwisu
    description = models.TextField()  # opis napraw/czynności
    cost = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # koszt napraw/czynności

    def __str__(self):
        return f"Service for {self.car} on {self.service_date}"

    def save(self, *args, **kwargs):
        if (
            self.pk is None
        ):  # jeśli primarykey nie znajdzie w bazie danych, tworzy nowy samochód i robi przegląd
            car = self.car
            car.last_service_date = (
                self.service_date
            )  # Ustaw datę ostatniego przeglądu na datę serwisu
            car.save()  # Zapisz zmiany w modelu Car
        super().save(
            *args, **kwargs
        )  # jeśli primarykey istnieje, nadal zadziała funkcja save


class Availability(models.Model):
    car = models.ForeignKey("Car", on_delete=models.CASCADE)
    start_date = models.DateField()  # dostępność początkowa data
    end_date = models.DateField()  # dostępność końcowa data
    status_choices = {
        ("Available", "Available"),
        ("Reserved", "Reserved"),
        ("Service", "Service"),
        ("Buffer", "Buffer"),
    }
    status = models.CharField(
        max_length=20, choices=status_choices, default="Available"
    )

    def __str__(self):
        return f"Availability of {self.car} from {self.start_date} to {self.end_date}"


class Order(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)  # samochód
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE
    )  # klient otrzymujący samochód
    driver = models.ForeignKey(
        Driver, on_delete=models.CASCADE, related_name="orders_as_driver"
    )  # kierowca wykonujący
    pickup_date = models.DateField()  # data rozpoczęcia zlecenia
    return_date = models.DateField()  # data zakończenia zlecenia
    distance = models.PositiveIntegerField()  # odległość w kilometrach
    cost = models.PositiveIntegerField()  # koszt zlecenia
    settled = models.BooleanField(
        default=False
    )  # informacja czy zlecenie zostało rozliczone

    def save(self, *args, **kwargs):
        if self.pk is None:  # Jeśli to nowe zamówienie
            super().save(*args, **kwargs)
            # Aktualizacja dostępności samochodu na "Zarezerwowany"
            if self.car.availability_set.filter(status="Available").exists():
                availability = self.car.availability_set.filter(
                    status="Available"
                ).first()
                availability.status = "Reserved"
                availability.save()
        else:  # Jeśli to aktualizacja istniejącego zamówienia
            super().save(*args, **kwargs)


class Events(models.Model):
    name = models.CharField(max_length=255, null=True)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Calendar Events")
        verbose_name_plural = _("Calendar Events")


class Reservation(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    pickup_address = models.TextField()
    created_by_client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    created_by_fleet_manager = models.ForeignKey(
        FleetManager, on_delete=models.CASCADE, null=True
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True)
    canceled = models.BooleanField(default=False)
    canceled_by_client = models.BooleanField(default=False)
    canceled_by_fleet_manager = models.BooleanField(default=False)

    def __str__(self):
        return f"Reservation for {self.car} from {self.start_date} to {self.end_date}"

    def save(self, *args, **kwargs):
        if self.pk is None:
            # save for new reservation
            super().save(*args, **kwargs)
        else:
            # Save for existing reservation
            self.updated_at = timezone.now()
            super().save(*args, **kwargs)
