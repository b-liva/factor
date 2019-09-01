import datetime

from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from rest_framework.test import APIClient
from django.test import Client
from rest_framework import status
from django.shortcuts import reverse
from accounts.tests.test_public_funcs import CustomAPITestCase
from django.conf import settings
from customer.models import Customer


class PublicCustomerViewsTests(CustomAPITestCase):
    """Test the publicly available customer views"""

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(reverse('customer_index'))

        self.assertRedirects(
            res,
            expected_url=settings.LOGIN_URL + "?next=" + reverse('customer_index'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )


class PrivateCustomerViewsTests(CustomAPITestCase):
    """Test the private customer views"""

    def test_retrieve_customer_list_view(self):
        """Test customer index page"""
        self.client.force_login(user=self.ex_user)
        self.sample_customer(owner=self.user, name='آبیاران دیمه', agent=True)
        self.sample_customer(name='پمپیران')
        self.sample_customer(name='پویندان')
        self.sample_customer(name='پارت صنعت')

        res = self.client.get(reverse('customer_index'))
        customers = Customer.objects.all()
        self.assertTrue(self.ex_user.is_authenticated)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.context['customers']), 4)
        self.assertEqual(res.context['title'], 'مشتریان')

    def test_retrieve_customer_agent_list(self):
        """Tes retrieve customer agent list"""
        self.client.force_login(user=self.ex_user)
        self.sample_customer(owner=self.ex_user, name='qgqerg', agent=True)
        self.sample_customer(owner=self.ex_user, name='jhv')
        self.sample_customer(owner=self.ex_user, name='rx')
        self.sample_customer(owner=self.user, name=';nlk')

        res = self.client.get(reverse('repr_index'))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.context['customers']), 1)
        self.assertEqual(res.context['title'], 'نمایندگان')

    def test_retrieve_customer_details_view(self):
        """Test retrieve customer details"""
        self.client.force_login(user=self.ex_user)
        req1 = self.sample_customer(name='asdgasg', owner=self.ex_user)
        req2 = self.sample_customer(name='ikjasf')
        req3 = self.sample_customer(name='hh')
        req4 = self.sample_customer(name='eheh')
        req5 = self.sample_customer(name='rtjrj')

        # todo: should implement all_requests for this view (all_requests in context)
        own = self.client.get(reverse('customer_read', args=[req1.pk]))
        response = self.client.get(reverse('customer_read', args=[req2.pk]))
        no_customer = self.client.get(reverse('customer_read', args=[50]))
        self.assertEqual(own.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(no_customer.status_code, status.HTTP_302_FOUND)
        self.assertEqual(no_customer.url, '/errorpage/')
