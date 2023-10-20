from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import random
import string

# models.py

from django.utils import timezone

class BusRoute(models.Model):
    class Meta:
        app_label = 'busapp1' 
    name = models.CharField(max_length=100)
    # Add other fields like source, destination, etc.

def get_current_time():
    return timezone.now().time()

class BusSchedule(models.Model):
    class Meta:
        app_label = 'busapp1' 
    route = models.ForeignKey(BusRoute, on_delete=models.CASCADE)
    departure_time = models.TimeField()
    arrival_time = models.TimeField(default=get_current_time)
class Contacts(models.Model):
    name = models.CharField(max_length=100 ,default='Some Default Name')
    email = models.EmailField()
    address = models.CharField(max_length=200, default='Some Default Value')
    message = models.TextField(default='Some Default Message')

    def __str__(self):
        return self.name
    
def default_departure_time():
    return timezone.now()

class Bus(models.Model):
    name = models.CharField(max_length=100)
    departure_time = models.DateTimeField(default=default_departure_time)
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)  # Add ticket_price

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    num_tickets = models.IntegerField( default=1)
    booking_time = models.DateTimeField()
    name = models.CharField(max_length=255, default="")
    address = models.TextField(default="")
    phone = models.CharField(max_length=15, default="")
    age = models.IntegerField(default=0)
    ticket_number = models.CharField(max_length=10,unique=True,default="")  # Add ticket_number
    seat_number = models.IntegerField(null=True, default=None)  # Add seat_number
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)  # Add ticket_price
    def generate_ticket_number(self):
        # Generate a random ticket number, e.g., a combination of letters and digits
        ticket_chars = string.ascii_letters + string.digits
        return ''.join(random.choice(ticket_chars) for _ in range(10))
    def save(self, *args, **kwargs):
        # Calculate total price and seat number based on your logic
        # For example, if the price is based on the number of tickets and seat number is random:

        self.total_price = self.num_tickets * self.bus.ticket_price
        self.seat_number = random.randint(1, self.bus.total_seats)

        super().save(*args, **kwargs)





    # Add other fields as needed



