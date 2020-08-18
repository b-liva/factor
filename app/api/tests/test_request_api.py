from django.test import TestCase
from rest_framework.test import APIClient
from request.models import Requests
from accounts.tests.test_public_funcs import CustomAPITestCase
from rest_framework import status
from django.shortcuts import reverse
from api.serializers import requestSerializers

REQUESTS_URL = reverse('apivs:requests-list')


class PublicRequestApiTests(CustomAPITestCase):
    """Test public requests api tests."""

    def test_login_required(self):

        response = self.client.get(REQUESTS_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.sample_request(owner=self.superuser, number=981550, customer=self.customer)

        response = self.client.get(reverse('apivs:requests-detail', args=[981550]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PrivateRequestApiTests(CustomAPITestCase):
    """Test login and permission required to access requests"""

    def test_retrieve_requests_list_api(self):
        """Test list requests only auth users. users see own requests. should have list_requests permission"""
        # todo: this should be refactored to multiple tests
        customer1 = self.sample_customer(name='customer1', owner=self.user)

        self.sample_request(owner=self.ex_user, number=10020, customer=customer1)
        self.sample_request(owner=self.ex_user, number=1204, customer=customer1)
        self.sample_request(owner=self.superuser, number=120, customer=customer1)

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

    def test_create_requests_need_permission_api(self):
        """Test can't create request with no permission even if logged in"""
        res = self.client.post(REQUESTS_URL, self.request_payload)
        exist = Requests.objects.filter(
            owner=self.user,
            customer=self.request_payload['customer'],
            number=self.request_payload['number'],
        ).exists()

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(exist)

    def test_create_request_successful_api(self):
        """Test create a request"""
        self.client.force_authenticate(user=self.ex_user)
        res = self.client.post(REQUESTS_URL, self.request_payload)
        exist = Requests.objects.filter(
            customer=self.request_payload['customer'],
            number=self.request_payload['number'],
        ).exists()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exist)

    def test_retrieve_request_api(self):
        """Test retrieve a requests"""
        req = self.sample_request(number=980010, owner=self.ex_user, customer=self.customer)

        self.client.force_authenticate(user=self.ex_user)
        res = self.client.get(reverse('apivs:requests-detail', args=[req.number]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['number'], req.number)

    def test_retrieve_request_not_found_api(self):
        """Test can't retrieve other users request"""
        self.client.force_authenticate(user=self.ex_user)

        res = self.client.get(reverse('apivs:requests-detail', args=[self.req.number]))
        # TODO: Check request user and owner of this request are not the same
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_request_api(self):
        """Test deletion of a request"""
        self.client.force_authenticate(user=self.ex_user)
        self.sample_request(owner=self.ex_user, customer=self.customer, number=985210)
        res = self.client.delete(reverse('apivs:requests-detail', args=[985210]))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_request_limited_api(self):
        """Test can't delete other user request"""
        self.client.force_authenticate(user=self.ex_user)
        self.sample_request(owner=self.superuser, customer=self.customer, number=981011)
        res = self.client.delete(reverse('apivs:requests-detail', args=[981011]))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_request_api(self):
        """Test update a request, logged in and has permission"""
        self.client.force_authenticate(user=self.ex_user)
        self.sample_request(number=981100, customer=self.customer, owner=self.ex_user)

        payload = {
            'customer': self.sample_customer(owner=self.user, name='mapna').pk,
            'number': 981101,
        }

        res = self.client.patch(reverse('apivs:requests-detail', args=[981100]), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['customer'], payload['customer'])
        self.assertEqual(res.data['number'], 981101)

    def test_update_request_limited_api(self):
        """Test can't update other users request. Even if logged in and has permission."""
        self.client.force_authenticate(user=self.ex_user)

        self.sample_request(owner=self.superuser, customer=self.customer, number=981000)

        payload = {
            'customer': self.sample_customer(owner=self.user, name='mapna').pk,
        }

        res = self.client.patch(reverse('apivs:requests-detail', args=[981000]), payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_request_superuser_api(self):
        """Test superuser can update other users requests."""
        self.sample_request(owner=self.ex_user, customer=self.customer, number=981090)
        self.client.force_authenticate(user=self.superuser)

        payload = {
            'customer': self.sample_customer(owner=self.user, name='mapna').pk,
        }

        res = self.client.patch(reverse('apivs:requests-detail', args=[981090]), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
