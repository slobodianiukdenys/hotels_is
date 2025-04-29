from django.contrib import admin
from .models import Client, Room, Booking, Service
# Register your models here.

admin.site.register(Client)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Service)