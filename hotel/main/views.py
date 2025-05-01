from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.admin.views.decorators import staff_member_required
from .models import Client, Room, Booking, Service
from .forms import ClientForm, BookingForm

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

@login_required
def free_rooms_view(request):
    free_rooms = Room.objects.filter(status='available')
    context = {
        'free_rooms': free_rooms,
    }
    return render(request, 'free_rooms.html', context)

@login_required
def unavailable_rooms_view(request):
    today = timezone.now().date()
    unavailable_bookings = Booking.objects.filter(check_out_date__gte=today).order_by('check_in_date')
    context = {
        'unavailable_bookings': unavailable_bookings,
    }
    return render(request, 'unavailable_rooms.html', context)

@login_required
def create_booking(request):
    available_rooms = Room.objects.filter(status='available').values_list('id', 'room_id')
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.save()
            form.save_m2m()
            room = booking.room
            room.status = 'unavailable'
            room.client = booking.client
            room.save()

            if booking.check_in_date and booking.check_out_date:
                delta = booking.check_out_date - booking.check_in_date
                booking.number_of_days = delta.days
                booking.total_price = booking.room.cost * booking.number_of_days
                for service in booking.additional_services.all():
                    booking.total_price += service.price
                booking.save()
            return render(request, 'booking_success.html', {'booking': booking})
        else:
            return render(request, 'create_booking.html', {'form': form})
    else:
        form = BookingForm()

    context = {
        'form': form,
        'available_rooms_choices': available_rooms
    }
    return render(request, 'create_booking.html', context)

@login_required
def booking_success(request):
    return render(request, 'booking_success.html')

@require_GET
def get_available_rooms(request):
    check_in_date_str = request.GET.get('check_in_date')
    check_out_date_str = request.GET.get('check_out_date')

    if not check_in_date_str or not check_out_date_str:
        return JsonResponse({'error': 'Будь ласка, введіть дати заселення та виселення.'}, status=400)

    try:
        check_in_date = timezone.datetime.strptime(check_in_date_str, '%Y-%m-%d').date()
        check_out_date = timezone.datetime.strptime(check_out_date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Неправильний формат дати (YYYY-MM-DD).'}, status=400)

    all_rooms = Room.objects.all()
    available_rooms = []

    for room in all_rooms:
        overlapping_bookings = Booking.objects.filter(
            room=room,
            check_in_date__lt=check_out_date,
            check_out_date__gt=check_in_date,
        )

        if not overlapping_bookings.exists():
            available_rooms.append(room)

    rooms_data = [{'id': room.id, 'room_id': room.room_id} for room in available_rooms]
    return JsonResponse({'rooms': rooms_data})

@login_required
def mark_past_bookings_as_available(request):
    if request.method == 'POST':
        today = timezone.now().date()
        past_bookings = Booking.objects.filter(check_out_date__lt=today)

        updated_rooms_count = 0
        for booking in past_bookings:
            room = booking.room
            if room.status == 'unavailable':
                room.status = 'available'
                room.client = None
                room.save()
                updated_rooms_count += 1

        messages.success(request, f'Успішно оновлено статус {updated_rooms_count} кімнат для минулих бронювань.')
        return redirect('menu') 
    else:
        return redirect('menu')