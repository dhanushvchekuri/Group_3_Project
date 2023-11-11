from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer

from .models import CustomerFeedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = CustomerFeedback
        fields = ['feedback_text']



from django import forms
from .models import Customer


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [ 'email', 'phone', 'address1', 'address2', 'city', 'state_code', 'zip_code', 'country']



from .models import HotelRoom

class HotelRoomForm(forms.ModelForm):
    class Meta:
        model = HotelRoom
        fields = ['number', 'room_type', 'description', 'price_per_night', 'max_occupancy', 'is_available']


from .models import AdditionalService

class AdditionalServiceForm(forms.ModelForm):
    class Meta:
        model = AdditionalService
        fields = ['name', 'description', 'additional_cost']

# forms.py

from .models import RoomBooking

class RoomBookingForm(forms.ModelForm):
    class Meta:
        model = RoomBooking
        fields = ['check_in_date', 'check_out_date', 'number_of_guests']

        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
            'number_of_guests': forms.NumberInput(attrs={'min': 1}),
        }

# forms.py


from .models import HotelPayment

class PaymentForm(forms.ModelForm):
    card_number = forms.CharField(max_length=19, required=True, widget=forms.TextInput(attrs={'placeholder': 'Card Number'}))
    card_expiry_month = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'placeholder': 'MM', 'min': 1, 'max': 12}))
    card_expiry_year = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'placeholder': 'YYYY'}))
    card_cvv = forms.CharField(max_length=4, required=True, widget=forms.TextInput(attrs={'placeholder': 'CVV'}))

    class Meta:
        model = HotelPayment
        fields = ['payment_method', 'amount']

