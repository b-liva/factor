from django.test import TestCase
from rest_framework.test import APIClient
from request.models import Requests
from accounts.tests import test_public_funcs as funcs
from rest_framework import status
from django.shortcuts import reverse
from api.serializers import requestSerializers

REQUESTS_URL = reverse('apivs:requests-list')


class PublicRequestApiTests(TestCase):
    """Test public requests api tests."""

    def setUp(self):
        self.client = APIClient()
        self.user = funcs.sample_user()

    def test_login_required(self):

        response = self.client.get(REQUESTS_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PrivateRequestApiTests(TestCase):
    """Test login and permission required to access requests"""

    def setUp(self):
        """
        client, ordinary user, superuser, expertuser created. login with ordinary user(no permissions)
        :return:
        """
        self.client = APIClient()
        self.superuser = funcs.sample_superuser()
        self.user = funcs.sample_user()
        self.ex_user = funcs.login_as_expert()
        self.client.force_authenticate(user=self.user)

        self.request_payload = {
            'number': 1000,
            'customer': funcs.sample_customer(owner=self.user).pk,
            "date_fa": "1398-05-06",
        }

    def test_retrieve_requests_api(self):
        """Test list requests only auth users. users see own requests. should have list_requests permission"""
        customer1 = funcs.sample_customer(name='customer1', owner=self.user)

        funcs.sample_request(owner=self.ex_user, number=10020, customer=customer1)
        funcs.sample_request(owner=self.ex_user, number=1204, customer=customer1)
        funcs.sample_request(owner=self.superuser, number=120, customer=customer1)

        response = self.client.get(REQUESTS_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.ex_user)
        res = self.client.get(REQUESTS_URL)
        reqs = Requests.objects.filter(owner=self.ex_user)
        serializer = requestSerializers.RequestSerializers(reqs, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

        self.client.force_authenticate(user=self.superuser)
        res = self.client.get(REQUESTS_URL)
        reqs = Requests.objects.all()
        serializer = requestSerializers.RequestSerializers(reqs, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_requests_successful_api(self):

        res = self.client.post(REQUESTS_URL, self.request_payload)
        exist = Requests.objects.filter(
            owner=self.user,
            customer=self.request_payload['customer'],
            number=self.request_payload['number'],
        ).exists()

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(exist)

    def test_create_request_by_expert_successful_api(self):

        self.client.force_authenticate(user=self.ex_user)
        res = self.client.post(REQUESTS_URL, self.request_payload)

        exist = Requests.objects.filter(
            customer=self.request_payload['customer'],
            number=self.request_payload['number'],
        ).exists()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exist)


