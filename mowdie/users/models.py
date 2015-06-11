from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    user = models.OneToOneField(User)

    def __str__(self):
        return str(self.user)