from django.db.models.signals import post_save
from django.dispatch import receiver
import os

from django.db import models
from core.models import TimestampedModel
# Create your models here.
from authentication.models import User

def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.user), filename)




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    bio = models.TextField(max_length=255, blank=True)
    image = models.ImageField(upload_to= get_image_path, default="default.png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)




    def __str__(self):
        return self.user.username
        
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()
post_save.connect(create_user_profile, sender=User, dispatch_uid="users-profilecreation-signal")




