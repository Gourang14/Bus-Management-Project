from django.urls import path
from busapp1 import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from .views import BusListView, BookTicketView
from django.contrib.auth.views import LoginView, LogoutView
from .views import BusListView, BookTicketView, YourBookingView, edit_profile,TicketDetails


urlpatterns = [
    path('', views.index, name='index'),
    
    path('index.html', views.index, name='index_html'),
    path('registration.html', views.reg, name='reg'),
  
    path('about_website.html', views.about, name='about'),

    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_page, name='logout_page'),
    path('register/', views.register_view, name='register_view'),
    path('login/dashboard.html', views.dashboard_view, name='dashboard'),
    path('timetable/', views.timetable_view, name='timetable'),
    path('contact/', views.contact, name='contact'),
    path('bus-list/', BusListView.as_view(), name='bus_list'),
    # path('book-ticket/<int:bus_id>/', BookTicketView.as_view(), name='book_ticket'),
    path('book-ticket/<int:bus_id>/', BookTicketView.as_view(), name='book_ticket'),
    path('your-booking/', views.YourBookingView.as_view(), name='your_booking'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('booking-success/', views.BookingSuccessView.as_view(), name='booking_success'),
    path('ticket-details/<int:booking_id>/', TicketDetails.as_view(), name='ticket_details'),
    path('handlerequest/', views.handlerequest, name='handlerequest'),

    
  
    
    # Other URL patterns for busapp1
]