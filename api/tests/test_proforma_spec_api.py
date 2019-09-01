from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.shortcuts import reverse
from request.models import PrefSpec, Xpref
from accounts.tests.test_public_funcs import CustomAPITestCase

PREFSPEC_URL = reverse('apivs:prefspec-list')


class PublicPrefSpecTests(CustomAPITestCase):

    def setUp(self):
        super().setUp()

    def test_prefspec_login_required(self):
        """Test prefspec is login required."""

        res = self.client.get(PREFSPEC_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivatePrefSpecTest(CustomAPITestCase):
    def setUp(self):
        """Setup for private prefspecs test cases."""
        super().setUp()
        self.client.force_authenticate(user=self.user)

        self.specs_payload = [
            {'qty': 132, 'kw': 132, 'rpm': 1500, 'voltage': 380},
            {'qty': 315, 'kw': 160, 'rpm': 1500, 'voltage': 380},
            {'qty': 132, 'kw': 315, 'rpm': 3000, 'voltage': 380},
            {'qty': 75, 'kw': 75, 'rpm': 1000, 'voltage': 380},
        ]

    def test_create_prefspec_api(self):
        self.client.force_authenticate(user=self.ex_user)
        proforma = self.sample_proforma(req=self.req, owner=self.ex_user, number=837498345)
        spec = self.sample_reqspec(req_id=self.req, owner=self.ex_user, **self.specs_payload[0])
        payload = {
            'owner': self.ex_user.pk,
            'xpref_id': proforma.pk,
            'reqspec_eq': spec.pk,
        }
        payload.update(self.specs_payload[0])
        res = self.client.post(PREFSPEC_URL, payload)
        exist = PrefSpec.objects.filter(
            owner=payload['owner'],
            xpref_id=payload['xpref_id'],
            reqspec_eq=payload['reqspec_eq'],
            kw=payload['kw'],
            rpm=payload['rpm'],
            voltage=payload['voltage'],
        ).exists()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exist)

    def test_retrieve_prefspec_list_api(self):
        """Test retrieve prefspecs list"""

        self.client.force_authenticate(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=982020)
        spec1 = self.sample_reqspec(req_id=req, owner=self.ex_user, **self.specs_payload[0])
        spec2 = self.sample_reqspec(req_id=req, owner=self.ex_user, **self.specs_payload[1])
        prof = self.sample_proforma(req=req, number=984040, owner=self.ex_user)

        prefspec1 = self.sample_prefspec(proforma=prof, owner=self.ex_user, reqspe=spec1)
        prefspec2 = self.sample_prefspec(proforma=prof, owner=self.ex_user, reqspe=spec2)

        res = self.client.get(reverse('apivs:xpref-prefspecs', args=[prof.pk]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0]['id'], prefspec1.pk)

    def test_retrieve_prefspec_list_limited_api(self):
        """Test retrieve prefspecs list is limited by permissions and ownership"""

        self.client.force_authenticate(user=self.ex_user)

        spec1 = self.sample_reqspec(req_id=self.req, owner=self.user, **self.specs_payload[0])
        spec2 = self.sample_reqspec(req_id=self.req, owner=self.user, **self.specs_payload[1])

        prefspec1 = self.sample_prefspec(proforma=self.proforma, owner=self.user, reqspe=spec1)
        prefspec2 = self.sample_prefspec(proforma=self.proforma, owner=self.user, reqspe=spec2)

        res = self.client.get(reverse('apivs:xpref-prefspecs', args=[self.proforma.pk]))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_prefspec_api(self):
        """Test retrieve prefspec"""
        self.client.force_authenticate(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=982020)
        spec1 = self.sample_reqspec(req_id=req, owner=self.ex_user, **self.specs_payload[0])
        spec2 = self.sample_reqspec(req_id=req, owner=self.ex_user, **self.specs_payload[1])
        prof = self.sample_proforma(req=req, number=984040, owner=self.ex_user)

        prefspec1 = self.sample_prefspec(proforma=prof, owner=self.ex_user, reqspe=spec1)
        prefspec2 = self.sample_prefspec(proforma=prof, owner=self.ex_user, reqspe=spec2)

        res = self.client.get(reverse('apivs:prefspec-detail', args=[prefspec1.pk]))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['id'], prefspec1.pk)

    def test_retrieve_prefspec_limited_api(self):
        """Test retrieve prefspec limited by permission and ownership"""

        self.client.force_authenticate(self.ex_user)

        spec1 = self.sample_reqspec(req_id=self.req, owner=self.user, **self.specs_payload[0])
        spec2 = self.sample_reqspec(req_id=self.req, owner=self.user, **self.specs_payload[1])

        prefspec1 = self.sample_prefspec(proforma=self.proforma, owner=self.user, reqspe=spec1)
        prefspec2 = self.sample_prefspec(proforma=self.proforma, owner=self.user, reqspe=spec2)

        res = self.client.get(reverse('apivs:reqspec-detail', args=[prefspec1.pk]))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_prefspec_api(self):
        """Test update prefspec"""
        # todo: It shouldn't be updated directly.
        self.client.force_authenticate(self.ex_user)

        req = self.sample_request(owner=self.ex_user, number=982020)
        spec1 = self.sample_reqspec(req_id=req, owner=self.ex_user, **self.specs_payload[0])
        spec2 = self.sample_reqspec(req_id=req, owner=self.ex_user, **self.specs_payload[1])
        prof = self.sample_proforma(req=req, number=984040, owner=self.ex_user)

        prefspec1 = self.sample_prefspec(proforma=prof, owner=self.ex_user, reqspe=spec1)
        prefspec2 = self.sample_prefspec(proforma=prof, owner=self.ex_user, reqspe=spec2)

        payload = {
            'kw': 355,
            'rpm': 1500,
        }

        res = self.client.patch(reverse('apivs:prefspec-detail', args=[prefspec1.pk]), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['kw'], payload['kw'])

    def test_update_prefspec_limited_api(self):
        """Test update prefspec is limited by permissions and ownership"""

        self.client.force_authenticate(user=self.ex_user)
        spec1 = self.sample_reqspec(req_id=self.req, owner=self.user, **self.specs_payload[0])
        spec2 = self.sample_reqspec(req_id=self.req, owner=self.user, **self.specs_payload[1])

        prefspec1 = self.sample_prefspec(proforma=self.proforma, owner=self.user, reqspe=spec1)
        prefspec2 = self.sample_prefspec(proforma=self.proforma, owner=self.user, reqspe=spec2)

        payload = {
            'kw': 355,
            'rpm': 1500,
        }

        res = self.client.patch(reverse('apivs:reqspec-detail', args=[prefspec1.pk]), payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_prefspec_api(self):
        """Test delete prefspec"""

        self.client.force_authenticate(self.ex_user)

        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=982020)
        spec1 = self.sample_reqspec(req_id=req, owner=self.ex_user, **self.specs_payload[0])
        spec2 = self.sample_reqspec(req_id=req, owner=self.ex_user, **self.specs_payload[1])
        prof = self.sample_proforma(req=req, number=984040, owner=self.ex_user)

        prefspec1 = self.sample_prefspec(proforma=prof, owner=self.ex_user, reqspe=spec1)
        prefspec2 = self.sample_prefspec(proforma=prof, owner=self.ex_user, reqspe=spec2)

        res = self.client.delete(reverse('apivs:prefspec-detail', args=[prefspec1.pk]))
        exist = PrefSpec.objects.filter(
            pk=prefspec1.pk,
            xpref_id=prof,
            owner=self.ex_user,
            reqspec_eq=spec1,
        ).exists()
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(exist)

    def test_delete_prefspec_limited_api(self):
        """Test delete prefspec is limited by permissions and ownership"""

        self.client.force_authenticate(user=self.ex_user)
        spec1 = self.sample_reqspec(req_id=self.req, owner=self.user, **self.specs_payload[0])
        spec2 = self.sample_reqspec(req_id=self.req, owner=self.user, **self.specs_payload[1])

        prefspec1 = self.sample_prefspec(proforma=self.proforma, owner=self.user, reqspe=spec1)
        prefspec2 = self.sample_prefspec(proforma=self.proforma, owner=self.user, reqspe=spec2)

        res = self.client.delete(reverse('apivs:prefspec-detail', args=[prefspec1.pk]))
        exist = PrefSpec.objects.filter(
            pk=prefspec1.pk,
            xpref_id=self.proforma,
            owner=self.user,
            reqspec_eq=spec1,
        ).exists()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(exist)
