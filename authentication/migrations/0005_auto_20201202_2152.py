# Generated by Django 3.1 on 2020-12-02 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_user_follows'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='follows',
        ),
        migrations.DeleteModel(
            name='Follow',
        ),
    ]
