from django.db import models

# Create your models here.
class Car(models.Model):
    """Модель для хранения информации об автомобилях"""
    license_plate = models.CharField(max_length=20, verbose_name="Номер")  # Номер автомобиля
    region = models.CharField(max_length=10, verbose_name="Регион")  # Регион регистрации
    country = models.CharField(max_length=50, verbose_name="Страна")  # Страна регистрации
    brand = models.CharField(max_length=50, verbose_name="Марка")  # Марка автомобиля
    model = models.CharField(max_length=50, verbose_name="Модель")  # Модель автомобиля
    color = models.CharField(max_length=30, verbose_name="Цвет", blank=True, null=True)  # Цвет автомобиля
    year = models.IntegerField(verbose_name="Год выпуска", blank=True, null=True)  # Год выпуска
    photo = models.ImageField(upload_to='car_photos/', blank=True, null=True, verbose_name="Фото")  # Фото автомобиля
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")  # Когда добавлена запись
    
    def __str__(self):
        return f"{self.brand} {self.model} - {self.license_plate} ({self.region})"
    
    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
        ordering = ['-date_added']