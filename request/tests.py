from django.test import TestCase

# Create your tests here.

from .models import Requests


class RequestModelTests(TestCase):

    def setup(self):

        Requests.objects.create(number=1000, customer_id=20, owner_id=4)
