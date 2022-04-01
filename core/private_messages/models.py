from django.db import models
from django.conf import settings
from posts.models import TimeStampedModel
from users.models import UserProfile
# Create your models here.

USER = settings.AUTH_USER_MODEL


class MessageBody(TimeStampedModel):
    message = models.TextField(null=True, blank=True)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="receiver")
    is_read = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f'SENDER > {self.sender} - MESSAGE - {self.message} - RECEIVER >  {self.receiver}'
    
"""    
    class Meta:
        ordering = ("-self.timestampedmodel.updated_at")
"""