import datetime

from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from customer.models import Customer
from api.serializers import customerSerializers
from accounts.tests import test_public_funcs as funcs

CUSTOMERS_URL = reverse('apivs:customer-list')


class PublicCustomersApiTests(TestCase):
    """Test available customer"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for listing customer"""
        res = self.client.get(CUSTOMERS_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateCustomerApiTests(TestCase):
    """Test the authorized user customer api"""

    def setUp(self):
        self.user = funcs.sample_user()
        self.superuser = funcs.sample_superuser(username='superuser')
        self.ex_user = funcs.login_as_expert(username='ex_user')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.customer_type = funcs.sample_customer_type()

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

        Customer.objects.create(
            owner=self.user,
            name='سازش',
            date2=datetime.datetime.now(),
            type=self.customer_type,
        )
        Customer.objects.create(
            owner=self.user,
            name='second',
            date2=datetime.datetime.now(),
            type=self.customer_type,
        )
        res = self.client.get(CUSTOMERS_URL)
        customers = Customer.objects.all().order_by('name')
        serializer = customerSerializers.CustomerSerializer(customers, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_customers_limited_to_user(self):
        """Test that customers are for the authenticated user"""

        user2 = funcs.sample_user(username='unauth', password='unauthpass123')
        customer = Customer.objects.create(
            owner=self.user,
            name='second',
            date2=datetime.datetime.now(),
            type=self.customer_type,
        )
        Customer.objects.create(
            owner=user2,
            name='fake',
            date2=datetime.datetime.now(),
            type=self.customer_type,
        )
        res = self.client.get(CUSTOMERS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], customer.name)

