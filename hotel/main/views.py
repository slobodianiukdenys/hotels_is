from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Client
from .forms import ClientForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
def menu(request):
    return render(request, 'menu.html')

@login_required
def addClient(request):
    error = ''
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu')
        else:
            error = 'Форма неправильна'

    form = ClientForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'addClient.html', data)

@login_required
def clients(request):
    clients = Client.objects.all()
    return render(request, 'clients.html', {'clients': clients})

@login_required
def rooms(request):
    return render(request, 'rooms.html')

def logout_view(request):
    logout(request)
    return redirect('menu')

