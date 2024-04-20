from .models import Car, Client, Order, Driver, DealerShipUser, DealerShipNetwork, FleetManager, ServiceHistory, Availability
from .forms import CarForm, ClientForm, OrderForm, DriverForm, DealerShipUserForm, DealerShipNetworkForm, FleetManagerForm, ServiceHistoryForm, AvailabilityForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.db.models import Max
from django.urls import reverse_lazy

# Create your views here.


class DashboardView(View):
    def get(self, request):
        context = self.get_context_data()
        return render(request, "dashboard.html", context)

    def get_context_data(self):
        # Liczba pojazdów
        car_count = Car.objects.count()
        # Ostatnio dodany pojazd
        latest_added_car_id = Car.objects.aggregate(Max('id'))['id__max']
        latest_added_car = Car.objects.get(id=latest_added_car_id)
        # Samochód z największym przebiegiem
        car_with_max_mileage = Car.objects.order_by('-mileage').first()
        # Ustawienie kontekstu
        context = {
            "car_count": car_count,
            "latest_added_car": latest_added_car,
            "car_with_max_mileage": car_with_max_mileage
        }
        return context


class CarAddView(CreateView):
    model = Car
    template_name = 'car_add.html'
    form_class = CarForm

    def get_success_url(self):
        return reverse_lazy('car_list')


class CarModifyView(UpdateView):
    model = Car
    template_name = 'car_modify.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('car_list')


class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'
    context_object_name = 'cars'

    def get_queryset(self):
        queryset = super().get_queryset()
        for car in queryset:
            car.needs_service = car.needs_service()
        return queryset


class CarDeleteView(DeleteView):
    model = Car
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('car_list')


class CarDetailsView(DetailView):
    model = Car
    template_name = 'car_details.html'


class ClientListView(ListView):
    model = Client
    template_name = 'client_list.html'
    context_object_name = 'clients'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car_id'] = self.kwargs.get('car_id')
        return context


class ClientAddView(CreateView):
    model = Client
    template_name = 'client_add.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('client_list')


class ClientDetailsView(DetailView):
    model = Client
    template_name = 'client_details.html'


class ClientModifyView(UpdateView):
    model = Client
    template_name = 'client_modify.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('client_list')


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('client_list')


class OrderListView(ListView):
    model = Order
    template_name = 'order_list.html'
    context_object_name = 'orders'


class OrderAddView(CreateView):
    model = Order
    template_name = 'order_add.html'
    form_class = OrderForm

    def get_success_url(self):
        return reverse_lazy('order_list')

    def form_valid(self, form):
        form.instance.car_id = self.request.GET.get('car_id')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car_id = self.kwargs.get('car_id')
        car = Car.objects.get(pk=car_id)
        context['car'] = car
        context['availabilities'] = Availability.objects.filter(car=car, status='available')
        return context


class OrderDetailsView(DetailView):
    model = Order
    template_name = 'order_details.html'


class OrderModifyView(UpdateView):
    model = Order
    template_name = 'order_modify.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['availabilities'] = Availability.objects.all()
        context['clients'] = Client.objects.all()
        return context


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('order_list')


class DriverListView(ListView):
    model = Driver
    template_name = 'driver_list.html'
    context_object_name = 'drivers'


class DriverDetailsView(DetailView):
    model = Driver
    template_name = 'driver_details.html'


class DriverAddView(CreateView):
    model = Driver
    template_name = 'driver_add.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('driver_list')


class DriverModifyView(UpdateView):
    model = Driver
    template_name = 'driver_modify.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('driver_list')


class DriverDeleteView(DeleteView):
    model = Driver
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('driver_list')


class FleetManagerListView(ListView):
    model = FleetManager
    template_name = 'fleetmanager_list.html'


class FleetManagerDetailsView(DetailView):
    model = FleetManager
    template_name = 'fleetmanager_detail.html'


class FleetManagerAddView(CreateView):
    model = FleetManager
    template_name = 'fleetmanager_add.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('fleetmanager_list')


class FleetManagerModifyView(UpdateView):
    model = FleetManager
    template_name = 'fleetmanager_modify.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('fleetmanager_list')


class FleetManagerDeleteView(DeleteView):
    model = FleetManager
    template_name = 'fleetmanager_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('fleetmanager_list')


class DealerShipUserListView(ListView):
    model = DealerShipUser
    template_name = 'dealershipuser_list.html'


class DealerShipUserDetailsView(DetailView):
    model = DealerShipUser
    template_name = 'dealershipuser_details.html'


class DealerShipUserAddView(CreateView):
    model = DealerShipUser
    template_name = 'dealershipuser_add.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('dealershipuser_list')


class DealerShipUserModifyView(UpdateView):
    model = DealerShipUser
    template_name = 'dealershipuser_modify.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('dealershipuser_list')


class DealerShipUserDeleteView(DeleteView):
    model = DealerShipUser
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('dealershipuser_list')


class DealerShipNetworkListView(ListView):
    model = DealerShipNetwork
    template_name = 'dealershipnetwork_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dealership_networks'] = DealerShipNetwork.objects.all()
        return context


class DealerShipNetworkDetailsView(DetailView):
    model = DealerShipNetwork
    template_name = 'dealershipnetwork_details.html'


class DealerShipNetworkAddView(CreateView):
    model = DealerShipNetwork
    template_name = 'dealershipnetwork_add.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('dealershipnetwork_list')


class DealerShipNetworkModifyView(UpdateView):
    model = DealerShipNetwork
    template_name = 'dealershipnetwork_modify.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('dealershipnetwork_list')


class DealerShipNetworkDeleteView(DeleteView):
    model = DealerShipNetwork
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('dealershipnetwork_list')


class ServiceHistoryListView(ListView):
    model = ServiceHistory
    template_name = 'servicehistory_list.html'


class ServiceHistoryDetailsView(DetailView):
    model = ServiceHistory
    template_name = 'servicehistory_details.html'


class ServiceHistoryAddView(CreateView):
    model = ServiceHistory
    template_name = 'servicehistory_add.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('servicehistory_list')


class ServiceHistoryModifyView(UpdateView):
    model = ServiceHistory
    template_name = 'servicehistory_modify.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('servicehistory_list')


class ServiceHistoryDeleteView(DeleteView):
    model = ServiceHistory
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('servicehistory_list')


class AvailabilityListView(ListView):
    model = Availability
    template_name = 'availability_list.html'


class AvailabilityDetailsView(DetailView):
    model = Availability
    template_name = 'availability_details.html'


class AvailabilityAddView(CreateView):
    model = Availability
    template_name = 'availability_add.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('availability_list')


class AvailabilityModifyView(UpdateView):
    model = Availability
    template_name = 'availability_modify.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('availability_list')


class AvailabilityDeleteView(DeleteView):
    model = Availability
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('availability_list')
