# Generated by Django 3.1 on 2020-08-12 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('discover', '0014_auto_20200812_2123'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True,  null=True, on_delete=django.db.models.deletion.CASCADE, to='discover.category'),
        ),
    ]