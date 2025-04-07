from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def menu(request):
    return render(request, 'menu.html')

def addClient(request):
    return render(request, 'addClient.html')

def clients(request):
    return render(request, 'clients.html')

def rooms(request):
    return render(request, 'rooms.html')