# Generated by Django 3.1 on 2021-03-24 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleeksvideo', '0006_auto_20210321_0137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fleek',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
