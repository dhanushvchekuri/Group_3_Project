from django.contrib import admin

from app.models import *

admin.site.register(Customer)

admin.site.register(HotelRoom)

admin.site.register(AdditionalService)

admin.site.register(RoomBooking)

admin.site.register(BookingService)

admin.site.register(HotelPayment)


admin.site.register(PaymentReceipt)

admin.site.register(CustomerFeedback)
# Register your models here.
