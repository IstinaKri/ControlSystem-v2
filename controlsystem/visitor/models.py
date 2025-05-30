from django.db import models
from parking.models import Parking
from cars.models import Car
from django.core.validators import RegexValidator

# Create your models here.
class Visitor(models.Model):
   
    STATUS_CHOICES = [
        ('active', 'Активный'),
        ('blocked', 'Заблокирован'),
        ('pending', 'Ожидает проверки'),
        ('temporary', 'Временный доступ')
    ]
    
    first_name = models.CharField(max_length=100, verbose_name="Имя")  # Имя посетителя
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")  # Фамилия посетителя
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Отчество")  # Отчество
    position = models.CharField(max_length=100, verbose_name="Должность")  # Должность
    organization = models.CharField(max_length=200, blank=True, null=True, verbose_name="Организация")  # Организация
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус"
    )  # Статус посетителя
    
    # Контактная информация
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Неверный формат телефона")],
        verbose_name="Телефон"
    )  # Телефон
    email = models.EmailField(blank=True, null=True, verbose_name="Email")  # Email
    
    # Фото
    photo = models.ImageField(upload_to='visitor_photos/', blank=True, null=True, verbose_name="Фото")  # Фото посетителя
    
    # Связь с автомобилем (у посетителя может быть несколько автомобилей)
    cars = models.ManyToManyField(Car, related_name='visitors', blank=True, verbose_name="Автомобили")
    
    # Доступ к парковкам
    parking_access = models.ManyToManyField(Parking, related_name='visitors', blank=True, verbose_name="Доступ к парковкам")
    
    # Дополнительная информация
    comments = models.TextField(blank=True, null=True, verbose_name="Комментарии")  # Комментарии
    access_from = models.DateTimeField(blank=True, null=True, verbose_name="Доступ с")  # Начало доступа
    access_to = models.DateTimeField(blank=True, null=True, verbose_name="Доступ до")  # Окончание доступа
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")  # Дата создания записи
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")  # Дата последнего обновления
    
    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.position})"
    
    def get_full_name(self):
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"
    
    class Meta:
        verbose_name = "Посетитель"
        verbose_name_plural = "Посетители"
        ordering = ['-created_at']
        
        
class VisitLog(models.Model):
  
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='visits', verbose_name="Посетитель")
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True, related_name='visits', verbose_name="Автомобиль")
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE, related_name='visits', verbose_name="Парковка")
    entry_time = models.DateTimeField(auto_now_add=True, verbose_name="Время въезда")
    exit_time = models.DateTimeField(null=True, blank=True, verbose_name="Время выезда")
    entry_photo = models.ImageField(upload_to='visit_photos/entry/', blank=True, null=True, verbose_name="Фото при въезде")
    exit_photo = models.ImageField(upload_to='visit_photos/exit/', blank=True, null=True, verbose_name="Фото при выезде")
    license_plate_detected = models.CharField(max_length=20, blank=True, null=True, verbose_name="Распознанный номер")
    
    def __str__(self):
        return f"Визит {self.visitor} ({self.entry_time.strftime('%d.%m.%Y %H:%M')})"
    
    class Meta:
        verbose_name = "Журнал посещений"
        verbose_name_plural = "Журнал посещений"
        ordering = ['-entry_time']
