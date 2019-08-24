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
        self.customer = funcs.sample_customer(owner=self.user, name='تام ایرانخودرو')

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
        Customer.objects.create(
            owner=self.ex_user,
            name='سازش',
            date2=datetime.datetime.now(),
            type=self.customer_type,
        )
        Customer.objects.create(
            owner=self.ex_user,
            name='پمپ یاران',
            date2=datetime.datetime.now(),
            type=self.customer_type,
        )
        Customer.objects.create(
            owner=self.user,
            name='فولاد خوزستان',
            date2=datetime.datetime.now(),
            type=self.customer_type,
        )
        Customer.objects.create(
            owner=self.user,
            name='آتیه سازان',
            date2=datetime.datetime.now(),
            type=self.customer_type,
        )
        res = self.client.get(CUSTOMERS_URL)
        customers = Customer.objects.all().order_by('name')
        serializer = customerSerializers.CustomerSerializer(customers, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 5)
        self.assertEqual(res.data[0]['name'], 'آتیه سازان')

    def test_retreive_customers_list_not_limited_to_user_api(self):
        """Test that customers are for the authenticated user"""
        self.client.force_authenticate(user=self.ex_user)
        user2 = funcs.sample_user(username='unauth', password='unauthpass123')
        user3 = funcs.sample_user(username='unauth2', password='unauthpass123')
        Customer.objects.create(
            owner=self.ex_user,
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
        Customer.objects.create(
            owner=user3,
            name='fake2',
            date2=datetime.datetime.now(),
            type=self.customer_type,
        )
        res = self.client.get(CUSTOMERS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 4)
        self.assertEqual(res.data[0]['name'], 'fake')  # Ordered by name

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
