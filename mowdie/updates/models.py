from django.db import models
from django.contrib.auth.models import User


class Update(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=140)
    posted_at = models.DateTimeField()
    favorited_users = models.ManyToManyField(User, through="Favorite",
                                             related_name="favorited_updates")

    def __str__(self):
        return "{}: {}".format(self.user, self.text)


class Favorite(models.Model):
    user = models.ForeignKey(User)
    update = models.ForeignKey(Update)

    class Meta:
        unique_together = ('user', 'update',)

    def __str__(self):
        return "{} -> {}".format(self.user, self.update)


def load_fake_data():
    """Create fake users and statuses for Mowdie."""
    from faker import Faker
    import random
    from django.conf import settings
    from PyMarkovTextGenerator import Markov

    fake = Faker()
    textgen = Markov(prob=True, level=3)
    with open(settings.BASE_DIR + "/../john_carter.txt") as file:
        textgen.parse(file.read())

    def update_text():
        return textgen.generate(
            startf=lambda db: random.choice([x for x in db
                                             if x[0][0].isupper()]),
            endf=lambda s: len(s) > 120)

    Favorite.objects.all().delete()
    Update.objects.all().delete()
    User.objects.all().delete()

    users = []
    for _ in range(20):
        user = User(username=fake.user_name(),
                    email=fake.email(),
                    password="password")
        user.save()
        users.append(user)

    statuses = []
    for _ in range(100):
        status = Update(text=update_text(),
                        posted_at=fake.date_time_this_year(),
                        user=random.choice(users))
        status.save()
        statuses.append(status)

    combos = random.sample([(user, status)
                            for user in users
                            for status in statuses], 200)
    for user, status in combos:
        favorite = Favorite(user=user, status=status)
        favorite.save()
