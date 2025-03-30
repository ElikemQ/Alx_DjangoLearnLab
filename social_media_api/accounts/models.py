from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# customised user model
class CustomUser(AbstractUser):
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='followers_relation', blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='following_relation', blank=True)

    def __str__(self):
        return self.username 