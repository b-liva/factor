from django.shortcuts import reverse
from rest_framework.test import APIClient
from rest_framework import status
from accounts.tests.test_public_funcs import CustomAPITestCase
from cost.models import WageCost
from cost.tests.test_cost_models import CreateCost
from cost.tests.factory import factories


COST_LIST_URL = reverse('cost:create_wage')


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

    def test_filter_costs_by_qty(self):
        """Test that filter backend based on wage"""
        qty_gte = 6000

        wages = factories.WageCostFactory.create_batch(10, owner=self.ex_user)
        payload = {
            'qty__gte': qty_gte
        }
        res = self.client_exp.get(COST_LIST_URL, payload)
        wages_qs = WageCost.objects.filter(owner=self.ex_user, qty__gte=qty_gte)
        qts = [i.qty for i in wages_qs]
        # print(qts)
        wage_counts = wages_qs.count()
        # print(len(res.data), wage_counts, len(wages))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), wage_counts)

    def test_filter_costs_by_price(self):
        """Test filter queryset based on wage price"""
        price_lte = 6000

        wages = factories.WageCostFactory.create_batch(10, owner=self.ex_user)
        payload = {
            'price__lte': price_lte
        }

        res = self.client_exp.get(COST_LIST_URL, payload)
        wages_qs = WageCost.objects.filter(owner=self.ex_user, price__lte=price_lte)
        wage_counts = wages_qs.count()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), wage_counts)
