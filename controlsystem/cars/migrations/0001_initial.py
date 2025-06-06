# Generated by Django 5.2.1 on 2025-05-30 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_plate', models.CharField(max_length=20, verbose_name='Номер')),
                ('region', models.CharField(max_length=10, verbose_name='Регион')),
                ('country', models.CharField(max_length=50, verbose_name='Страна')),
                ('brand', models.CharField(max_length=50, verbose_name='Марка')),
                ('model', models.CharField(max_length=50, verbose_name='Модель')),
                ('color', models.CharField(blank=True, max_length=30, null=True, verbose_name='Цвет')),
                ('year', models.IntegerField(blank=True, null=True, verbose_name='Год выпуска')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='car_photos/', verbose_name='Фото')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
            ],
            options={
                'verbose_name': 'Автомобиль',
                'verbose_name_plural': 'Автомобили',
                'ordering': ['-date_added'],
            },
        ),
    ]
