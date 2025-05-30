from django.db import models
from users.models import CustomUser
from django.contrib.auth.hashers import make_password

class Parking(models.Model):
    name = models.CharField(max_length=100)  # Название парковки
    address = models.CharField(max_length=200)  # Адрес парковки
    max_cars = models.IntegerField()  # Максимальное количество машин
    current_cars = models.IntegerField(default=0)  # Текущее количество машин

    def __str__(self):
        return self.name

class Barrier(models.Model):
    name = models.CharField(max_length=100)  # Название барьера
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE, related_name='barriers')  # Связь с парковкой
    login = models.CharField(max_length=100, blank=True, null=True)  # Логин для доступа к шлагбауму
    password = models.CharField(max_length=128, blank=True, null=True)  # Пароль для доступа к шлагбауму
    ip_address = models.GenericIPAddressField(blank=True, null=True)  # IP-адрес шлагбаума

    def save(self, *args, **kwargs):
        # Шифрование пароля перед сохранением, если пароль был изменен
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ParkingAccess(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='parking_accesses')  # Связь с пользователем
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE)  # Связь с парковкой

    class Meta:
        unique_together = ('user', 'parking')  # Уникальное сочетание user и parking

    def __str__(self):
        return f"Доступ для {self.user.username} на парковку {self.parking.name}"
