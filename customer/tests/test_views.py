import datetime

from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from rest_framework.test import APIClient
from django.test import Client
from rest_framework import status
from django.shortcuts import reverse
from accounts.tests import test_public_funcs as funcs
from django.conf import settings
from customer.models import Customer


class PublicCustomerViewsTests(TestCase):
    """Test the publicly available customer views"""

    def setUp(self):
        """Setup customer tests"""
        self.user = funcs.sample_user()
        self.client = Client()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(reverse('customer_index'))

        self.assertRedirects(
            res,
            expected_url=settings.LOGIN_URL + "?next=" + reverse('customer_index'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )


class PrivateCustomerViewsTests(TestCase):
    """Test the private customer views"""

    def setUp(self):
        self.client = Client()
        self.user = funcs.sample_user()
        self.customer_type = funcs.sample_customer_type()
        self.client.force_login(user=self.user)

    def login_as_expert(self):
        # client can't be more than one user.
        self.ex_user = funcs.sample_user(username='zarif')
        self.client.force_login(user=self.ex_user)
        # self.client.login(username='zarif', password='testpass123')
        self.sale_expert_group = Group.objects.create(name='sale_expert')
        self.sale_expert_group.permissions.add(
            Permission.objects.get(codename='add_customer', content_type__app_label='customer'),
            Permission.objects.get(codename='index_customer', content_type__app_label='customer'),
            Permission.objects.get(codename='read_customer', content_type__app_label='customer'),
        )
        self.ex_user.groups.add(self.sale_expert_group)
        self.ex_user.super_user = True
        self.ex_user.save()
        return True

    def test_retrieve_customer_list_view(self):
        """Test customer index page"""
        self.login_as_expert()
        Customer.objects.create(
            owner=self.ex_user,
            name='سازش',
            date2=datetime.datetime.now(),
            type=self.customer_type,
        )
        Customer.objects.create(
            owner=self.ex_user,
            name='second',
            date2=datetime.datetime.now(),
            type=self.customer_type,
        )

        Customer.objects.create(
            owner=self.ex_user,
            name='secondone',
            date2=datetime.datetime.now(),
            type=self.customer_type,
            agent=True
        )
        Customer.objects.create(
            owner=self.user,
            name='secondone',
            date2=datetime.datetime.now(),
            type=self.customer_type,
        )

        res = self.client.get(reverse('customer_index'))

        self.assertTrue(self.ex_user.is_authenticated)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.context['customers']), 3)
        self.assertEqual(res.context['title'], 'مشتریان')

    def test_retrieve_customer_repr_list_view(self):

        self.login_as_expert()
        Customer.objects.create(
            owner=self.ex_user,
            name='سازش',
            date2=datetime.datetime.now(),
            type=self.customer_type,
        )
        Customer.objects.create(
            owner=self.ex_user,
            name='second',
            date2=datetime.datetime.now(),
            type=self.customer_type,
        )

        Customer.objects.create(
            owner=self.ex_user,
            name='secondone',
            date2=datetime.datetime.now(),
            type=self.customer_type,
            agent=True
        )
        Customer.objects.create(
            owner=self.user,
            name='secondone',
            date2=datetime.datetime.now(),
            type=self.customer_type,
        )

        res = self.client.get(reverse('repr_index'))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.context['customers']), 1)
        self.assertEqual(res.context['title'], 'نمایندگان')

    def test_retrieve_customer_details_view(self):
        self.login_as_expert()
        Customer.objects.create(
            owner=self.ex_user,
            name='سازش',
            date2=datetime.datetime.now(),
            type=self.customer_type,
        )
        Customer.objects.create(
            owner=self.ex_user,
            name='second',
            date2=datetime.datetime.now(),
            type=self.customer_type,
        )

        Customer.objects.create(
            owner=self.ex_user,
            name='secondone',
            date2=datetime.datetime.now(),
            type=self.customer_type,
            agent=True
        )
        Customer.objects.create(
            owner=self.user,
            name='secondone',
            date2=datetime.datetime.now(),
            type=self.customer_type,
        )
        # todo: should implement all_requests for this view (all_requests in context)
        own = self.client.get(reverse('customer_read', args=[1]))
        response = self.client.get(reverse('customer_read', args=[4]))
        no_customer = self.client.get(reverse('customer_read', args=[10]))
        self.assertEqual(own.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(no_customer.status_code, status.HTTP_302_FOUND)
        self.assertEqual(no_customer.url, '/errorpage/')
