from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField()
    position = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')]
    )
    email = models.EmailField(unique=True)
    has_photo = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)

    role = models.CharField(
        max_length=50,
        choices=[
            ('main_guard', 'Глава охраны'),
            ('guard', 'Охранник'),
            ('admin', 'Админ'),
            ('security_director', 'Руководитель по безопасности')
        ]
    )
    
    USERNAME_FIELD = 'username'
    
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
