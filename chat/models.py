from django.db import models
from django.db import models
from django_extensions.db.models import TimeStampedModel
from authentication.models import User
from discover.models import Post

# Create your models here.
class _Message(TimeStampedModel):
    _sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    _recipient = models.ForeignKey(User, default=1, on_delete=models.CASCADE, related_name='recipient')
    _referenced_post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True)
    _message = models.TextField(max_length=500)
    _is_read = models.BooleanField(default=False)
    def __str__(self):
        return self._message
    class Meta:
        ordering = ('-created',)
