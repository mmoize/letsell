# Generated by Django 3.1 on 2020-08-05 14:55

import discover.models
from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('discover', '0008_auto_20200720_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=0, size=[500, 300], upload_to=discover.models.Product_image_path),
        ),
    ]
