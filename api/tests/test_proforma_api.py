from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.shortcuts import reverse
from accounts.tests import test_public_funcs as funcs
from request.models import Xpref

PROFORMA_URL = reverse('apivs:xpref-list')


class PublicProformaTests(APITestCase):

    def setUp(self):
        self.user = funcs.sample_user(username='user')
        self.superuser = funcs.sample_user(username='username')
        self.ex_user = funcs.login_as_expert(username='ex_user')
        self.client = APIClient()

        self.customer = funcs.sample_customer(owner=self.user, name='customerOne')
        self.req = funcs.sample_request(owner=self.user, number=981010, customer=self.customer)
        self.proforma = funcs.sample_proforma(req=self.req, number=981000, owner=self.user)

    def test_login_required(self):
        """Test Anonymous user can't access the url"""
        res = self.client.get(PROFORMA_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client.get(reverse('apivs:xpref-detail', args=[self.proforma.pk]))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateProformaTest(APITestCase):

    def setUp(self):
        self.user = funcs.sample_user(username='user')
        self.superuser = funcs.sample_user(username='username')
        self.ex_user = funcs.login_as_expert(username='ex_user')

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.customer = funcs.sample_customer(owner=self.user, name='customerOne')
        self.req = funcs.sample_request(owner=self.user, number=981010, customer=self.customer)
        self.proforma = funcs.sample_proforma(req=self.req, number=981000, owner=self.user)

    def test_create_proforma_successful_api(self):
        self.client.force_authenticate(user=self.ex_user)
        payload = {
            'req_id': self.req.pk,
            'number': 985050,
            'owner': self.user.pk,
            'number_auto': 985050,
            'date_fa': "1398-05-26",
        }
        res = self.client.post(PROFORMA_URL, payload)
        exist = Xpref.objects.filter(
            number=payload['number'],
            req_id=payload['req_id'],
            owner=self.ex_user,
        ).exists()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exist)
        self.assertEqual(res.data['number'], 985050)
        self.assertEqual(res.data['owner'], self.ex_user)

    def test_retrieve_proforma_permission_required_api(self):
        """Test retrieve proforma list is limited for a user that hasn't index_xpref permission"""
        res = self.client.get(PROFORMA_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_proforma_list_api(self):
        """Test retrieve proforma list: limited by ownership and permission"""
        self.client.force_authenticate(user=self.ex_user)

        req2 = funcs.sample_request(owner=self.ex_user, number=981011, customer=self.customer)
        proforma2 = funcs.sample_proforma(req=req2, number=981001, owner=self.ex_user)
        req3 = funcs.sample_request(owner=self.ex_user, number=981012, customer=self.customer)
        proforma3 = funcs.sample_proforma(req=req2, number=981002, owner=self.ex_user)
        req4 = funcs.sample_request(owner=self.ex_user, number=981013, customer=self.customer)
        proforma4 = funcs.sample_proforma(req=req2, number=981003, owner=self.user)

        res = self.client.get(PROFORMA_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0]['number'], 981001)

    def test_retrieve_proforma_login_required_api(self):
        res = self.client.get(reverse('apivs:xpref-detail', args=[self.proforma.pk]))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_proforma_api(self):
        self.client.force_authenticate(user=self.ex_user)
        req = funcs.sample_request(owner=self.ex_user, number=981011, customer=self.customer)
        proforma = funcs.sample_proforma(req=self.req, number=981050, owner=self.ex_user)

        res = self.client.get(reverse('apivs:xpref-detail', args=[proforma.pk]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['number'], proforma.number)

    def test_retrieve_proforma_limited_api(self):
        self.client.force_authenticate(user=self.ex_user)
        req = funcs.sample_request(owner=self.user, number=981011, customer=self.customer)
        proforma = funcs.sample_proforma(req=self.req, number=981050, owner=self.user)

        res = self.client.get(reverse('apivs:xpref-detail', args=[proforma.pk]))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_proforma_api(self):
        """Test proforma deletion"""
        self.client.force_authenticate(user=self.ex_user)
        proforma = funcs.sample_proforma(req=self.req, owner=self.ex_user, number=9810001)

        res = self.client.delete(reverse('apivs:xpref-detail', args=[proforma.pk]))
        exist = Xpref.objects.filter(
            number=proforma.number,
            req_id=proforma.req_id,
            owner=proforma.owner
        ).exists()

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(exist)

    def test_delete_proforma_limited_api(self):
        """Test deleting proforma is limited by permission and ownership"""

        self.client.force_authenticate(user=self.ex_user)
        res = self.client.delete(reverse('apivs:xpref-detail', args=[self.proforma.pk]))
        exist = Xpref.objects.filter(
            owner=self.proforma.owner,
            req_id=self.proforma.req_id,
            number=self.proforma.number
        ).exists()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(exist)

    def test_update_proforma_api(self):
        """Test update proforma"""
        self.client.force_authenticate(user=self.ex_user)
        proforma = funcs.sample_proforma(req=self.req, owner=self.ex_user, number=9810001)

        payload = {
            'number': 982020,
        }
        res = self.client.patch(reverse('apivs:xpref-detail', args=[proforma.pk]), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['number'], payload['number'])

    def test_update_proforma_limited_api(self):
        """Test update proforma is limited by permissions and ownership"""
        self.client.force_authenticate(user=self.ex_user)

        payload = {
            'number': 982020,
        }
        res = self.client.patch(reverse('apivs:xpref-detail', args=[self.proforma.pk]), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
