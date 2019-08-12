from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()


class ModelTests(TestCase):

    def test_create_user_with_username_successful(self):
        """test creating a new user with an username successful"""
        username = 'someUserName'
        password = 'TestPass123'
        user = User.objects.create_user(
            username=username,
            password=password
        )

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    # def test_create_user_with_email_successful(self):
    #     """test creating a new user with an email successful"""
    #     email = 'test_email@testmail.com'
    #     password = 'TestPass123'
    #
    #     user = get_user_model().objects.create_user(
    #         email=email,
    #         password=password
    #     )
    #
    #     self.assertEqual(user.email, email)
    #     self.assertTrue(user.check_password())
