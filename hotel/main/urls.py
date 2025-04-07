from django.urls import path, include
from .  import views

urlpatterns = [
    path('', views.index),
    path('menu/', views.menu),
    path('addclient/', views.addClient),
    path('clients/', views.clients),
    path('rooms/', views.rooms,),
]
