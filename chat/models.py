from django.db import models
from django_extensions.db.models import TimeStampedModel
from authentication.models import User
from discover.models import Post


class  Room(TimeStampedModel):
    title = models.CharField(max_length=200 )
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default=00)

    def get_absolute_url(self):
 
        return reverse('room-detail', args=[str(self.id)])



    def __unicode__(self):
        return self.title
 

class Message(TimeStampedModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, default=1, on_delete=models.CASCADE, related_name='recipient')
    referenced_post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True)
    message = models.TextField(max_length=1500, default='')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, default=00)




    def __unicode__(self):
         return self.message  # [:30]
    class Meta:
        ordering = ('-created',)