from django.db import models
from parking.models import Parking
from parking.models import Barrier
from django.contrib.auth.hashers import make_password
from django.db import models
# Create your models here.

class Camera(models.Model):
    name = models.CharField(max_length=100) 
    id_parking = models.ForeignKey(Parking, on_delete=models.CASCADE, related_name='cameras') 
    stream_url = models.CharField(max_length=255)  
    password = models.CharField(max_length=128, blank=True, null=True)  
    login = models.CharField(max_length=100, blank=True, null=True) 
    camera_type = models.CharField(
        max_length=20,
        choices=[('barrier', 'На шлагбаум'), ('overview', 'Обзорная')]
    )  
    barrier = models.ForeignKey(Barrier, on_delete=models.SET_NULL, null=True, blank=True, related_name='cameras')  
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE, related_name='parking_cameras')  
    
    car_roi_x = models.IntegerField(default=0, verbose_name="X-координата области машины")
    car_roi_y = models.IntegerField(default=0, verbose_name="Y-координата области машины")
    car_roi_width = models.IntegerField(default=0, verbose_name="Ширина области машины")
    car_roi_height = models.IntegerField(default=0, verbose_name="Высота области машины")
    plate_roi_x = models.IntegerField(default=0, verbose_name="X-координата области номера")
    plate_roi_y = models.IntegerField(default=0, verbose_name="Y-координата области номера")
    plate_roi_width = models.IntegerField(default=0, verbose_name="Ширина области номера")
    plate_roi_height = models.IntegerField(default=0, verbose_name="Высота области номера")

    def save(self, *args, **kwargs):
     
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name