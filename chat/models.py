from django.db import models
from django_extensions.db.models import TimeStampedModel
from authentication.models import User
from discover.models import Post


class  Member(TimeStampedModel):
    user = models.ForeignKey(User, verbose_name="users", blank=False, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.user.username
 




