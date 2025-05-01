from django.urls import path, include
from .  import views

urlpatterns = [
    path('', views.menu),
    path('menu/', views.menu, name="menu"),
    path('addclient/', views.addClient, name="addclient"),
    path('clients/', views.clients, name="clients"),
    path('free-rooms/', views.free_rooms_view, name='free_rooms'),
    path('logout/', views.logout_view, name='logout'),
    path('unavailable-rooms/', views.unavailable_rooms_view, name='unavailable_rooms'),
    path('bookings/create/', views.create_booking, name='create_booking'),
    path('bookings/success/', views.booking_success, name='booking_success'),
    path('get-available-rooms/', views.get_available_rooms, name='get_available_rooms'),
    path('mark-past-bookings-available/', views.mark_past_bookings_as_available, name='mark_past_bookings_available'),
]
