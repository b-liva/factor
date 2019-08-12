from django.test import TestCase
from customer.func import addNum
from accounts.tests import test_public_funcs as funcs
from customer.models import Customer
import datetime


class PublicCustomerModelTest(TestCase):

    def test_add_number(self):
        self.assertEqual(addNum(8, 3), 11)

    def test_customer_str(self):
        """Test the customer string representation"""
        customer = Customer.objects.create(
            owner=funcs.sample_user(),
            name='سازش',
            date2=datetime.datetime.now(),
            type=funcs.sample_customer_type(),
        )

        self.assertEqual(str(customer), customer.name)
