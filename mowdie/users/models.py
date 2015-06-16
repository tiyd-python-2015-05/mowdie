from datetime import date

from django.core.exceptions import ValidationError

from django.db import models
from django.contrib.auth.models import User, AnonymousUser


# Create your models here.

def get_profile(user, save=False):
    """Gets the profile for a user. Ensures profile exists."""
    if type(user) == AnonymousUser:
        return None
    else:
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            profile = Profile(user=user)
            if save: profile.save()
        finally:
            return profile


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
    followed = models.ManyToManyField("Profile", related_name="followers")

    def __str__(self):
        return str(self.user)
