from django.test import TestCase
from django.shortcuts import reverse
from rest_framework import status
from rest_framework.test import APIClient

from request.models import Requests, ReqSpec
from accounts.tests import test_public_funcs as funcs

REQSPEC_URL = reverse('apivs:reqspec-list')


class PublicReqSepcTests(TestCase):

    def setUp(self):
        self.user = funcs.sample_user(username='user')
        self.superuser = funcs.sample_superuser(username='superuser')
        self.ex_use = funcs.login_as_expert(username='expert')
        self.customer = funcs.sample_customer(owner=self.user, name='testcasecustomer')
        self.req = funcs.sample_request(number=981010, customer=self.customer, owner=self.user)

        self.specs_payload = [
            {'qty': 132, 'kw': 132, 'rpm': 1500, 'voltage': 380},
            {'qty': 315, 'kw': 160, 'rpm': 1500, 'voltage': 380},
            {'qty': 132, 'kw': 315, 'rpm': 3000, 'voltage': 380},
            {'qty': 75, 'kw': 75, 'rpm': 1000, 'voltage': 380},
        ]

    def test_login_reqired(self):
        """،Test login required for reqspecs operations."""
        # reqspec-list
        self.client = APIClient()
        res = self.client.get(REQSPEC_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        # reqspec-detail
        funcs.sample_reqspec(req=self.req, owner=self.user, **self.specs_payload[0])
        res = self.client.get(reverse('apivs:reqspec-detail', args=[1]))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateReqSepcTests(TestCase):

    def setUp(self):
        self.user = funcs.sample_user(username='user')
        self.superuser = funcs.sample_superuser(username='superuser')
        self.ex_user = funcs.login_as_expert(username='expert')
        self.customer = funcs.sample_customer(owner=self.user, name='testcasecustomer')
        self.req = funcs.sample_request(number=981010, customer=self.customer, owner=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.specs_payload = [
            {'qty': 2, 'kw': 132, 'rpm': 1500, 'voltage': 380},
            {'qty': 1, 'kw': 160, 'rpm': 1500, 'voltage': 380},
            {'qty': 3, 'kw': 315, 'rpm': 3000, 'voltage': 380},
            {'qty': 5, 'kw': 75, 'rpm': 1000, 'voltage': 380},
        ]

    def test_retrieve_reqspec_list_for_request_api(self):
        """Test retrieve specs of a request, needs to be filtered by request"""
        req = funcs.sample_request(number=981011, customer=self.customer, owner=self.ex_user)
        spec1 = funcs.sample_reqspec(req, owner=self.ex_user, **self.specs_payload[0])
        spec2 = funcs.sample_reqspec(req, owner=self.ex_user, **self.specs_payload[1])

        self.client.force_authenticate(user=self.ex_user)
        res = self.client.get(reverse('apivs:requests-reqspecs', args=[req.number]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0]['kw'], spec1.kw)

    def test_retrieve_reqsepc_list_for_request_limited_api(self):
        """Test retrieving spec list limited by request ownership and permissions."""

        req = funcs.sample_request(number=981012, customer=self.customer, owner=self.user)

        funcs.sample_reqspec(req, owner=self.ex_user, **self.specs_payload[0])
        funcs.sample_reqspec(req, owner=self.ex_user, **self.specs_payload[3])
        self.client.force_authenticate(user=self.ex_user)

        res = self.client.get(reverse('apivs:requests-reqspecs', args=[req.number]))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_reqspec_api(self):
        """Test retrieving spec is limited to request ownership"""

        req = funcs.sample_request(number=981012, customer=self.customer, owner=self.ex_user)

        spec1 = funcs.sample_reqspec(req, owner=self.ex_user, **self.specs_payload[0])
        spec2 = funcs.sample_reqspec(req, owner=self.ex_user, **self.specs_payload[3])
        self.client.force_authenticate(user=self.ex_user)

        res = self.client.get(reverse('apivs:reqspec-detail', args=[spec1.pk]))
        print('******DATA*********', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['kw'], spec1.kw)
