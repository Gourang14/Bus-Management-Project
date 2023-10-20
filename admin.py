from django.contrib import admin
from .models import BusRoute, BusSchedule,Contacts,Bus,Booking


admin.site.register(BusRoute)
admin.site.register(BusSchedule)
admin.site.register(Contacts)
admin.site.register(Bus)
admin.site.register(Booking)

# Register your models here.
