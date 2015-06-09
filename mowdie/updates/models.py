from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Status(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=140)
    posted_at = models.DateTimeField()


class Favorite(models.Model):
    user = models.ForeignKey(User)
    status = models.ForeignKey(Status)