from django.db import models

# Create your models here.
class Clients(models.Model):
    name = models.CharField('Імя', max_length=20)
    surname = models.CharField('Прізвище', max_length=20)
    phone_number = models.CharField('Номер телефону', max_length=13)
    room_id = models.IntegerField('Номер кімнати')

    def __str__(self):
        return self.title