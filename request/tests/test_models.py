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

    def test_create_req_part(self):
        """Test create request parts model"""
        part1 = ReqPart.objects.create(
            owner=self.user,
            req=self.req,
            title='درپوش عایقی',
            qty=3
        )

        part2 = ReqPart.objects.create(
            owner=self.user,
            req=self.req,
            title='ptc',
            qty=5
        )
        parts = ReqPart.objects.all()
        self.assertEqual(parts.count(), 2)
        self.assertEqual(part1.title, 'درپوش عایقی')
        self.assertEqual(part2.qty, 5)
        self.assertEqual(str(part1), str(part1.qty) + ' عدد ' + str(part1.title))
