# Generated by Django 3.0.8 on 2020-07-24 07:21

import discover.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_remove_room_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='referenced_post',
            field=models.CharField(blank=True, max_length=200, verbose_name=discover.models.Post),
        ),
    ]