from django.test import TestCase
from core.tests.factory import factories
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactoryTest(TestCase):
    def test_create_user(self):
        user_created = factories.create_user()
        user = User.objects.last()
        self.assertEqual(user_created, user)

    def test_create_super_user(self):
        user_created = factories.create_superuser()
        user = User.objects.last()
        self.assertEqual(user_created, user)
        self.assertTrue(user_created.is_superuser)
