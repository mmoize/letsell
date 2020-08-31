# Generated by Django 3.1 on 2020-08-26 15:05

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discover', '0016_auto_20200814_1138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='post',
            name='longitude',
        ),
        migrations.AddField(
            model_name='post',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, geography=True, null=True, srid=4326, verbose_name='Location'),
        ),
    ]