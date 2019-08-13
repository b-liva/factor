import datetime

from django.test import TestCase
from accounts.tests import test_public_funcs as funcs
from customer.models import Customer
from request.models import Requests


class RequestModelTest(TestCase):

    def setUp(self):
        self.user = funcs.sample_user()
        # self.customer = funcs.sample_customer(owner=self.user)
        # self.customer = Customer.objects.create(
        #     owner=self.user,
        #     name='name',
        #     date2=datetime.datetime.now(),
        #     type=funcs.sample_customer_type()
        # )
        self.customer = funcs.sample_customer(owner=self.user)

    def test_customer_model_str(self):
        req = Requests.objects.create(
            owner=self.user,
            number=12456,
            customer=self.customer,
        )

        self.assertEqual(str(req), str(req.number))
