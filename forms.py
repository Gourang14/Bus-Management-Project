from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
# from django import forms.forms import 
from django.contrib.auth.models import User

class CreateuserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

from django import forms
from .models import Booking

class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['num_tickets', 'name', 'address', 'phone', 'age']
        # fields = ['name', 'address', 'phone', 'age']
        labels = {
           'num_tickets': 'Number of Tickets',
            'name': 'Name',
            'address': 'Address',
            'phone': 'Phone Number',
            'age': 'Age',
        }
        widgets = {
            'num_tickets': forms.NumberInput(attrs={'min': 1}),
            'age': forms.NumberInput(attrs={'min': 0}),
        }

    seat_number = forms.IntegerField(
        label='Seat Number',
        required=False,
        widget=forms.NumberInput(attrs={'min': 1}),
    )

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        if 'num_tickets' in self.initial:
            ticket_price = self.instance.ticket_price
            num_tickets = self.initial['num_tickets']
            if ticket_price and num_tickets:
                total_price = ticket_price * num_tickets
                self.initial['total_price'] = total_price

