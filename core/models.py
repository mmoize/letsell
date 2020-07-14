from django.db import models
from django_extensions.db.fields import RandomCharField

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class meta:
        abstract = True

        ordering = ['-created_at', '-updated_at']

# randomize the url fields for endpoints such as posts, profiles and messaging
class RandomSlugModel(models.Model):
    slug = RandomCharField(length=8, lowercase=True, unique=True)

    class Meta:
        abstract = True