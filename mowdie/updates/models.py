from django.core.urlresolvers import reverse, reverse_lazy
from django.db import models
from django.contrib.auth.models import User


class Update(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=140)
    posted_at = models.DateTimeField()
    favorited_users = models.ManyToManyField(User, through="Favorite",
                                             related_name="favorited_updates")

    def get_absolute_url(self):
        return reverse('show_update', kwargs={"update_id": self.id})

    def __str__(self):
        return "{}: {}".format(self.user, self.text)


class Favorite(models.Model):
    user = models.ForeignKey(User)
    update = models.ForeignKey(Update)

    class Meta:
        unique_together = ('user', 'update',)

    def __str__(self):
        return "{} -> {}".format(self.user, self.update)
