import os
from django.db import models
from authentication.models import User
from accounts.models import Profile
from django_extensions.db.models import (ActivatorModel,TimeStampedModel)
from django_resized import ResizedImageField
from django.db.models import Q
from djgeojson.fields import PointField
from django.contrib.gis.db.models import PointField










      



class FleekQuerySet(models.QuerySet):
    def by_username(self, username):
        return self.filter(user__username__iexact=username)

    def feed(self, user):
  
        profiles_exist = user.profile.following.exists()
        following_ = User.objects.get(id=user.id)
        folllowing = following_.profile.following

        print("||| user", following_)
        print("||| user", profiles_exist)
        followed_users_id = []
        if profiles_exist:
            followed_users_id = Profile.following.values_list("user__id", flat=True) # [x.user.id for x in profiles]
        return self.filter(
            Q(user__id__in=followed_users_id) |
            Q(user=user)
        ).distinct().order_by("-created")

class FleekManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return FleekQuerySet(self.model, using=self._db)

    def feed(self, user):
        return self.get_queryset().feed(user)

class Fleeka(TimeStampedModel):
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fleeks") # many users can many tweets
    content = models.TextField(blank=True, null=True)
    location = PointField(null=True, geography=True, blank=True, srid=4326, verbose_name='Location')
    anonymity = models.BooleanField(default=False)
    public = models.BooleanField(default=True)

    objects = FleekManager()
    # def __str__(self):
    #     return self.content
    
    class Meta:
        ordering = ['-id']
    
    @property
    def is_refleek(self):
        return self.parent != None




def Fleeks_image_path(instance, filename):
    return os.path.join('FleeksImage', str(instance.user.username), filename)

class FleeksImage(TimeStampedModel):
    fleeka = models.ForeignKey(Fleeka, on_delete=models.CASCADE)
    image = ResizedImageField(size=[500, 400], upload_to= Fleeks_image_path)
    user = models.ForeignKey(User, default="1", on_delete=models.CASCADE)



    def __str__(self):
        template = '{0.user.username}'
        return template.format(self)

    class Meta:
        ordering = ['-created',]