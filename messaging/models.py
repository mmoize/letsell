from django.db import models
from django_extensions.db.models import TimeStampedModel
from authentication.models import User
from discover.models import Post

# Create your models here.
class Message(TimeStampedModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, default=1, on_delete=models.CASCADE, related_name='recipient')
    subject = models.CharField(max_length=128)
    referenced_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=5000)

    