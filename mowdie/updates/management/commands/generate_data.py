from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from updates.models import Update, Favorite


class Command(BaseCommand):
    def handle(self, *args, **options):
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
                        email=fake.email())
            user.set_password("password")
            user.save()
            users.append(user)

        user = User(username="admin",
                    email="admin@example.org",
                    is_staff=True,
                    is_superuser=True)
        user.set_password("password")
        user.save()

        updates = []
        for _ in range(100):
            update = Update(text=update_text(),
                            posted_at=fake.date_time_this_year(),
                            user=random.choice(users))
            update.save()
            updates.append(update)

        combos = random.sample([(user, update)
                                for user in users
                                for update in updates], 200)
        for user, update in combos:
            favorite = Favorite(user=user, update=update)
            favorite.save()
