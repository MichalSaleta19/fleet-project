from .models import Car, Client, Order, Driver, FleetManager, ServiceHistory, Availability, Reservation, FleetUser
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from rules.contrib.views import permission_required
from django.contrib.auth.models import User
# Create your views here.


def dashboard_view(request):
    try:
        # Car counter
        car_count = Car.objects.count()
        # Car latest added
        latest_added_car_id = Car.objects.aggregate(Max('id'))['id__max']
        latest_added_car = Car.objects.get(id=latest_added_car_id)
        # Most mileage Car
        car_with_max_mileage = Car.objects.order_by('-mileage').first()
    except Car.DoesNotExist:
        car_count = 0
        latest_added_car = None
        car_with_max_mileage = None

    # Data Dir context
    context = {
        "car_count": car_count,
        "latest_added_car": latest_added_car,
        "car_with_max_mileage": car_with_max_mileage
    }
    return render(request, "dashboard.html", context)


@permission_required('is_fleet_manager')
def car_add_view(request):
    template_name = 'car_add.html'
    context = {
        'BODY_TYPES': Car.BODY_TYPES,
        'FUEL_TYPES': Car.FUEL_TYPES,
        'TECHNICAL_CONDITION': Car.TECHNICAL_CONDITION
    }
    if request.method == 'POST':
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        year = request.POST.get('year')
        model_year = request.POST.get('model_year')
        vin_number = request.POST.get('vin_number')
        mileage = request.POST.get('mileage')
        registration_number = request.POST.get('registration_number')
        body_type = request.POST.get('body_type')
        fuel_type = request.POST.get('fuel_type')
        engine_capacity = request.POST.get('engine_capacity')
        engine_power = request.POST.get('engine_power')
        fuel_consumption_1 = request.POST.get('fuel_consumption_1')
        fuel_consumption_2 = request.POST.get('fuel_consumption_2')
        fuel_consumption_3 = request.POST.get('fuel_consumption_3')
        color = request.POST.get('color')
        technical_condition = request.POST.get('technical_condition')
        equipment_list = request.POST.get('equipment_list')
        seats = request.POST.get('seats')
        trunk_space = request.POST.get('trunk_space')
        catalog_price = request.POST.get('catalog_price')
        last_service_date = request.POST.get('last_service_date')
        service_interval_km = request.POST.get('service_interval_km')
        service_interval_months = request.POST.get('service_interval_months')
        damage = request.POST.get('damage')

        # validation
        if not brand or not model or not year or not model_year or not vin_number:
            return render(request, template_name, {'error': 'Please fill in all required fields'})

        # Creating Car object filled with data from form
        car_instance = Car.objects.create(
            brand=brand,
            model=model,
            year=year,
            model_year=model_year,
            vin_number=vin_number,
            mileage=mileage,
            registration_number=registration_number,
            body_type=body_type,
            fuel_type=fuel_type,
            engine_capacity=engine_capacity,
            engine_power=engine_power,
            fuel_consumption_1=fuel_consumption_1,
            fuel_consumption_2=fuel_consumption_2,
            fuel_consumption_3=fuel_consumption_3,
            color=color,
            technical_condition=technical_condition,
            equipment_list=equipment_list,
            seats=seats,
            trunk_space=trunk_space,
            catalog_price=catalog_price,
            last_service_date=last_service_date,
            service_interval_km=service_interval_km,
            service_interval_months=service_interval_months,
            damage=damage
        )

        # Create availability for year records for the new car
        car_instance.create_year_availability()

        # Redirect to success URL
        return redirect('car_list')
    else:
        return render(request, template_name, context)


@permission_required('is_fleet_manager')
def car_modify_view(request, car_id):
    template_name = 'car_modify.html'
    car = Car.objects.get(pk=car_id)
    context = {
        'BODY_TYPES': Car.BODY_TYPES,
        'FUEL_TYPES': Car.FUEL_TYPES,
        'TECHNICAL_CONDITION': Car.TECHNICAL_CONDITION,
        'car': car
    }
    if request.method == 'POST':
        # Data from POST request
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        year = request.POST.get('year')
        model_year = request.POST.get('model_year')
        vin_number = request.POST.get('vin_number')
        mileage = request.POST.get('mileage')
        registration_number = request.POST.get('registration_number')
        body_type = request.POST.get('body_type')
        fuel_type = request.POST.get('fuel_type')
        engine_capacity = request.POST.get('engine_capacity')
        engine_power = request.POST.get('engine_power')
        fuel_consumption_1 = request.POST.get('fuel_consumption_1')
        fuel_consumption_2 = request.POST.get('fuel_consumption_2')
        fuel_consumption_3 = request.POST.get('fuel_consumption_3')
        color = request.POST.get('color')
        technical_condition = request.POST.get('technical_condition')
        equipment_list = request.POST.get('equipment_list')
        seats = request.POST.get('seats')
        trunk_space = request.POST.get('trunk_space')
        catalog_price = request.POST.get('catalog_price')
        last_service_date = request.POST.get('last_service_date')
        service_interval_km = request.POST.get('service_interval_km')
        service_interval_months = request.POST.get('service_interval_months')
        damage = request.POST.get('damage')

        # Validation
        if not brand or not model or not year or not model_year or not vin_number:
            return render(request, template_name, {'error': 'Please fill in all required fields'})

        # Update the car instance with the new data
        car.brand = brand
        car.model = model
        car.year = year
        car.model_year = model_year
        car.vin_number = vin_number
        car.mileage = mileage
        car.registration_number = registration_number
        car.body_type = body_type
        car.fuel_type = fuel_type
        car.engine_capacity = engine_capacity
        car.engine_power = engine_power
        car.fuel_consumption_1 = fuel_consumption_1
        car.fuel_consumption_2 = fuel_consumption_2
        car.fuel_consumption_3 = fuel_consumption_3
        car.color = color
        car.technical_condition = technical_condition
        car.equipment_list = equipment_list
        car.seats = seats
        car.trunk_space = trunk_space
        car.catalog_price = catalog_price
        car.last_service_date = last_service_date
        car.service_interval_km = service_interval_km
        car.service_interval_months = service_interval_months
        car.damage = damage

        # Save modified informations
        car.save()

        # Redirect to car list
        return redirect('car_list')
    else:
        return render(request, template_name, context)


def car_list_view(request):
    cars = Car.objects.all()
    return render(request, 'car_list.html', {'cars': cars})


@permission_required('is_fleet_manager')
def car_delete_view(request, car_id):
    template_name = 'confirm_delete.html'

    car = get_object_or_404(Car, pk=car_id)

    if request.method == 'POST':
        # Delete the car instance
        car.delete()
        # Redirect to success URL
        return redirect('car_list')
    else:
        return render(request, template_name, {'car': car})


def car_details_view(request, car_id):
    template_name = 'car_details.html'
    car = get_object_or_404(Car, pk=car_id)
    return render(request, template_name, {'car': car})


@permission_required('is_fleet_manager_or_driver')
def client_list_view(request):
    clients = Client.objects.all()
    return render(request, 'client_list.html', {'clients': clients})


@permission_required('is_fleet_manager_or_driver')
def client_add_view(request):
    template_name = 'client_add.html'

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        driver_license = request.POST.get('driver_license')
        max_rental_days = request.POST.get('max_rental_days')
        is_vip = request.POST.get('is_vip')

        if not first_name or not last_name or not address or not email or not phone_number or not driver_license:
            return render(request, template_name, {'error': 'Please fill in all required fields'})

        client = Client.objects.create(
            first_name=first_name,
            last_name=last_name,
            address=address,
            email=email,
            phone_number=phone_number,
            driver_license=driver_license,
            max_rental_days=max_rental_days,
            is_vip=is_vip
        )
        return redirect('client_list')
    else:
        return render(request, template_name)


@permission_required('is_fleet_manager_or_driver')
def client_details_view(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'client_details.html', {'client': client})


@permission_required('is_fleet_manager_or_driver')
def client_modify_view(request, pk):
    template_name = 'client_modify.html'
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        driver_license = request.POST.get('driver_license')
        max_rental_days = request.POST.get('max_rental_days')
        is_vip = request.POST.get('is_vip')

        if not first_name or not last_name or not address or not email or not phone_number or not driver_license:
            return render(request, template_name, {'error': 'Please fill in all required fields'})

        client.first_name = first_name
        client.last_name = last_name
        client.address = address
        client.email = email
        client.phone_number = phone_number
        client.driver_license = driver_license
        client.max_rental_days = max_rental_days
        client.is_vip = is_vip

        client.save()
        return redirect('client_list')
    else:
        return render(request, template_name, {'client': client})


@permission_required('is_fleet_manager_or_driver')
def client_delete_view(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
    else:
        return render(request, 'confirm_delete.html', {'object': client})


@permission_required('is_fleet_manager_or_driver')
def driver_list_view(request):
    drivers = Driver.objects.all()
    return render(request, 'driver_list.html', {'drivers': drivers})


@permission_required('is_authenticated')
def driver_details_view(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    return render(request, 'driver_details.html', {'driver': driver})


@permission_required('is_fleet_manager_or_driver')
def driver_add_view(request):
    if request.method == 'POST':
        # data from form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        driver_license = request.POST.get('driver_license')
        hire_date = request.POST.get('hire_date')

        # Create new driver
        driver = Driver.objects.create(
            first_name=first_name,
            last_name=last_name,
            address=address,
            email=email,
            phone_number=phone_number,
            driver_license=driver_license,
            hire_date=hire_date
        )
        return redirect('driver_list')
    else:
        return render(request, 'driver_add.html')


@permission_required('is_fleet_manager_or_driver')
def driver_modify_view(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    if request.method == 'POST':
        # Data from form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        driver_license = request.POST.get('driver_license')
        hire_date = request.POST.get('hire_date')

        # Modify driver
        driver.first_name = first_name
        driver.last_name = last_name
        driver.address = address
        driver.email = email
        driver.phone_number = phone_number
        driver.driver_license = driver_license
        driver.hire_date = hire_date
        driver.save()
        return redirect('driver_list')
    else:
        return render(request, 'driver_modify.html', {'driver': driver})


@permission_required('is_fleet_manager')
def driver_delete_view(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    if request.method == 'POST':
        driver.delete()
        return redirect('driver_list')
    else:
        return render(request, 'confirm_delete.html', {'object': driver, 'next_url': 'driver_list'})


@permission_required('is_fleet_manager_or_driver')
def fleet_manager_list_view(request):
    fleet_managers = FleetManager.objects.all()
    return render(request, 'fleetmanager_list.html', {'fleet_managers': fleet_managers})


@permission_required('is_fleet_manager_or_driver')
def fleet_manager_details_view(request, pk):
    fleet_manager = get_object_or_404(FleetManager, pk=pk)
    return render(request, 'fleetmanager_detail.html', {'fleet_manager': fleet_manager})


@permission_required('is_fleet_manager')
def fleet_manager_add_view(request):
    if request.method == 'POST':
        # Pobierz dane z formularza
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        # Stwórz nowego managera floty
        fleet_manager = FleetManager.objects.create(
            first_name=first_name,
            last_name=last_name,
            address=address,
            email=email,
            phone_number=phone_number,
        )
        return redirect('fleetmanager_list')
    else:
        return render(request, 'fleetmanager_add.html')


@permission_required('is_fleet_manager')
def fleet_manager_modify_view(request, pk):
    fleet_manager = get_object_or_404(FleetManager, pk=pk)
    if request.method == 'POST':
        # Pobierz dane z formularza
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        # Zaktualizuj istniejącego managera floty
        fleet_manager.first_name = first_name
        fleet_manager.last_name = last_name
        fleet_manager.address = address
        fleet_manager.email = email
        fleet_manager.phone_number = phone_number
        fleet_manager.save()
        return redirect('fleetmanager_list')
    else:
        return render(request, 'fleetmanager_modify.html', {'fleet_manager': fleet_manager})


@permission_required('is_fleet_manager')
def fleet_manager_delete_view(request, pk):
    fleet_manager = get_object_or_404(FleetManager, pk=pk)
    if request.method == 'POST':
        fleet_manager.delete()
        return redirect('fleetmanager_list')
    else:
        return render(request, 'fleetmanager_confirm_delete.html', {'object': fleet_manager, 'next_url': 'fleetmanager_list'})


@permission_required('is_fleet_manager_or_driver')
def order_list_view(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})

@permission_required('is_authenticated')
def order_add_view(request, car_id):
    if request.method == 'POST':
        # Data from form
        car_id = request.POST.get('car_id')
        client_id = request.POST.get('client_id')
        driver_id = request.POST.get('driver_id')
        pickup_date = request.POST.get('pickup_date')
        return_date = request.POST.get('return_date')
        distance = request.POST.get('distance')
        cost = request.POST.get('cost')

        # Saving new order
        order = Order.objects.create(
            car_id=car_id,
            client_id=client_id,
            driver_id=driver_id,
            pickup_date=pickup_date,
            return_date=return_date,
            distance=distance,
            cost=cost
        )

        # Creating new rezervation
        Reservation.objects.create(
            car_id=car_id,
            start_date=pickup_date,
            end_date=return_date
        )

        # redirect to order_details
        return redirect('order_details', pk=order.pk)
    else:
        # getting all cars
        cars = Car.objects.all()
        # getting all clients
        clients = Client.objects.all()
        # getting all drivers
        drivers = Driver.objects.all()

        context = {
            'car_id': car_id,
            'cars': cars,
            'clients': clients,
            'drivers': drivers
        }
        return render(request, 'order_add.html', context)

@permission_required('is_fleet_manager_or_driver')
def order_modify_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    template_name = 'order_modify.html'

    if request.method == 'POST':
        # Data from form
        car_id = request.POST.get('car_id')
        client_id = request.POST.get('client_id')
        driver_id = request.POST.get('driver_id')
        pickup_date = request.POST.get('pickup_date')
        return_date = request.POST.get('return_date')
        distance = request.POST.get('distance')
        cost = request.POST.get('cost')

        # Validate form data
        if not car_id or not client_id or not driver_id or not pickup_date or not return_date:
            return render(request, template_name, {'error': 'Please fill in all required fields'})

        # Update order instance with new data
        order.car_id = car_id
        order.client_id = client_id
        order.driver_id = driver_id
        order.pickup_date = pickup_date
        order.return_date = return_date
        order.distance = distance
        order.cost = cost

        # Save modified order
        order.save()

        # Redirect to the details view of the modified order
        return HttpResponseRedirect(reverse('order_details', kwargs={'pk': order.pk}))
    else:
        return render(request, template_name, {'order': order})


@permission_required('is_fleet_manager_or_driver')
def order_details_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'order_details.html', {'order': order})


@permission_required('is_fleet_manager_or_driver')
def order_delete_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    else:
        return render(request, 'confirm_delete.html', {'object': order})


@permission_required('is_fleet_manager_or_driver')
def service_history_list_view(request):
    service_history_list = ServiceHistory.objects.all()
    return render(request, 'servicehistory_list.html', {'service_history_list': service_history_list})


@permission_required('is_fleet_manager_or_driver')
def service_history_details_view(request, service_history_id):
    service_history = get_object_or_404(ServiceHistory, pk=service_history_id)
    return render(request, 'servicehistory_details.html', {'service_history': service_history})


@permission_required('is_fleet_manager_or_driver')
def service_history_add_view(request):
    if request.method == 'POST':
        car_id = request.POST.get('car_id')
        service_date = request.POST.get('service_date')
        description = request.POST.get('description')
        cost = request.POST.get('cost')

        # Creating new service history object to car id from POST
        service_history = ServiceHistory(
            car_id=car_id,
            service_date=service_date,
            description=description,
            cost=cost
        )
        service_history.save()
        return redirect('service_history_list')
    else:
        return render(request, 'servicehistory_add.html')


@permission_required('is_fleet_manager_or_driver')
def service_history_modify_view(request, service_history_id):
    service_history = get_object_or_404(ServiceHistory, pk=service_history_id)
    if request.method == 'POST':
        # Data from form
        service_history.service_date = request.POST.get('service_date')
        service_history.description = request.POST.get('description')
        service_history.cost = request.POST.get('cost')
        service_history.save()  # Saving modified service history
        return redirect('service_history_list')
    else:
        return render(request, 'servicehistory_modify.html', {'service_history': service_history})


@permission_required('is_fleet_manager')
def service_history_delete_view(request, service_history_id):
    service_history = get_object_or_404(ServiceHistory, pk=service_history_id)
    if request.method == 'POST':
        service_history.delete()  # Deleting service history
        return redirect('service_history_list')
    else:
        return render(request, 'confirm_delete.html', {'object': service_history})


def availability_list_view(request):
    availability_list = Availability.objects.all()
    return render(request, 'availability_list.html', {'availability_list': availability_list})


def availability_details_view(request, availability_id):
    availability = get_object_or_404(Availability, pk=availability_id)
    return render(request, 'availability_details.html', {'availability': availability})


@permission_required('is_fleet_manager')
def availability_add_view(request):
    if request.method == 'POST':
        car_id = request.POST.get('car_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        status = request.POST.get('status')

        # Creating new Availability
        availability = Availability(
            car_id=car_id,
            start_date=start_date,
            end_date=end_date,
            status=status
        )
        availability.save()
        return redirect('availability_list')
    else:
        return render(request, 'availability_add.html')


@permission_required('is_fleet_manager')
def availability_modify_view(request, availability_id):
    availability = get_object_or_404(Availability, pk=availability_id)
    if request.method == 'POST':
        # Data from form
        availability.start_date = request.POST.get('start_date')
        availability.end_date = request.POST.get('end_date')
        availability.status = request.POST.get('status')
        availability.save()  # saving modified data
        return redirect('availability_list')
    else:
        return render(request, 'availability_modify.html', {'availability': availability})


@permission_required('is_fleet_manager')
def availability_delete_view(request, availability_id):
    availability = get_object_or_404(Availability, pk=availability_id)
    if request.method == 'POST':
        availability.delete()  # Deleting availability
        return redirect('availability_list')
    else:
        return render(request, 'confirm_delete.html', {'object': availability})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('dashboard')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        # checking if user already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error_message': 'Username already exists'})

        # creating user object
        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

        if user:
            # Creating client object
            Client.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=request.POST.get('phone_number'),
                driver_license=request.POST.get('driver_license'),
                address=request.POST.get('address'),
            )

            # New user login
            login(request, user)
            return redirect('dashboard')
        else:
            # Error while creating user
            return render(request, 'register.html', {'error_message': 'Failed to register user'})
    else:
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})
