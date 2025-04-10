from django.db import models

# Create your models here.
class Client(models.Model):
    name = models.CharField('Імя', max_length=20)
    surname = models.CharField('Прізвище', max_length=20)
    second_name = models.CharField('По Батькові', max_length=20)
    phone_number = models.CharField('Номер телефону', max_length=13, unique=True)
    room_id = models.IntegerField('Номер кімнати', null=True, blank=True)

    def __str__(self):
        return self.name