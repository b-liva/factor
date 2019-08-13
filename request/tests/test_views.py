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


class PrivateCustomerViewsTest(TestCase):
    """Tests Request privately avaible"""

    def setUp(self):
        # self.user = funcs.sample_user()

        # Superuser.
        self.superuser = funcs.sample_superuser(username='superuser')

        # ordinary user: not superuser, not expert, not...
        self.user = funcs.sample_user(username='user02')
        self.client.force_login(user=self.user)
        self.customer = funcs.sample_customer(name='name123', owner=self.user)

        # Expert user.
        self.ex_user = funcs.login_as_expert()

    def test_retrieve_request_list_view(self):
        """Test private list requests: superuser sees all, experts sees themselves"""
        funcs.sample_request(owner=self.user, number=1324580, customer=self.customer)
        funcs.sample_request(owner=self.user, number=132458, customer=self.customer)

        response = self.client.get(reverse('request_index'))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        # self.ex_user = funcs.login_as_expert(username='exuser')
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

    def test_retrieve_request_view(self):
        """Test retrieve request as superuser, expert_user, ordinary authenticated user"""
        funcs.sample_request(number=1545, owner=self.ex_user, customer=funcs.sample_customer(owner=self.ex_user))
        funcs.sample_request(number=15455, owner=self.ex_user, customer=funcs.sample_customer(owner=self.ex_user))
        funcs.sample_request(number=1645, owner=self.user, customer=funcs.sample_customer(owner=self.ex_user))

        # expert user:
        self.client.force_login(user=self.ex_user)
        response = self.client.get(reverse('request_details', kwargs={'request_pk': 1}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.context['request'].number, 1545)

        response = self.client.get(reverse('request_details', args=[3]))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        # ordinary user:
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('request_details', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        response = self.client.get(reverse('request_details', args=[3]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_login(user=self.superuser)
        response = self.client.get(reverse('request_details', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse('request_details', args=[3]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
