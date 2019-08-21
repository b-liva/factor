from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.shortcuts import reverse
from accounts.tests import test_public_funcs as funcs
from request.models import Payment


INCOME_URL = reverse('apivs:payment-list')


class PublicIncomeTests(APITestCase):

    def setUp(self):
        self.user = funcs.sample_user(username='user')
        self.superuser = funcs.sample_superuser(username='superuser')
        self.ex_user = funcs.login_as_expert(username='ex_user')

    def test_login_requried(self):
        """Test login requried."""
        res = self.client.get(INCOME_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateIncomeTests(APITestCase):

    def setUp(self):
        self.user = funcs.sample_user(username='user')
        self.superuser = funcs.sample_superuser(username='superuser')
        self.ex_user = funcs.login_as_expert(username='ex_user')

        self.customer = funcs.sample_customer(owner=self.user, name='customer')
        self.req = funcs.sample_request(owner=self.user, customer=self.customer, number=981010)
        self.proforma = funcs.sample_proforma(req=self.req, owner=self.user, number=982020)
        self.income = funcs.sample_income(proforma=self.proforma, owner=self.user, number=79348347)
        self.client = APIClient()

    def test_create_income_api(self):
        """Test create income"""
        self.client.force_authenticate(user=self.ex_user)
        req1 = funcs.sample_request(owner=self.ex_user, number=981020, customer=self.customer)
        prof1 = funcs.sample_proforma(req=req1, owner=self.ex_user, number=983020)
        payload = {
            'number': 9347348,
            'xpref_id': prof1.pk,
            'owner': self.ex_user.pk,
            'amount': 1340000,
        }
        res = self.client.post(INCOME_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        income = Payment.objects.get(number=payload['number'], xpref_id=payload['xpref_id'], owner=payload['owner'])
        self.assertEqual(income.number, payload['number'])
        self.assertEqual(income.xpref_id.id, payload['xpref_id'])

    def test_retreive_income_list_needs_permission_list(self):
        """Test retrieve income list needs permission(index_payment)"""
        self.client.force_authenticate(user=self.user)
        res = self.client.get(INCOME_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_income_list_api(self):
        """Test retrieve income list"""
        self.client.force_authenticate(user=self.ex_user)

        req1 = funcs.sample_request(owner=self.ex_user, number=981020, customer=self.customer)
        req2 = funcs.sample_request(owner=self.ex_user, number=981021, customer=self.customer)
        prof1 = funcs.sample_proforma(req=req1, owner=self.ex_user, number=983020)
        prof2 = funcs.sample_proforma(req=req2, owner=self.ex_user, number=983021)

        income1 = funcs.sample_income(proforma=prof1, owner=self.ex_user, number=9813030)
        income2 = funcs.sample_income(proforma=prof2, owner=self.ex_user, number=9813031)

        res = self.client.get(INCOME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0]['number'], income1.number)
        self.assertEqual(res.data[0]['id'], income1.pk)

    def test_retrieve_income_needs_permission_api(self):
        """Test retrieve income limited by permission"""
        self.client.force_authenticate(user=self.user)

        res = self.client.get(reverse('apivs:payment-detail', args=[self.income.pk]))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_income_api(self):
        """Test retrieve income"""

        self.client.force_authenticate(user=self.ex_user)
        req1 = funcs.sample_request(owner=self.ex_user, number=981020, customer=self.customer)
        prof1 = funcs.sample_proforma(req=req1, owner=self.ex_user, number=983020)
        income1 = funcs.sample_income(proforma=prof1, owner=self.ex_user, number=9813030)

        res = self.client.get(reverse('apivs:payment-detail', args=[income1.pk]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['id'], income1.pk)
        self.assertEqual(res.data['amount'], income1.amount)

    def test_retrieve_income_limited_api(self):
        """Test retrieve income limited by user"""
        self.client.force_authenticate(user=self.ex_user)

        res = self.client.get(reverse('apivs:payment-detail', args=[self.income.pk]))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_income_needs_permission_api(self):
        """Test updating income needs permission"""

        self.client.force_authenticate(user=self.user)
        payload = {
            'amount': 2500000,
        }

        res = self.client.patch(reverse('apivs:payment-detail', args=[self.income.pk]), payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_income_api(self):
        """Test update income"""

        self.client.force_authenticate(user=self.ex_user)
        req1 = funcs.sample_request(owner=self.ex_user, number=981020, customer=self.customer)
        prof1 = funcs.sample_proforma(req=req1, owner=self.ex_user, number=983020)
        income1 = funcs.sample_income(proforma=prof1, owner=self.ex_user, number=9813030)
        payload = {
            'amount': 2450000,
        }
        res = self.client.patch(reverse('apivs:payment-detail', args=[income1.pk]), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['amount'], payload['amount'])

    def test_update_income_limited_api(self):
        """Test update income is limited by ownership"""

        self.client.force_authenticate(user=self.ex_user)

        payload = {
            'amount': 245000,
        }
        res = self.client.patch(reverse('apivs:payment-detail', args=[self.income.pk]), payload)
        income = Payment.objects.get(pk=self.income.pk)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(income.amount, self.income.amount)

    def test_delete_income_needs_permission_api(self):
        """Test deleting income needs permission(delete_payment)"""

        self.client.force_authenticate(user=self.user)
        res = self.client.delete(reverse('apivs:payment-detail', args=[self.income.pk]))
        exist = Payment.objects.filter(
            owner=self.income.owner,
            amount=self.income.amount,
            number=self.income.number,
        ).exists()

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(exist)

    def test_delete_income_api(self):
        """Test delete income"""

        self.client.force_authenticate(user=self.ex_user)
        req1 = funcs.sample_request(owner=self.ex_user, number=981020, customer=self.customer)
        prof1 = funcs.sample_proforma(req=req1, owner=self.ex_user, number=983020)
        income1 = funcs.sample_income(proforma=prof1, owner=self.ex_user, number=9813030)

        res = self.client.delete(reverse('apivs:payment-detail', args=[income1.pk]))

        exist = Payment.objects.filter(
            owner=income1.owner,
            amount=income1.amount,
            number=income1.number,
        ).exists()
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(exist)

    def test_delete_income_limited_api(self):
        """Test deleting income is limited by ownership"""

        self.client.force_authenticate(user=self.ex_user)

        res = self.client.delete(reverse('apivs:payment-detail', args=[self.income.pk]))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        exist = Payment.objects.filter(
            owner=self.income.owner,
            amount=self.income.amount,
            number=self.income.number,
        ).exists()
        self.assertTrue(exist)
