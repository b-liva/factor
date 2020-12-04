import factory
from faker import Factory
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.tests.factory import factories
User = get_user_model()
faker = Factory()


class ModelTests(TestCase):
    def setUp(self):
        self.user = factories.UserFactory()

    def test_create_user_with_username_successful(self):
        """test creating a new user with an username successful"""
        username = "someUserName"
        password = "TestPass123"
        user = factories.UserFactory(
            username=username,
            password=password
        )

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_make_user_superuser(self):
        """Test that makes user a superuser"""
        self.user.make_user_a_superuser()
        self.assertTrue(self.user.is_superuser)

    def test_make_user_expuser(self):
        """Test that makes user a expert user"""
        res = self.user.make_user_an_expertuser()
        self.assertTrue(self.user.sales_exp)


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
