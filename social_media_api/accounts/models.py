from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Profile(AbstractUser):
    bio = models.CharField(max_length=200, blank=True, null=True)
    profile_picture = models.CharField(max_length=40, blank=True, null=True)
#    profile_picture = models.ImageField(upload_to='accounts/profile_pictures', blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

    def __str__(self):
        return self.username

