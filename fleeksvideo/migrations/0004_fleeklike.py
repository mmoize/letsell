# Generated by Django 3.1 on 2021-03-20 14:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fleeksvideo', '0003_auto_20210320_1603'),
    ]

    operations = [
        migrations.CreateModel(
            name='FleekLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('fleek', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleeksvideo.fleek')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
