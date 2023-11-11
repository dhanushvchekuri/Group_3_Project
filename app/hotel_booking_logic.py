from django.shortcuts import render

# Create your views here.

def hotel_home(request):
    return render(request,'hotel_home.html')

from .models import Customer

from django.contrib.auth import login
from django.shortcuts import render, redirect

def admin_signup_logic(request):
    if request.method == 'POST':
        # Get data from the form
        username = request.POST['username']
        password1 = request.POST['admin_password_signup']
        #password2 = request.POST['password2']
        phone = request.POST['admin_phone']
        address1 = request.POST['admin_address1']
        address2 = request.POST['admin_address2']
        city = request.POST['admin_city']
        state = request.POST['admin_state']
        postal_code = request.POST['admin_postal_code']
        country = request.POST['admin_country']

        # Perform custom validation if needed
        # if password1 != password2:
        #     # Passwords do not match, handle the error as needed
        #     return render(request, 'customer_signup.html', {'error_message': 'Passwords do not match'})

        # Create a new Customer object
        customer = Customer.objects.create_user(
            username=username,
            password=password1,
            phone=phone,
            address1=address1,
            address2=address2,
            city=city,
            state_code=state,
            zip_code=postal_code,
            country=country
        )

        customer.set_password(password1)
        customer.is_staff = True
        customer.is_superuser = True
        customer.save()
        # Log the user in
        login(request, customer)
        return redirect('admin_dashboard')

    return render(request, 'hotel_home.html')

def admin_login_logic(request):
    if request.method == 'POST':
        username = request.POST['admin_username']
        password1 = request.POST['admin_password1']

        admin = Customer.objects.filter(username=username).first()

        if admin.check_password(password1):
            return redirect('admin_dashboard')
        return render(request, 'hotel_home.html')
    return render(request, 'hotel_home.html')


def customer_logic_logic(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']

        customer = Customer.objects.filter(username=username).first()

        if customer.check_password(password1):
            return redirect('customer_dashboard')
        return render(request, 'hotel_home.html')
    return render(request, 'hotel_home.html')

def customer_signup_logic(request):
    if request.method == 'POST':
        # Get data from the form
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        address1 = request.POST['address1']
        address2 = request.POST['address2']
        city = request.POST['city']
        state = request.POST['state']
        postal_code = request.POST['postal_code']
        country = request.POST['country']

        # Perform custom validation if needed
        # if password1 != password2:
        #     # Passwords do not match, handle the error as needed
        #     return render(request, 'customer_signup.html', {'error_message': 'Passwords do not match'})

        # Create a new Customer object
        customer = Customer.objects.create_user(
            username=username,
            password=password1,
            phone=phone,
            address1=address1,
            address2=address2,
            city=city,
            state_code=state,
            zip_code=postal_code,
            country=country
        )

        customer.set_password(password1)
        customer.save()
        # Log the user in
        login(request, customer)
        return redirect('customer_dashboard')

    return render(request, 'hotel_home.html')

def customer_dashboard(request):
    return render(request,'customer_home.html')

def admin_dashboard(request):
    return render(request,'admin_dashboard.html')

# views.py

def profile_view(request):
    return render(request, 'customer_profile.html', {'user': request.user})

from .forms import EditProfileForm

def edit_profile_view(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'customer_edit_profile.html', {'form': form})

from .forms import FeedbackForm

# views.py

from .models import RoomBooking
def my_bookings_view(request):
    bookings = RoomBooking.objects.filter(customer=request.user)

    return render(request, 'customer_bookings.html', {'bookings': bookings})


def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.customer = request.user
            feedback.save()
            return redirect('customer_dashboard')
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})

# views.py
from .models import HotelPayment
def payment_details_view(request):
    payments = HotelPayment.objects.filter(customer=request.user)
    return render(request, 'customer_payment_details.html', {'payments': payments})


from .models import CustomerFeedback
def see_feedback_list(request):
    feedbacks = CustomerFeedback.objects.all()
    return render(request,'customer_feedback.html',{'feedbacks':feedbacks})

from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Customer, RoomBooking

def is_staff_user(user):
    return user.is_staff

@login_required
def view_customers(request):
    customers = Customer.objects.filter(is_staff=False)
    customers_with_bookings = []
    for customer in customers:
        customer_bookings = RoomBooking.objects.filter(customer=customer)
        customers_with_bookings.append({
            'customer': customer,
            'bookings': customer_bookings
        })
    return render(request, 'view_customers.html', {'customers_with_bookings': customers_with_bookings})


from .models import HotelRoom
from .forms import HotelRoomForm
from django.shortcuts import get_object_or_404

@login_required
def add_room(request):
    if request.method == 'POST':
        form = HotelRoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('room_list')  # Redirect to the room list view
    else:
        form = HotelRoomForm()
    return render(request, 'add_room.html', {'form': form})

@login_required
def delete_room(request, room_id):

    room = get_object_or_404(HotelRoom, id=room_id)
    room.delete()
    return redirect('room_list')


from .models import AdditionalService
from .forms import AdditionalServiceForm
from django.contrib import messages

@login_required
def add_service(request):

    if request.method == 'POST':
        form = AdditionalServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Service added successfully!")
            return redirect('service_list')
    else:
        form = AdditionalServiceForm()
    return render(request, 'add_service.html', {'form': form})

@login_required
def delete_service(request, service_id):

    service = get_object_or_404(AdditionalService, id=service_id)
    service.delete()
    messages.success(request, "Service deleted successfully!")
    return redirect('service_list')

@login_required
def service_list(request):
    services = AdditionalService.objects.all()
    return render(request, 'service_list.html', {'services': services})



from .models import HotelRoom,ROOM_TYPES
from django.db.models import Q


def room_list(request):
    query = request.GET.get('query', '')
    room_type_filter = request.GET.get('room_type', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    min_occupancy = request.GET.get('min_occupancy', '')
    max_occupancy = request.GET.get('max_occupancy', '')

    rooms = HotelRoom.objects.all()

    if query:
        rooms = rooms.filter(number__icontains=query)

    if room_type_filter:
        rooms = rooms.filter(room_type=room_type_filter)

    if min_price:
        rooms = rooms.filter(price_per_night__gte=min_price)

    if max_price:
        rooms = rooms.filter(price_per_night__lte=max_price)

    if min_occupancy:
        rooms = rooms.filter(max_occupancy__gte=min_occupancy)

    if max_occupancy:
        rooms = rooms.filter(max_occupancy__lte=max_occupancy)

    context = {
        'rooms': rooms,
        'room_types': ROOM_TYPES,
        'selected_type': room_type_filter,
        # Add other filter values to context if needed
    }
    return render(request, 'room_list.html', context)

from .forms import RoomBookingForm
def book_room(request, room_id):
    room = get_object_or_404(HotelRoom, id=room_id, is_available=True)

    if request.method == 'POST':
        form = RoomBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.room = room
            # calculate total_amount or set other fields as needed
            total_cost = booking.calculate_total_cost()
            booking.total_amount = total_cost
            room.is_available = False
            room.save()
            booking.save()
            return redirect('select_services', booking_id=booking.id)
    else:
        form = RoomBookingForm()

    return render(request, 'book_room.html', {'form': form, 'room': room})




from .models import BookingService
@login_required
def select_additional_room_services(request, booking_id):
    booking = get_object_or_404(RoomBooking, id=booking_id, customer=request.user)
    services = AdditionalService.objects.all()

    if request.method == 'POST':
        selected_services = request.POST.getlist('services')
        for service_id in selected_services:
            service = get_object_or_404(AdditionalService, id=service_id)
            BookingService.objects.create(room_booking=booking, room_service=service)
        return redirect('make_payment', booking_id=booking.id)

    return render(request, 'select_services.html', {'services': services, 'booking': booking})


from .forms import PaymentForm
from .models import PaymentReceipt
from django.utils import timezone

def payment_view(request, booking_id):
    booking = get_object_or_404(RoomBooking, id=booking_id, customer=request.user)
    total_cost = booking.calculate_total_cost()

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.customer = request.user
            payment.room_booking = booking
            booking.is_paid = True
            booking.save()
            payment.amount = total_cost  # Set the payment amount to the total cost
            payment.is_successful = True  # Set appropriately based on payment gateway response
            payment.save()
            receipt = PaymentReceipt.objects.create(
                payment=payment,
                receipt_date=timezone.now(),
                receipt_content=f'Receipt for Booking {booking.id}'
            )
            return redirect('booking_list')

    else:
        form = PaymentForm(initial={'amount': total_cost})

    return render(request, 'payment.html', {'form': form, 'booking': booking, 'total_cost': total_cost})

def booking_list(request):
    user = request.user
    bookings = RoomBooking.objects.filter(customer=user).order_by('-check_in_date')
    return render(request, 'booking_list.html', {'bookings': bookings})