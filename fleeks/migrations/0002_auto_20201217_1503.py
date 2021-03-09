# Generated by Django 3.1 on 2020-12-17 05:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_profile_following'),
        ('fleeks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FleeksLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('fleek', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleeks.fleek')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile')),
            ],
        ),
        migrations.AddField(
            model_name='fleek',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='fleek_user', through='fleeks.FleeksLike', to='accounts.Profile'),
        ),
    ]