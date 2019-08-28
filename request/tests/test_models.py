import datetime

from django.test import TestCase
from accounts.tests.test_public_funcs import CustomAPITestCase
from customer.models import Customer
from request.models import Requests


class RequestModelTest(CustomAPITestCase):

    def test_customer_model_str(self):
        req = Requests.objects.create(
            owner=self.user,
            number=12456,
            customer=self.customer,
        )

        self.assertEqual(str(req), str(req.number))
