from django.test import TestCase
from customer.func import addNum
from accounts.tests.test_public_funcs import CustomAPITestCase
from customer.models import Customer
import datetime


class PublicCustomerModelTest(CustomAPITestCase):

    def test_add_number(self):
        self.assertEqual(addNum(8, 3), 11)

    def test_customer_str(self):
        """Test the customer string representation"""
        customer = Customer.objects.create(
            owner=self.sample_user(),
            name='سازش',
            date2=datetime.datetime.now(),
            type=self.sample_customer_type(),
        )

        self.assertEqual(str(customer), customer.name)
