from django.db import models

# Create your models here.
class PlateRecognitionLog(models.Model):
    """Модель для логирования всех распознаваний номеров"""
    STATUS_CHOICES = [
        ('recognized', 'Распознан'),
        ('not_recognized', 'Не распознан'),
        ('found_in_db', 'Найден в базе'),
        ('not_found_in_db', 'Не найден в базе'),
        ('error', 'Ошибка распознавания'),
    ]
    
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время распознавания")
    license_plate = models.CharField(max_length=20, blank=True, null=True, verbose_name="Распознанный номер")
    original_text = models.CharField(max_length=50, blank=True, null=True, verbose_name="Исходный текст распознавания")
    corrected_text = models.CharField(max_length=50, blank=True, null=True, verbose_name="Исправленный текст")
    confidence = models.FloatField(default=0.0, verbose_name="Уверенность распознавания")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Статус распознавания")
    
    # Связи с другими моделями
    camera = models.ForeignKey(Camera, on_delete=models.SET_NULL, null=True, blank=True, related_name='recognitions', verbose_name="Камера")
    parking = models.ForeignKey(Parking, on_delete=models.SET_NULL, null=True, blank=True, related_name='recognitions', verbose_name="Парковка")
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True, related_name='recognitions', verbose_name="Найденный автомобиль")
    visitor = models.ForeignKey(Visitor, on_delete=models.SET_NULL, null=True, blank=True, related_name='recognitions', verbose_name="Посетитель")
    
    # Изображения
    plate_image = models.ImageField(upload_to='recognition_logs/plates/', blank=True, null=True, verbose_name="Изображение номера")
    full_frame = models.ImageField(upload_to='recognition_logs/frames/', blank=True, null=True, verbose_name="Полный кадр")
    
    def __str__(self):
        return f"Распознавание {self.license_plate or 'Не распознан'} ({self.timestamp.strftime('%d.%m.%Y %H:%M:%S')})"
    
    class Meta:
        verbose_name = "Лог распознавания"
        verbose_name_plural = "Логи распознавания"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['license_plate']),
            models.Index(fields=['status']),
        ]
    
    @staticmethod
    def log_recognition(license_plate=None, original_text=None, corrected_text=None, confidence=0.0, 
                        status='recognized', camera=None, parking=None, processing_time=0.0, 
                        plate_image=None, full_frame=None, ip_address=None, additional_info=None):
        """
        Статический метод для записи информации о распознавании номера в лог
        
        Args:
            license_plate (str): Распознанный номер (после коррекции и валидации)
            original_text (str): Исходный текст распознавания (до коррекции)
            corrected_text (str): Скорректированный текст (если применялась коррекция)
            confidence (float): Уверенность распознавания (0-100%)
            status (str): Статус распознавания (из STATUS_CHOICES)
            camera (Camera): Объект камеры, с которой произведено распознавание
            parking (Parking): Объект парковки, где произведено распознавание
            processing_time (float): Время обработки в миллисекундах
            plate_image (Image): Изображение номера
            full_frame (Image): Полный кадр
            ip_address (str): IP-адрес источника
            additional_info (dict): Дополнительная информация в формате JSON
        
        Returns:
            PlateRecognitionLog: Созданный объект лога
        """
        # Поиск автомобиля в базе по номеру, если он был распознан
        car = None
        visitor = None
        
        if license_plate:
            try:
                # Пытаемся найти машину по номеру
                cars = Car.objects.filter(license_plate=license_plate)
                if cars.exists():
                    car = cars.first()
                    # Если нашли машину, пытаемся найти связанного посетителя
                    visitors = car.visitors.all()
                    if visitors.exists():
                        visitor = visitors.first()
                        # Обновляем статус на "найден в базе"
                        status = 'found_in_db'
                    else:
                        # Машина найдена, но посетитель не найден
                        status = 'found_in_db'
                else:
                    # Машина не найдена в базе
                    if status == 'recognized':
                        status = 'not_found_in_db'
            except Exception as e:
                # В случае ошибки при поиске
                if additional_info is None:
                    additional_info = {}
                additional_info['search_error'] = str(e)
        
        # Создаем запись в логе
        log_entry = PlateRecognitionLog.objects.create(
            license_plate=license_plate,
            original_text=original_text,
            corrected_text=corrected_text,
            confidence=confidence,
            status=status,
            camera=camera,
            parking=parking,
            car=car,
            visitor=visitor,
            plate_image=plate_image,
            full_frame=full_frame,
        )
        
        return log_entry