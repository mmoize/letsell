# Generated by Django 3.1 on 2021-03-20 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleeksvideo', '0005_fleek_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fleek',
            name='commentsCount',
        ),
        migrations.RemoveField(
            model_name='fleek',
            name='likesCount',
        ),
    ]
