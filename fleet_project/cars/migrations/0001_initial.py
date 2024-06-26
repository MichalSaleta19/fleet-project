# Generated by Django 5.0.4 on 2024-04-24 15:39

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Car",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("brand", models.CharField(max_length=100)),
                ("model", models.CharField(max_length=100)),
                ("year", models.IntegerField()),
                ("model_year", models.IntegerField()),
                ("vin_number", models.CharField(max_length=17)),
                ("mileage", models.PositiveIntegerField()),
                ("registration_number", models.CharField(max_length=10)),
                (
                    "body_type",
                    models.CharField(
                        choices=[
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
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "fuel_type",
                    models.CharField(
                        choices=[
                            ("Petrol", "Petrol"),
                            ("Diesel", "Diesel"),
                            ("Hybrid PHEV", "HHybrid PHEV"),
                            ("Hybrid HEV", "Hybrid HEV"),
                            ("Electric", "Electric"),
                            ("Hydrogen", "Hydrogen"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "engine_capacity",
                    models.DecimalField(decimal_places=2, max_digits=5, null=True),
                ),
                ("engine_power", models.PositiveIntegerField()),
                (
                    "fuel_consumption_1",
                    models.DecimalField(decimal_places=2, max_digits=6),
                ),
                (
                    "fuel_consumption_2",
                    models.DecimalField(decimal_places=2, max_digits=6),
                ),
                (
                    "fuel_consumption_3",
                    models.DecimalField(decimal_places=2, max_digits=6),
                ),
                ("color", models.CharField(max_length=50)),
                (
                    "technical_condition",
                    models.CharField(
                        choices=[
                            ("Good condition", "Good condition"),
                            ("Need basic service", "Need basic service"),
                            ("Need advanced service", "Need advanced service"),
                        ],
                        max_length=30,
                    ),
                ),
                ("equipment_list", models.TextField(blank=True, null=True)),
                ("seats", models.PositiveIntegerField()),
                ("trunk_space", models.PositiveIntegerField()),
                ("catalog_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("last_service_date", models.DateField(null=True)),
                ("service_interval_km", models.PositiveIntegerField(default=30000)),
                ("service_interval_months", models.PositiveIntegerField(default=12)),
                ("damage", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="FleetUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("address", models.TextField()),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("phone_number", models.CharField(max_length=20, unique=True)),
                ("driver_license", models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Events",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, null=True)),
                ("start", models.DateTimeField(null=True)),
                ("end", models.DateTimeField(null=True)),
                ("description", models.TextField(null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Calendar Events",
                "verbose_name_plural": "Calendar Events",
            },
        ),
        migrations.CreateModel(
            name="Availability",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Service", "Service"),
                            ("Reserved", "Reserved"),
                            ("Available", "Available"),
                            ("Buffer", "Buffer"),
                        ],
                        default="Available",
                        max_length=20,
                    ),
                ),
                (
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cars.car"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "fleetuser_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="cars.fleetuser",
                    ),
                ),
                ("max_rental_days", models.PositiveIntegerField(default=3)),
                ("is_vip", models.BooleanField(default=False)),
            ],
            bases=("cars.fleetuser",),
        ),
        migrations.CreateModel(
            name="Driver",
            fields=[
                (
                    "fleetuser_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="cars.fleetuser",
                    ),
                ),
                ("hire_date", models.DateField()),
            ],
            bases=("cars.fleetuser",),
        ),
        migrations.CreateModel(
            name="FleetManager",
            fields=[
                (
                    "fleetuser_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="cars.fleetuser",
                    ),
                ),
            ],
            bases=("cars.fleetuser",),
        ),
        migrations.CreateModel(
            name="ServiceHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("service_date", models.DateField()),
                ("description", models.TextField()),
                ("cost", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cars.car"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("pickup_date", models.DateField()),
                ("return_date", models.DateField()),
                ("distance", models.PositiveIntegerField()),
                ("cost", models.PositiveIntegerField()),
                ("settled", models.BooleanField(default=False)),
                (
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cars.car"
                    ),
                ),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cars.client"
                    ),
                ),
                (
                    "driver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="orders_as_driver",
                        to="cars.driver",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Reservation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("pickup_address", models.TextField()),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(null=True)),
                ("canceled", models.BooleanField(default=False)),
                ("canceled_by_client", models.BooleanField(default=False)),
                ("canceled_by_fleet_manager", models.BooleanField(default=False)),
                (
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cars.car"
                    ),
                ),
                (
                    "created_by_client",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cars.client",
                    ),
                ),
                (
                    "created_by_fleet_manager",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cars.fleetmanager",
                    ),
                ),
            ],
        ),
    ]
