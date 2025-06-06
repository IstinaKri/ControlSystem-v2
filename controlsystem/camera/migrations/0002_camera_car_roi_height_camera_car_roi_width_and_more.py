# Generated by Django 5.2.1 on 2025-05-30 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camera', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='camera',
            name='car_roi_height',
            field=models.IntegerField(default=0, verbose_name='Высота области машины'),
        ),
        migrations.AddField(
            model_name='camera',
            name='car_roi_width',
            field=models.IntegerField(default=0, verbose_name='Ширина области машины'),
        ),
        migrations.AddField(
            model_name='camera',
            name='car_roi_x',
            field=models.IntegerField(default=0, verbose_name='X-координата области машины'),
        ),
        migrations.AddField(
            model_name='camera',
            name='car_roi_y',
            field=models.IntegerField(default=0, verbose_name='Y-координата области машины'),
        ),
        migrations.AddField(
            model_name='camera',
            name='plate_roi_height',
            field=models.IntegerField(default=0, verbose_name='Высота области номера'),
        ),
        migrations.AddField(
            model_name='camera',
            name='plate_roi_width',
            field=models.IntegerField(default=0, verbose_name='Ширина области номера'),
        ),
        migrations.AddField(
            model_name='camera',
            name='plate_roi_x',
            field=models.IntegerField(default=0, verbose_name='X-координата области номера'),
        ),
        migrations.AddField(
            model_name='camera',
            name='plate_roi_y',
            field=models.IntegerField(default=0, verbose_name='Y-координата области номера'),
        ),
    ]
