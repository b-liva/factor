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


    def test_create_customer_needs_permission_api(self):
        """Test create customer needs permission"""
        self.client.force_authenticate(user=self.user)
        payload = {
            'name': 'sazesh',
            'type': self.customer_type.pk,
        }
        res = self.client.get(CUSTOMERS_URL, payload)
        exist = Customer.objects.filter(
            owner=self.user,
            name='sazesh',
            type=self.customer_type.pk,
        ).exists()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(exist)

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

    def test_create_customer_invalid_data_api(self):
        """Test creating a new customer with invalid payload"""
        self.client.force_authenticate(user=self.ex_user)

        payload = {
            'name': '',
            'date2': datetime.datetime.now(),
            'type': self.customer_type,
        }
        res = self.client.post(CUSTOMERS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_customers_list_needs_permission_api(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.get(CUSTOMERS_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_customers_list_api(self):
        """Test retrieving customer api"""
        self.client.force_authenticate(user=self.ex_user)
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

    def test_update_customer_needs_permission_api(self):
        """Test updating a customer needs permission(change_customer)"""
        self.client.force_authenticate(user=self.user)
        payload = {
            'name': 'newname',
        }
        res = self.client.patch(reverse('apivs:customer-detail', args=[self.customer.pk]), payload)
        exist = Customer.objects.filter(
            name=self.customer.name,
            owner=self.customer.owner,
            pk=self.customer.pk
        ).exists()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(exist)

    def test_update_customer_not_limited_by_user_api(self):
        """Test update a customer limited by user"""
        self.client.force_authenticate(user=self.ex_user)
        payload = {
            'name': 'newname',
        }
        res = self.client.patch(reverse('apivs:customer-detail', args=[self.customer.pk]), payload)
        customer = Customer.objects.get(pk=self.customer.pk)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], customer.name)
        self.assertEqual(res.data['name'], payload['name'])

    def test_update_customer_successful_api(self):
        """Test update a customer successful"""
        self.client.force_authenticate(user=self.ex_user)
        customer = funcs.sample_customer(owner=self.ex_user, name='somecustomer')
        payload = {
            'name': 'newname',
        }
        res = self.client.patch(reverse('apivs:customer-detail', args=[customer.pk]), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data['name'], payload['name'])

    def test_delete_customer_needs_permission_api(self):
        """Test delete a customer needs permission(delete_customer)"""
        self.client.force_authenticate(user=self.user)
        res = self.client.delete(reverse('apivs:customer-detail', args=[self.customer.pk]))
        exist = Customer.objects.filter(pk=self.customer.pk).exists()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(exist)

    def test_delete_customer_not_limited_by_user_api(self):
        """Test delete a customer limited by user"""
        self.client.force_authenticate(user=self.ex_user)
        res = self.client.delete(reverse('apivs:customer-detail', args=[self.customer.pk]))
        exist = Customer.objects.filter(pk=self.customer.pk).exists()
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(exist)

    def test_delete_customer_successful(self):
        """Test delete a customer seuccessful"""
        self.client.force_authenticate(user=self.ex_user)
        customer = funcs.sample_customer(owner=self.ex_user, name='something')
        res = self.client.delete(reverse('apivs:customer-detail', args=[customer.pk]))
        exist = Customer.objects.filter(pk=customer.pk).exists()
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(exist)
