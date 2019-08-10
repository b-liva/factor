from django.test import TestCase
from customer.func import addNum


class TempTest(TestCase):

    def test_add_number(self):
        self.assertEqual(addNum(8, 3), 11)

