from django.test import TestCase, Client
from django.shortcuts import reverse
from rest_framework import status
from django.conf import settings

from accounts.tests import test_public_funcs as funcs
from request.models import Requests


class PublicRequestViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = funcs.sample_user()

    def test_request_list_view(self):
        """Test Login required to see list of requests."""
        response = self.client.get(reverse('request_index'))

        self.assertRedirects(
            response,
            expected_url=settings.LOGIN_URL + '?next=' + reverse('request_index'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )


class PirvateCustomerViewsTest(TestCase):
    """Tests Request privately avaible"""

    def setUp(self):
        self.user = funcs.sample_user()
        self.superuser = funcs.sample_user(username='superuser')
        self.superuser.is_superuser = True
        self.superuser.save()
        self.client.force_login(user=self.user)
        self.user2 = funcs.sample_user(username='user02')
        self.customer = funcs.sample_customer(name='name123', owner=self.user2)

    def test_retrieve_request_list_view(self):
        """Test private list requests: superuser sees all, experts sees themselves"""
        funcs.sample_request(owner=self.user, number=1324580, customer=self.customer)
        funcs.sample_request(owner=self.user, number=132458, customer=self.customer)

        response = self.client.get(reverse('request_index'))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        self.ex_user = funcs.login_as_expert()
        self.client.force_login(user=self.ex_user)
        funcs.sample_request(owner=self.ex_user, number=13245, customer=self.customer)
        res = self.client.get(reverse('request_index'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.context['all_requests']), 1)

        self.client.force_login(user=self.superuser)
        superuser_res = self.client.get(reverse('request_index'))
        self.assertEqual(superuser_res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(superuser_res.context['all_requests']), 3)

    def test_request_report(self):
        # todo: should be implemented.

        return True
