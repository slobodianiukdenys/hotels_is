from django.db import models

# Create your models here.
class Client(models.Model):
    name = models.CharField('Імя', max_length=20)
    surname = models.CharField('Прізвище', max_length=20)
    second_name = models.CharField('По Батькові', max_length=20)
    phone_number = models.CharField('Номер телефону', max_length=13, unique=True)

    def __str__(self):
        return f"{self.surname} {self.name}"

class Room(models.Model):
    room_id = models.CharField('Номер кімнати', max_length=10, unique=True)
    room_class = models.CharField('Клас кімнати', max_length=50, choices=[
        ('standart', 'Стандарт'),
        ('premium', 'Преміум'),
    ])
    capacity = models.IntegerField('Місткість кімнати')
    cost = models.IntegerField('Ціна')
    status = models.CharField('Статус кімнати', max_length=20, default='доступна', choices=[
        ('available', 'Доступна'),
        ('unavailable', 'Зайнята'),
    ])
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Клієнт')

    def __str__(self):
        return self.room_id

class Booking(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE, verbose_name='Клієнт')
    room = models.ForeignKey('Room', on_delete=models.CASCADE, verbose_name='Номер кімнати')
    check_in_date = models.DateField('Дата заселення')
    check_out_date = models.DateField('Дата виселення')
    additional_services = models.ManyToManyField('Service', blank=True, verbose_name='Додаткові послуги')
    total_price = models.DecimalField('Загальна ціна', max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата бронювання')

    def __str__(self):
        return f"Бронювання №{self.id} - Клієнт: {self.client}, Кімната: {self.room}"

class Service(models.Model):
    name = models.CharField('Назва послуги', max_length=100, unique=True)
    price = models.DecimalField('Ціна', max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


