import datetime

from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from customer.models import Customer
from api.serializers import customerSerializers
from accounts.tests.test_public_funcs import CustomAPITestCase

CUSTOMERS_URL = reverse('apivs:customer-list')


class PublicCustomersApiTests(CustomAPITestCase):
    """Test available customer"""

    def setUp(self):
        super().setUp()

    def test_login_required(self):
        """Test that login required for listing customer"""
        res = self.client.get(CUSTOMERS_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateCustomerApiTests(CustomAPITestCase):
    """Test the authorized user customer api"""

    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.user)

    def test_create_customer_successful_api(self):
        """Test create customer from api successfully"""
        self.client.force_authenticate(user=self.ex_user)
        payload = {
            'name': 'sazesh',
            'type': self.customer_type.pk,
        }
        res = self.client.post(CUSTOMERS_URL, payload)
        exists = Customer.objects.filter(
            owner=self.ex_user,
            type=payload['type'],
            name=payload['name'],
        ).exists()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)
        self.assertEqual(res.data['name'], payload['name'])

    def test_create_customer_api_invalid(self):
        """Test creating a new customer with invalid payload"""
        self.client.force_authenticate(user=self.ex_user)

        payload = {
            'name': '',
            'date2': datetime.datetime.now(),
            'type': self.customer_type,
        }
        res = self.client.post(CUSTOMERS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_customers(self):
        """Test retrieving customer api"""

        self.sample_customer(name='lkasjdf')
        self.sample_customer(name='oijg')
        res = self.client.get(CUSTOMERS_URL)
        customers = Customer.objects.all().order_by('name')
        serializer = customerSerializers.CustomerSerializer(customers, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_customers_not_limited_to_user(self):
        """Test users can see all customers."""
        self.client.force_authenticate(user=self.ex_user)
        user2 = self.sample_user(username='unauth', password='unauthpass123')
        customer = self.sample_customer(owner=self.user, name='customer01')
        self.sample_customer(owner=self.ex_user, name='customer02')
        self.sample_customer(owner=user2, name='customer03')
        res = self.client.get(CUSTOMERS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 4)
        self.assertEqual(res.data[0]['name'], customer.name)

