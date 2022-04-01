from distutils.command.upload import upload

from django.db import models

from users.models import UserProfile
from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL
#from users.models import UserProfile

VOTES_CHOICES = (
    ("UP", "Up_Vote"),
    ("DOWN",  "Down_Vote")
)


class TimeStampedModel(models.Model):
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        abstract = True
        
        
        
class Tags(TimeStampedModel):
    tag = models.CharField(max_length=50, null=True, blank=True)

    
    def __str__(self):
        return self.tag
    
    


class Posts(TimeStampedModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="posts", blank=True, null=True)
    caption = models.TextField(blank=True, null=True)
    hashtags = models.ManyToManyField(Tags, blank=True, related_name="hashtags")
    
    
    def __str__(self):
        return f'{self.user} > {self.image}'
    
    """
    def vote_count(self):
        return self.votes.all().count()
    
    
    def comment_count(self):
        return self.comments.all().count()
    """
    
    
    
    class Meta:
        ordering = ['-created_at']
    
    
    
    
class Comments(TimeStampedModel):
    message = models.TextField(blank=True, null=True)
    image = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return f'{self.user.user.username} > {self.message}  >{self.image.user.user.username} > {self.image.image}' 
    
    
    
class Votes(TimeStampedModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ForeignKey(Posts, on_delete=models.CASCADE)
    vote =  models.CharField(choices=VOTES_CHOICES, null=True, blank=True, max_length=10)
    
    
    def  __str__(self):
        return f'{self.user.user.username} > {self.vote}  > {self.image.user.user.username} > {self.image.image}'
