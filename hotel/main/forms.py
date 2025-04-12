from .models import Client
from django.forms import ModelForm, TextInput

class ClientForm(ModelForm):
    class Meta: 
        model = Client
        fields = ['name', 'surname', 'second_name', 'phone_number']

    widgets = {
        "surname": TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Прізвище'
        }),
        "name": TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Імя'
        }),
        "second_name": TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'По Батькові'
        }),
        "phone_number": TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+380995124378'
        }),
    }