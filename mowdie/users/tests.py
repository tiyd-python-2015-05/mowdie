from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase

# Create your tests here.
from users.models import Profile, get_profile


class ProfileTest(TestCase):
    def test_get_profile_makes_profile(self):
        user = User()
        self.assertEqual(Profile, type(get_profile(user)))

    def test_get_profile_with_anon_user(self):
        user = AnonymousUser()
        self.assertEqual(None, get_profile(user))