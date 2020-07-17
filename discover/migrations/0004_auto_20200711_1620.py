# Generated by Django 3.0.8 on 2020-07-11 06:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('discover', '0003_auto_20200711_1251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='cold',
        ),
        migrations.AddField(
            model_name='productimage',
            name='user',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]