from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

def validate_date_in_past(value):
    if value >= date.today():
        raise ValidationError("Date must be in past.")


class Profile(models.Model):
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    user = models.OneToOneField(User)
    url = models.URLField("Personal URL (homepage/blog)", max_length=255,
                          null=True, blank=True)
    birthday = models.DateField(null=True, blank=True,
                                validators=[validate_date_in_past])

    def __str__(self):
        return str(self.user)
