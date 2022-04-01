import uuid
from django.db import models
from django.conf import settings

# Create your models here.

#class UserProfile(AbstractUser):
class UserProfile(models.Model):
   
   
    GENDER_CHOICES = (
        ('male', "Male"),
        ('female', 'Female'),
        ('not-specified', 'Not specified')
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    profile_image = models.ImageField(upload_to = 'profile-pictures', null=True, blank=True)
    #contact_details = models.ForeignKey('Contact_Info', on_delete=models.CASCADE, null=True, blank=True)
    website = models.URLField(null=True, blank=True, max_length=255)
    gender = models.CharField(max_length=80, choices=GENDER_CHOICES, null=True, blank=True)
    code = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    #push_token = models.TextField(default='')
    phone_no = models.CharField(blank=True, null=True, max_length=255, unique=True)
    secondary_no = models.CharField(blank=True, null=True, max_length=255, unique=True)
    permanent_address = models.CharField(blank=True, null=True, max_length=255)
    temporary_address = models.CharField(blank=True, null=True, max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " UserProfile class"
    
    
"""
class Contact_Info(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    phone_no = models.CharField(blank=True, null=True, max_length=255, unique=True)
    secondary_no = models.CharField(blank=True, null=True, max_length=255, unique=True)
    permanent_address = models.CharField(blank=True, null=True, max_length=255)
    temporary_address = models.CharField(blank=True, null=True, max_length=255)

    def __str__(self):
        return f'{self.user.user.username} - phone_no = {self.phone_no}'
    
"""

    
class Follow(models.Model):
    #user = models.OneToOneField(UserProfile)
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    followers = models.ManyToManyField(UserProfile, blank=True, related_name = 'followers')
    following = models.ManyToManyField(UserProfile, blank=True, related_name = 'following')


    def __str__(self):
        return self.user.user.username + " Follow class"