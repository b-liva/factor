from django.contrib.auth import get_user_model
from django.test import TestCase
from django.shortcuts import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from customer.models import Customer
from request.models import Requests, ReqSpec, ProjectType, RpmType, IMType, ICType, IPType, IEType
from accounts.tests import test_public_funcs as funcs

REQSPEC_URL = reverse('apivs:reqspec-list')


class PublicReqSepcTests(APITestCase):

    def setUp(self):
        self.user = funcs.sample_user(username='user')
        self.superuser = funcs.sample_superuser(username='superuser')
        self.ex_use = funcs.login_as_expert(username='expert')
        self.customer = funcs.sample_customer(owner=self.user, name='testcasecustomer')
        self.req = funcs.sample_request(number=981010, customer=self.customer, owner=self.user)

        self.specs_payload = [
            {'qty': 132, 'kw': 132, 'rpm': 1500, 'voltage': 380},
            {'qty': 315, 'kw': 160, 'rpm': 1500, 'voltage': 380},
            {'qty': 132, 'kw': 315, 'rpm': 3000, 'voltage': 380},
            {'qty': 75, 'kw': 75, 'rpm': 1000, 'voltage': 380},
        ]

    def test_login_reqired(self):
        """،Test login required for reqspecs operations."""
        # reqspec-list
        self.client = APIClient()
        res = self.client.get(REQSPEC_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        # reqspec-detail
        funcs.sample_reqspec(req=self.req, owner=self.user, **self.specs_payload[0])
        res = self.client.get(reverse('apivs:reqspec-detail', args=[1]))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateReqSepcTests(APITestCase):

    def setUp(self):
        self.user = funcs.sample_user(username='user')
        self.superuser = funcs.sample_superuser(username='superuser')
        self.ex_user = funcs.login_as_expert(username='expert')
        self.customer = funcs.sample_customer(owner=self.user, name='testcasecustomer')
        self.req = funcs.sample_request(number=981010, customer=self.customer, owner=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        # self.reqspe_type = ProjectType.objects.create(title='روتین'),
        self.reqspe_type = ProjectType.objects.create(title='lksjdf')
        self.reqspec_rpm_new = RpmType.objects.create(rpm=1500, pole=4)
        self.im = IMType.objects.create(title='IMB3')
        self.ic = ICType.objects.create(title='IC411')
        self.ip = IPType.objects.create(title='IP55')
        self.ie = IEType.objects.create(title='IE1')
        self.specs_payload = [
            {'code': 98585, 'qty': 2, 'kw': 132, 'rpm': 1500, 'rpm_new': self.reqspec_rpm_new, 'voltage': 380},
            {'code': 98586, 'qty': 1, 'kw': 160, 'rpm': 1500, 'rpm_new': self.reqspec_rpm_new, 'voltage': 380},
            {'code': 98587, 'qty': 3, 'kw': 315, 'rpm': 3000, 'rpm_new': self.reqspec_rpm_new, 'voltage': 380},
            {'code': 98588, 'qty': 5, 'kw': 75, 'rpm': 1000, 'rpm_new': self.reqspec_rpm_new, 'voltage': 380},
        ]

    def test_create_reqspec_needs_permission_api(self):
        res = self.client.post(REQSPEC_URL, self.specs_payload[0])

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_reqspec_api(self):
        """Test create reqspec"""
        self.client.force_authenticate(user=self.ex_user)
        req = funcs.sample_request(owner=self.ex_user, number=9855454, customer=self.customer)
        payload = {
            'req_id': req.pk,
            'type': self.reqspe_type.pk,
            'owner': self.ex_user.pk,
            'rpm_new': self.reqspec_rpm_new.pk,
        }
        self.specs_payload[0].pop('rpm_new')
        payload.update(self.specs_payload[0])

        res = self.client.post(REQSPEC_URL, payload)
        exist = ReqSpec.objects.filter(
            kw=payload['kw'],
            voltage=payload['voltage'],
            owner=payload['owner'],
            type=payload['type'],
            # code=payload['code'],
            qty=payload['qty'],
        ).exists()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exist)

    def test_create_spec_update_code_api(self):
        """Test create spec needs to update code according to MotorCodes"""
        self.client.force_authenticate(user=self.ex_user)
        req = funcs.sample_request(owner=self.ex_user, number=9855454, customer=self.customer)
        funcs.sample_motorcode(
            owner=self.ex_user,
            code=100100100,
            kw=160,
            speed=1500,
            im=self.im.pk,
            ip=self.ip.pk,
            ie=self.ie.pk,
            ic=self.ic.pk,
            voltage=380,
        )
        payload = {
            'req_id': req.pk,
            'owner': self.ex_user.pk,
            'qty': 1,
            'kw': 160,
            'rpm': 1500,
            'rpm_new': self.reqspec_rpm_new.pk,
            'im': self.im.pk,
            'ip': self.ip.pk,
            'ie': self.ie.pk,
            'ic': self.ic.pk,
            'voltage': 380,
            'type': self.reqspe_type.pk,
        }
        res = self.client.post(REQSPEC_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['code'], 100100100)

    def test_retrieve_reqspec_list_for_request_api(self):
        """Test retrieve specs of a request, needs to be filtered by request"""
        req = funcs.sample_request(number=981011, customer=self.customer, owner=self.ex_user)
        spec1 = funcs.sample_reqspec(req, owner=self.ex_user, **self.specs_payload[0])
        spec2 = funcs.sample_reqspec(req, owner=self.ex_user, **self.specs_payload[1])

        self.client.force_authenticate(user=self.ex_user)
        res = self.client.get(reverse('apivs:requests-reqspecs', args=[req.number]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0]['kw'], spec1.kw)

    def test_retrieve_reqsepc_list_for_request_limited_api(self):
        """Test retrieving spec list limited by request ownership and permissions."""

        req = funcs.sample_request(number=981012, customer=self.customer, owner=self.user)

        funcs.sample_reqspec(req, owner=self.ex_user, **self.specs_payload[0])
        funcs.sample_reqspec(req, owner=self.ex_user, **self.specs_payload[3])
        self.client.force_authenticate(user=self.ex_user)

        res = self.client.get(reverse('apivs:requests-reqspecs', args=[req.number]))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_reqspec_api(self):
        """Test retrieve spec"""

        req = funcs.sample_request(number=981012, customer=self.customer, owner=self.ex_user)

        spec1 = funcs.sample_reqspec(req, owner=self.ex_user, **self.specs_payload[0])
        spec2 = funcs.sample_reqspec(req, owner=self.ex_user, **self.specs_payload[3])
        self.client.force_authenticate(user=self.ex_user)

        res = self.client.get(reverse('apivs:reqspec-detail', args=[spec2.pk]))
        # todo: probably some bug with setUp(self).
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['kw'], spec2.kw)

    def test_retrieve_reqspec_limited_api(self):
        """Test retrieve spec is limited by ownership and permissions"""
        req = funcs.sample_request(number=981012, customer=self.customer, owner=self.user)

        spec1 = funcs.sample_reqspec(req, owner=self.user, **self.specs_payload[0])
        spec2 = funcs.sample_reqspec(req, owner=self.user, **self.specs_payload[3])

        self.client.force_authenticate(user=self.ex_user)

        res = self.client.get(reverse('apivs:reqspec-detail', args=[spec2.pk]))
        # todo: probably some bug with setUp(self).
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_reqspec_noperm_api(self):
        """Test update spec needs delete_reqspec permission."""

        req = funcs.sample_request(number=981012, customer=self.customer, owner=self.ex_user)

        spec1 = funcs.sample_reqspec(req, owner=self.ex_user, **self.specs_payload[0])
        spec2 = funcs.sample_reqspec(req, owner=self.ex_user, **self.specs_payload[3])
        self.client.force_authenticate(user=self.user)
        payload = {
            'kw': 1200,
        }
        res = self.client.patch(reverse('apivs:reqspec-detail', args=[spec2.pk]), payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_reqspec_api(self):
        """Test update spec"""

        req = funcs.sample_request(number=981012, customer=self.customer, owner=self.ex_user)

        spec1 = funcs.sample_reqspec(req, owner=self.ex_user, **self.specs_payload[0])
        spec2 = funcs.sample_reqspec(req, owner=self.ex_user, **self.specs_payload[3])
        self.client.force_authenticate(user=self.ex_user)
        payload = {
            'kw': 1200,
        }
        res = self.client.patch(reverse('apivs:reqspec-detail', args=[spec2.pk]), payload)
        # todo: probably some bug with setUp(self).
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['kw'], payload['kw'])

    def test_update_reqspec_limited_api(self):
        """Test update spec is limited by ownership and permissions"""
        # todo: what about the case: owner of the req but not reqspec.

        req = funcs.sample_request(number=981012, customer=self.customer, owner=self.user)

        spec1 = funcs.sample_reqspec(req, owner=self.user, **self.specs_payload[0])
        spec2 = funcs.sample_reqspec(req, owner=self.user, **self.specs_payload[3])
        self.client.force_authenticate(user=self.ex_user)
        payload = {
            'kw': 1200,
        }
        res = self.client.patch(reverse('apivs:reqspec-detail', args=[spec2.pk]), payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_reqspec_api(self):
        """Test delete spec"""

        req = funcs.sample_request(number=981012, customer=self.customer, owner=self.ex_user)

        spec1 = funcs.sample_reqspec(req, owner=self.ex_user, **self.specs_payload[0])
        spec2 = funcs.sample_reqspec(req, owner=self.ex_user, **self.specs_payload[3])
        self.client.force_authenticate(user=self.ex_user)

        res = self.client.delete(reverse('apivs:reqspec-detail', args=[spec2.pk]))
        exist = ReqSpec.objects.filter(pk=spec2.pk).exists()
        # todo: probably some bug with setUp(self).
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(exist)

    def test_delete_reqspec_limited_api(self):
        """Test delete spec is limited by ownership and permissions"""

        req = funcs.sample_request(number=981012, customer=self.customer, owner=self.user)

        spec1 = funcs.sample_reqspec(req, owner=self.user, **self.specs_payload[0])
        spec2 = funcs.sample_reqspec(req, owner=self.user, **self.specs_payload[3])
        self.client.force_authenticate(user=self.ex_user)

        res = self.client.delete(reverse('apivs:reqspec-detail', args=[spec2.pk]))
        exist = ReqSpec.objects.filter(pk=spec2.pk).exists()
        # todo: probably some bug with setUp(self).
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(exist)


class NewReqSpecTest(APITestCase):
    # todo: this class should be deleted after the above bug is fixed
    def test_retrieve_reqspec_new(self):
        """Test retrieve spec"""
        user = get_user_model().objects.create(username='username', password='pass1233')
        from customer.models import Type
        type = Type.objects.create(name='petro')
        customer = Customer.objects.create(name='name', owner=user, type=type)
        req = Requests.objects.create(number=981010, owner=user, customer=customer)

        spec1 = funcs.sample_reqspec(req, owner=user)
        spec2 = funcs.sample_reqspec(req, owner=user)
        self.client.force_authenticate(user=user)

        res = self.client.get(reverse('apivs:reqspec-detail', args=[spec2.pk]))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
