from django.urls import path, include
from .  import views

urlpatterns = [
    path('', views.menu),
    path('menu/', views.menu, name="menu"),
    path('addclient/', views.addClient, name="addclient"),
    path('clients/', views.clients, name="clients"),
    path('rooms/', views.rooms, name="rooms"),
    path('logout/', views.logout_view, name='logout'),
]
