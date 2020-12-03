from rest_framework.test import APIClient
from django_filters import rest_framework as filters
from accounts.tests.test_public_funcs import CustomAPITestCase
from cost.models import WageCost
from cost.tests.test_cost_models import CreateCost


class PubicApiTest(CustomAPITestCase):

    def setUp(self):
        super().setUp()


class PrivateApiTest(CustomAPITestCase):
    def setUp(self):
        super().setUp()
        self.client_exp = APIClient()
        self.client_exp.force_authenticate(user=self.ex_user)

        cc = CreateCost()  # create cost
        self.payload = cc.create_total_cost()
        self.payload['owner'] = self.ex_user.pk

    def test_filter_costs(self):
        """Test that filter backend based on wage"""
        wages = [
            {'qty': 1, 'price': 125},
            {'qty': 18, 'price': 130},
            {'qty': 5, 'price': 230},
            {'qty': 6, 'price': 450},
            {'qty': 7, 'price': 378},
            {'qty': 9, 'price': 514},
        ]
        for wage in wages:
            wage_payload = {
                'qty': wage['qty'],
                'price': wage['price'],
                'unit': ('hr', 'hr')
            }
            WageCost.objects.create(**wage_payload)

