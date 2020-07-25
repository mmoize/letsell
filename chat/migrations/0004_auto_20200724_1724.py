# Generated by Django 3.0.8 on 2020-07-24 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('discover', '0008_auto_20200720_0917'),
        ('chat', '0003_auto_20200724_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='referenced_post',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='discover.Post'),
        ),
    ]
