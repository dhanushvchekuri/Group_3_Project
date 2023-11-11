from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

ROOM_TYPES = (
    ('SGL', 'Single Room'),
    ('DBL', 'Double Room'),
    ('DLX', 'Deluxe Room'),
    ('TWN', 'Twin Room'),
    ('KNG', 'King Room'),
    ('STE', 'Suite'),
    ('VIP', 'VIP Suite'),
    ('FAM', 'Family Room'),
)

PAYMENT_METHODS = (
        ('CC', 'Credit Card'),
        ('DC', 'Debit Card'),
    )

# Extend the User model or use a One-To-One Link for additional fields
class Customer(AbstractUser):
    phone = models.CharField(max_length=15)
    address1 = models.TextField()
    address2 = models.TextField(blank=True, null=True)  # Optional second address line
    city = models.CharField(max_length=100, null=True)
    state_code = models.CharField(max_length=2, null=True)
    zip_code = models.CharField(max_length=10, null=True)
    country = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.username  # Changed to use 'username' instead of 'user.username'

class HotelRoom(models.Model):
    number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=3, choices=ROOM_TYPES)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=6, decimal_places=2)
    max_occupancy = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.number} - {self.get_room_type_display()}'

class AdditionalService(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    additional_cost = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class RoomBooking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_guests = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Booking Room number {self.id} by {self.customer}'

    def calculate_total_cost(self):
        total_cost = self.room.price_per_night
        additional_services = BookingService.objects.filter(room_booking=self)
        for service in additional_services:
            total_cost += service.room_service.additional_cost
        return total_cost

class BookingService(models.Model):
    room_booking = models.ForeignKey(RoomBooking, on_delete=models.CASCADE)
    room_service = models.ForeignKey(AdditionalService, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.room_service.name} for Booking {self.room_booking.id}'

class HotelPayment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    room_booking = models.OneToOneField(RoomBooking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=2, choices=PAYMENT_METHODS)
    is_successful = models.BooleanField(default=True)

    def __str__(self):
        return f'Payment {self.id} by {self.customer}'

class PaymentReceipt(models.Model):
    payment = models.OneToOneField(HotelPayment, on_delete=models.CASCADE)
    receipt_date = models.DateTimeField(auto_now_add=True)
    receipt_content = models.TextField(null=True)

    def __str__(self):
        return f'Receipt {self.id} for Payment {self.payment.id}'

class CustomerFeedback(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    feedback_text = models.TextField(null=True)