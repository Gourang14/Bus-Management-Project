from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views import View  # Add this line to import View
from django.contrib.auth import login, authenticate ,logout
from django.http import HttpResponse
from .forms import CreateuserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt




# myapp/views.py
from .models import BusRoute
from .models import BusSchedule
from .models import Contacts
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


def index(request):
    # Your view logic here
    return render(request, 'index.html')
def index_html(request):
    return render(request,'index.html')
def reg(request):
    return render(request,'registraion.html')
def about(request):
    # return HttpResponse("This is the about page")
    return render(request,'about_website.html')
@login_required(login_url='login_view')
def dashboard_view(request):
    # Your view logic goes here
    return render(request, 'dashboard.html')

def login_view(request):
    if request.method== 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('dashboard.html')#Here write the link for dashboard page 
        else:
            messages.info(request,'Username or password is incorrrect')
    
    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('index_html')

def register_view(request):
        form = CreateuserForm()
        if request.method =='POST':
            form = CreateuserForm(request.POST)
            if form.is_valid():
                form.save()
                user=form.cleaned_data.get('username')
                messages.success(request, "Account was created for "+ user)
                return redirect('login_view')
            
                
             
    
        
        context ={'form':form}
        return render(request, 'registration.html', context)
def bus_route_view(request):
    routes = BusRoute.objects.all()
    return render(request, 'timetable.html', {'routes': routes})

def timetable_view(request):
    schedules = BusSchedule.objects.all()
    return render(request, 'timetable.html', {'schedules': schedules})
# for restricting user dashboard page 
# @login_required(login_url='login_view')
# def dashboard(request):
#     return redirect()
# Create your views here.
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('Address')  # Correct the capitalization
        message = request.POST.get('message')
        contact = Contacts(name=name, email=email, address=address, message=message)  # Include all fields
        contact.save()
        messages.success(request, "Your Form Is Submitted")
    return render(request, 'index.html')

from django.shortcuts import render, redirect
from django.views import View
from .models import Bus
from .forms import BookingForm
import datetime
from django.utils import timezone
import random
import string
# bus = Bus(name="Sample Bus", departure_time=timezone.now(), total_seats=50, available_seats=50)
# bus.save()

@method_decorator(login_required, name='dispatch')
class BusListView(View):
    def get(self, request):
        # Get a list of available buses with available seats
        # available_buses = Bus.objects.filter(available_seats__gt=0, departure_time__gt=datetime.datetime.now())
        available_buses = Bus.objects.filter(available_seats__gt=0, departure_time__gt=timezone.now())
        return render(request, 'bus_list.html', {'buses': available_buses})

from django.shortcuts import render, redirect
from django.views import View
from .models import Bus, Booking
from .forms import BookingForm
from django.utils import timezone
import datetime

import random
import string

from django.views import View
from django.shortcuts import render, redirect
from .models import Bus
from .forms import BookingForm
from django.utils import timezone
import random
from django.views import View
from django.shortcuts import render

class BookingSuccessView(View):
    def get(self, request):
        return render(request, 'booking_success.html')

# views.py
from django.shortcuts import render
from django.views import View
from .models import Booking


class BookTicketView(View):
    def get(self, request, bus_id):
        # Handle GET requests here, e.g., display the booking form
        bus = Bus.objects.get(pk=bus_id)
        form = BookingForm()
        return render(request, 'book_ticket.html', {'bus': bus, 'form': form})

    def post(self, request, bus_id):
        import pdb
        bus = Bus.objects.get(pk=bus_id)
        print(type(bus))
        form = BookingForm(request.POST)
        # print(form.errors)

        if form.is_valid():
            # Allow booking only one ticket
            num_tickets = 1  # A person can book only one ticket

            # Check if there are enough available seats
            if num_tickets <= bus.available_seats:
                # Generate a random seat number and calculate total price
                available_seats = list(range(1, bus.total_seats + 1))
                seat_number = random.choice(available_seats)
                total_price = bus.ticket_price  # Use the individual ticket price

                # Create a booking and deduct an available seat
                booking = form.save(commit=False)
                booking.bus = bus
                # booking.bus = bus_id
                booking.user = request.user
                booking.booking_time = timezone.now()
                booking.seat_number = seat_number
                booking.ticket_number = booking.generate_ticket_number()
                booking.ticket_price = total_price
                booking.save()

                # pdb.set_trace()

                bus.available_seats -= num_tickets
                bus.save()


                return redirect('booking_success')  # Redirect to bus list or a booking success page
            else:
                form.add_error(None, "Not enough available seats.")

        return render(request, 'booking_success.html', {'bus': bus, 'form': form})


class YourBookingView(View):
    def get(self, request):
        # Retrieve the user's bookings
        user_bookings = Booking.objects.filter(user=request.user)

        # Calculate the status for each booking
        for booking in user_bookings:
            if booking.bus.departure_time <= timezone.now():
                booking.status = "Bus Departed"
            else:
                booking.status = "Valid Booking"

        # Render the 'your_booking.html' template with user's bookings and status
        return render(request, 'your_booking.html', {'user_bookings': user_bookings})
    
@login_required(login_url='login_view')
def edit_profile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        # Update the user's name
        request.user.username = name
        request.user.save()

        # Update the user's password if provided
        if password:
            request.user.set_password(password)
            request.user.save()
            messages.success(request, 'Your profile and password have been updated successfully.')
        else:
            messages.success(request, 'Your profile has been updated successfully.')

        return redirect('edit_profile')

    return render(request, 'edit.html')

class TicketDetails(View):
    def get(self, request, booking_id):
        try:
            booking = Booking.objects.get(pk=booking_id)
            return render(request, 'ticket_details.html', {'booking': booking})
        except Booking.DoesNotExist:
            # Handle the case where the booking doesn't exist
            return render(request, 'ticket_details.html', {'booking': None})
        
@csrf_exempt
def handlerequest(request):
    #paytm will send you post request
    pass