from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Status(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=140)
    posted_at = models.DateTimeField()

    def favorite_count(self):
        return self.favorite_set.count()

    def __str__(self):
        return "{}: {}".format(self.user, self.text)


class Favorite(models.Model):
    user = models.ForeignKey(User)
    status = models.ForeignKey(Status)

    def __str__(self):
        return "{} -> {}".format(self.user, self.status)
