from .models import Client, Booking, Service, Room
from django import forms
from django.forms import ModelForm, TextInput
from django.core.exceptions import ValidationError

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'surname', 'second_name', 'phone_number']
        widgets = {
            "surname": TextInput(attrs={'class': 'form-control', 'placeholder': 'Прізвище'}),
            "name": TextInput(attrs={'class': 'form-control', 'placeholder': 'Імя'}),
            "second_name": TextInput(attrs={'class': 'form-control', 'placeholder': 'По Батькові'}),
            "phone_number": TextInput(attrs={'class': 'form-control', 'placeholder': '+380995124378'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['client', 'room', 'check_in_date', 'check_out_date', 'additional_services']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room'].queryset = Room.objects.filter(status='available') 
        
    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')
        room = cleaned_data.get('room')

        if check_in_date and check_out_date and room:
            overlapping_bookings = Booking.objects.filter(
                room=room,
                check_in_date__lt=check_out_date,
                check_out_date__gt=check_in_date,
            ).exclude(pk=self.instance.pk if self.instance else None)

            if overlapping_bookings.exists():
                raise ValidationError(
                    f"Кімната '{room.room_id}' вже заброньована на обрані дати."
                )
        return cleaned_data