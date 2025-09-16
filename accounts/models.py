from django.db import models
from django.contrib.auth.models import AbstractUser


#User model
class MyUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
