from django import forms
from .models import Car, Client, Order, Driver, FleetManager, DealerShipUser, DealerShipNetwork, ServiceHistory, Availability
from django.forms import DateInput
from django.forms.widgets import SelectDateWidget
from django.utils import timezone


class CarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_year = timezone.now().year
        self.fields['year'].widget.choices = [(year, year) for year in range(1900, current_year + 1)]
        self.fields['model_year'].widget.choices = [(year, year) for year in range(1900, current_year + 1)]
        self.fields['year'].initial = 2000  # Ustawienie domyślnej wartości na 2000 - ułatwienie obsługi
        self.fields['model_year'].initial = 2000  # Ustawienie domyślnej wartości na 2000 - ułatwienie obsługi

    last_service_date = forms.DateField(label='Data ostatniego przeglądu', required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Car
        fields = '__all__'
        labels = {
            'year': 'Rok produkcji',
            'model_year': 'Modelowy rok produkcji',
            'seats': 'Liczba siedzeń',
        }

    def clean_last_service_date(self):
        last_service_date = self.cleaned_data.get('last_service_date')
        if last_service_date is None:  # Jeśli data ostatniego przeglądu jest pusta
            return timezone.now().date()  # Ustaw datę ostatniego przeglądu na bieżącą datę
        return last_service_date


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = '__all__'


class FleetManagerForm(forms.ModelForm):
    class Meta:
        model = FleetManager
        fields = '__all__'


class DealerShipNetworkForm(forms.ModelForm):
    class Meta:
        model = DealerShipNetwork
        fields = '__all__'


class DealerShipUserForm(forms.ModelForm):
    class Meta:
        model = DealerShipUser
        fields = '__all__'


class ServiceHistoryForm(forms.ModelForm):
    class Meta:
        model = ServiceHistory
        fields = '__all__'


class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = '__all__'


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['car', 'dealership_user', 'client', 'driver', 'pickup_date', 'return_date', 'distance', 'cost', 'new_damage', 'settled']