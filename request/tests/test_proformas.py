import unittest
from django.test import TestCase, Client
from django.shortcuts import reverse
from django.conf import settings
from rest_framework import status
from accounts.tests.test_public_funcs import CustomAPITestCase
from request.forms.forms import ProformaForm
from request.models import Requests, ReqSpec, Xpref, PrefSpec


class PublicProformaTests(CustomAPITestCase):

    def test_create_proforma_login_required(self):
        """Test create proforma need authentication"""
        res = self.client.get(reverse('pro_form'))
        self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(
            res,
            expected_url=settings.LOGIN_URL + '?next=' + reverse('pro_form'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_index_proforma_login_required(self):
        """Test index proforma need authentication"""
        res = self.client.get(reverse('pref_index'))
        self.assertRedirects(
            res,
            expected_url=settings.LOGIN_URL + '?next=' + reverse('pref_index'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )


class PrivateProformaTest(CustomAPITestCase):

    # PROFORMA
    # Create
    def test_create_proforma_get_needs_permission(self):
        """Test creating proforma needs permissions"""

        self.client.force_login(user=self.user)
        res = self.client.get(reverse('pro_form'))
        # self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_create_proforma_post_needs_permission(self):
        """Test sending proforma post data needs permission"""
        self.client.force_login(user=self.user)
        res = self.client.post(reverse('prof_spec_form', args=[self.proforma.pk]), self.proforma_payload)
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_create_proforma_get_successful(self):
        """Test create proforma"""
        self.client.force_login(user=self.ex_user)
        res = self.client.get(reverse('pro_form'))
        # print(res.context)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.context['message'], 'ثبت پیش فاکتور')

    def test_create_proforma_post_successful(self):
        """Test create proforma post page"""
        self.client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=160, rpm=3000)
        self.proforma_payload.update({'req_id': req.pk})
        res = self.client.post(reverse('pro_form'), self.proforma_payload)
        self.assertRedirects(
            res,
            # todo: this has a bug --> payload['req_id']
            expected_url=reverse('prof_spec_form', args=[self.proforma_payload['req_id']]),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_create_proforma_get_colleague_successful(self):
        """Test create proforma by request colleague successfully"""
        new_ex_user = self.sample_expert_user(username='new_ex_user')
        self.client.force_login(user=new_ex_user)
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=160, rpm=3000)
        req.colleagues.add(new_ex_user)
        res = self.client.get(reverse('pro_form'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_proforma_post_colleague_successful(self):
        """Test req colleague can add proforma"""
        new_ex_user = self.sample_expert_user(username='new_ex_user')
        self.client.force_login(user=new_ex_user)
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=160, rpm=3000)
        req.colleagues.add(new_ex_user)
        self.proforma_payload.update({'req_id': req.pk})
        res = self.client.post(reverse('pro_form'), self.proforma_payload)
        self.assertRedirects(
            res,
            expected_url=reverse('prof_spec_form', args=[self.proforma_payload['req_id']]),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_create_proforma_post_no_req_fail(self):
        """Test proforma creation fails if no request is added."""
        # todo: additional failure tests needed.
        self.client.force_login(user=self.ex_user)
        exist = Requests.objects.filter(pk=1000).exists()
        self.proforma_payload.update({'req_id': 1000})
        res = self.client.post(reverse('pro_form'), self.proforma_payload)
        self.assertTrue(res.context['form'].errors)
        self.assertFalse(exist)

    # List
    def test_index_proforma_needs_permission(self):
        """Test index proforma needs permission"""
        self.client.force_login(user=self.user)
        res = self.client.get(reverse('pref_index'))
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )

    def test_index_proforma_success(self):
        """Test index proforma success"""
        self.client.force_login(user=self.ex_user)
        res = self.client.get(reverse('pref_index'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # Retrieve
    def test_retrieve_proforma_needs_permission(self):
        """Test retrieving proforma needs permission"""
        self.client.force_login(user=self.user)
        res = self.client.get(reverse('pref_details', args=[self.proforma.pk]))
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )

    def test_retrieve_proforma_success(self):
        """Test retrieving proforma needs permission"""
        self.client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, number=987643)

        self.sample_reqspec(owner=self.ex_user, kw=550, rpm=1000)
        self.sample_reqspec(owner=self.ex_user, kw=355, rpm=1500)
        proforma = self.sample_proforma(req=req, owner=self.ex_user, number=983424)
        res = self.client.get(reverse('pref_details', args=[proforma.pk]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.context['pref'].pk, proforma.pk)

    # Update
    # Delete
    def test_delete_proforma_get_needs_permission(self):
        """Test delete proforma gettin form needs permission"""
        self.client.force_login(user=self.user)
        res = self.client.get(reverse('pref_delete', args=[self.proforma.pk]))
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )

    def test_delete_proforma_post_needs_permission(self):
        """Test delete proforma posting data needs permission"""
        self.client.force_login(user=self.user)
        res = self.client.post(reverse('pref_delete', args=[self.proforma.pk]))
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )

    def test_delete_proforma_get_limited_by_owner(self):
        """Test delete proforma gettin form limited by owner"""
        self.client.force_login(user=self.ex_user)
        res = self.client.get(reverse('pref_delete', args=[self.proforma.pk]))
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )

    def test_delete_proforma_post_limited_by_owner(self):
        """Test delete proforma posting data limited by owner"""
        self.client.force_login(user=self.ex_user)
        res = self.client.post(reverse('pref_delete', args=[self.proforma.pk]))
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )

    def test_delete_proforma_get_success(self):
        """Test delete proforma gettin form success"""
        self.client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, number=986354)
        spec1 = self.sample_reqspec(owner=self.ex_user, kw=225)
        spec2 = self.sample_reqspec(owner=self.ex_user, kw=125)
        proforma = self.sample_proforma(owner=self.ex_user, number=2435, req=req)
        res = self.client.get(reverse('pref_delete', args=[proforma.pk]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.context['fn'], 'prof_del')

    def test_delete_proforma_post_success(self):
        """Test delete proforma posting data success"""
        self.client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, number=986354)
        spec1 = self.sample_reqspec(owner=self.ex_user, kw=225)
        spec2 = self.sample_reqspec(owner=self.ex_user, kw=125)
        proforma = self.sample_proforma(owner=self.ex_user, number=2435, req=req)
        prefspec1 = self.sample_prefspec(proforma=proforma, owner=self.ex_user, reqspe=spec1)
        prefspec2 = self.sample_prefspec(proforma=proforma, owner=self.ex_user, reqspe=spec2)
        res = self.client.post(reverse('pref_delete', args=[proforma.pk]))
        exist = Xpref.objects.filter(pk=proforma.pk, is_active=True).exists()
        exist_spec1_active = PrefSpec.objects.filter(pk=prefspec1.pk).exists()
        exist_spec2_active = PrefSpec.objects.filter(pk=prefspec1.pk).exists()
        exist_spec1_not_active = PrefSpec.objects.filter(pk=prefspec2.pk, is_active=True).exists()
        exist_spec2_not_active = PrefSpec.objects.filter(pk=prefspec2.pk, is_active=True).exists()

        self.assertRedirects(
            res,
            expected_url=reverse('pref_index'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )
        self.assertFalse(exist)
        self.assertTrue(exist_spec1_active)
        self.assertTrue(exist_spec2_active)
        self.assertFalse(exist_spec1_not_active)
        self.assertFalse(exist_spec2_not_active)

    # PROFORMA SPEC
    # Create
    def test_create_prefspec_get_user_not_req_owner_nor_prof_owner(self):
        """Test create prefspec needs permission
        :return redirect to error page
        """
        # todo: should be implemented or not? create pref spec need add_prefspec permission explicitly
        self.user = self.sample_user(username='thisUserIsSoLongAsYouCanSee')
        self.client.force_login(user=self.user)
        req = self.sample_request(owner=self.ex_user, number=981515)
        spec1 = self.sample_reqspec(owner=self.user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.user, req_id=req, kw=160, rpm=3000)
        proforma = self.sample_proforma(req=req, owner=self.ex_user, number=9820009)
        res = self.client.get(reverse('prof_spec_form', args=[proforma.pk]))
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_create_prefspec_post_user_not_req_owner_nor_prof_owner(self):
        """Test create prefspec needs permission
        :return redirect to error page
        """
        # todo: should be implemented or not? create pref spec need add_prefspec permission explicitly
        self.user = self.sample_user(username='thisUserIsSoLongAsYouCanSee')
        self.client.force_login(user=self.user)
        req = self.sample_request(owner=self.ex_user, number=981515)
        spec1 = self.sample_reqspec(owner=self.user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.user, req_id=req, kw=160, rpm=3000)
        proforma = self.sample_proforma(req=req, owner=self.ex_user, number=9820009)
        res = self.client.post(reverse('prof_spec_form', args=[proforma.pk]), self.prefspec_payload)
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_create_prefspec_get_user_is_req_owner(self):
        """Test req owner can get prefspec form"""
        self.client.force_login(user=self.user)
        req = self.sample_request(owner=self.user, customer=self.customer, number=981515)
        spec1 = self.sample_reqspec(owner=self.user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.user, req_id=req, kw=160, rpm=3000)
        spec4 = self.sample_reqspec(owner=self.user, req_id=req, kw=160, rpm=3000, is_active=False)
        proforma = self.sample_proforma(req=req, owner=self.ex_user, number=9820009)
        res = self.client.get(reverse('prof_spec_form', args=[proforma.pk]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.context['proforma'].pk, proforma.pk)
        self.assertEqual(res.context['req_obj'].pk, req.pk)
        self.assertEqual(
            len(res.context['reqspecs']),
            req.reqspec_set.filter(is_active=True).count()
        )
        self.assertEqual(
            len(res.context['prefspecs']),
            proforma.prefspec_set.filter(is_active=True).count()
        )

    def test_create_prefspec_post_req_owner_no_permission(self):
        """Test req owner can post prefspec data"""
        self.client.force_login(user=self.user)
        req = self.sample_request(owner=self.user, customer=self.customer, number=981515)
        spec1 = self.sample_reqspec(owner=self.user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.user, req_id=req, kw=160, rpm=3000)
        proforma = self.sample_proforma(req=req, owner=self.ex_user, number=9820009)

        res = self.client.post(reverse('pref_insert_spec_form', args=[proforma.pk]))
        # self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_create_prefspec_post_req_owner_no_payload(self):
        """Test req owner can post prefspec data"""
        self.client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=160, rpm=3000)
        proforma = self.sample_proforma(req=req, owner=self.ex_user, number=9820009)
        res = self.client.post(reverse('pref_insert_spec_form', args=[proforma.pk]))
        self.assertRedirects(
            res,
            expected_url=reverse("prof_spec_form", args=[proforma.pk]),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )

    def test_create_prefspec_get_form_user_is_proforma_owner(self):
        """Test proforma owner can add prespec to proforma"""
        self.client.force_login(user=self.user)
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=160, rpm=3000)
        proforma = self.sample_proforma(req=req, owner=self.user, number=9820009)
        res = self.client.get(reverse('prof_spec_form', args=[proforma.pk]))
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )

    def test_create_prefspec_get_form_success(self):
        """Test get prefspec form page"""
        # todo: is this working?
        self.client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, number=981515)
        spec1 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=160, rpm=3000)
        proforma = self.sample_proforma(req=req, owner=self.ex_user, number=982020)
        res = self.client.get(reverse('prof_spec_form', args=[proforma.pk]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_prefspec_get_form_limited_by_user(self):
        """Test prefspec creation is limited by owner of proforma"""
        self.client.force_login(user=self.ex_user)
        self.ex_user.username = 'somethingveryspecific'
        self.ex_user.save()
        req = self.sample_request(owner=self.user, number=981515)
        spec1 = self.sample_reqspec(owner=self.user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.user, req_id=req, kw=160, rpm=3000)
        proforma = self.sample_proforma(req=req, owner=self.user, number=982020)
        res = self.client.get(reverse('prof_spec_form', args=[proforma.pk]))
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    # def test_create_prefspec_post_all_prices_zero_fail(self):

    def test_create_prefspec_post_success(self):
        """Test prefsepcs creation fails if all prices are zeros."""
        self.client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=160, rpm=3000)
        proforma = self.sample_proforma(req=req, owner=self.ex_user, number=9820009)
        # payload = [
        #     {'spec_id': spec1.pk, 'qty': 3, 'price': 53135151},
        #     {'spec_id': spec2.pk, 'qty': 3, 'price': 53100151},
        #     {'spec_id': spec3.pk, 'qty': 3, 'price': 53105451},
        # ]
        payload = {
            'qty': ['1', '1', '2'], 'price': ['3452345', '2345345', '83975'], 'spec_id': [spec1.pk, spec2.pk, spec3.pk],
        }
        res = self.client.post(reverse('pref_insert_spec_form', args=[proforma.pk]), payload)

        self.assertRedirects(
            res,
            expected_url=reverse('pref_details', args=[proforma.pk]),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )
        response = self.client.get(reverse('pref_details', args=[proforma.pk]))
        prefspecs = proforma.prefspec_set.all().count()
        self.assertEqual(response.context['prefspecs'].count(), prefspecs)

    def test_create_prefspec_post_all_prices_zero_fail(self):
        """Test prefsepcs creation fails if all prices are zeros."""
        self.client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=160, rpm=3000)
        proforma = self.sample_proforma(req=req, owner=self.ex_user, number=9820009)
        payload = {
            'qty': ['1', '1', '2'], 'price': [0, 0, 0], 'spec_id': [spec1.pk, spec2.pk, spec3.pk],
        }
        res = self.client.post(reverse('pref_insert_spec_form', args=[proforma.pk]), payload)
        self.assertRedirects(
            res,
            expected_url=reverse('prof_spec_form', args=[proforma.pk]),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )
        response = self.client.get(reverse('pref_details', args=[proforma.pk]))
        prefspecs = proforma.prefspec_set.all().count()
        self.assertEqual(0, prefspecs)

    def test_create_prefspec_post_all_prices_empty_fail(self):
        """Test prefsepcs creation fails if all prices are zeros."""
        self.client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=160, rpm=3000)
        proforma = self.sample_proforma(req=req, owner=self.ex_user, number=9820009)
        payload = {
            'qty': ['1', '1', '2'], 'price': ['', '', ''], 'spec_id': [spec1.pk, spec2.pk, spec3.pk],
        }
        res = self.client.post(reverse('pref_insert_spec_form', args=[proforma.pk]), payload)
        self.assertRedirects(
            res,
            expected_url=reverse('prof_spec_form', args=[proforma.pk]),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )
        response = self.client.get(reverse('pref_details', args=[proforma.pk]))
        prefspecs = proforma.prefspec_set.all().count()
        self.assertEqual(0, prefspecs)

    def test_create_prefspec_post_all_qty_zero_fail(self):
        """Test prefsepcs creation fails if all qty are zeros."""
        self.client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=160, rpm=3000)
        proforma = self.sample_proforma(req=req, owner=self.ex_user, number=9820009)
        payload = {
            'qty': ['0', '0', '0'], 'price': ['651', '68435', '68451'], 'spec_id': [spec1.pk, spec2.pk, spec3.pk],
        }
        res = self.client.post(reverse('pref_insert_spec_form', args=[proforma.pk]), payload)

        self.assertRedirects(
            res,
            expected_url=reverse('prof_spec_form', args=[proforma.pk]),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )
        response = self.client.get(reverse('pref_details', args=[proforma.pk]))
        prefspecs = proforma.prefspec_set.all().count()
        self.assertEqual(0, prefspecs)

    def test_create_prefspec_post_string_price_fail(self):
        """Test prefsepcs creation fails if all qty are zeros."""
        self.client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=160, rpm=3000)
        proforma = self.sample_proforma(req=req, owner=self.ex_user, number=9820009)
        payload = {
            'qty': ['515', '3531', '34'], 'price': ['651', '68435', 'dgfg'], 'spec_id': [spec1.pk, spec2.pk, spec3.pk],
        }
        res = self.client.post(reverse('pref_insert_spec_form', args=[proforma.pk]), payload)

        self.assertRedirects(
            res,
            expected_url=reverse('prof_spec_form', args=[proforma.pk]),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )
        response = self.client.get(reverse('pref_details', args=[proforma.pk]))
        prefspecs = proforma.prefspec_set.all().count()
        self.assertEqual(0, prefspecs)

    # List
    # Retrieve
    # Update
    def test_update_prefspec_get_needs_permission(self):
        """Test getting prefspec update form need permission"""
        self.client.force_login(user=self.user)
        res = self.client.get(reverse('pref_edit_form', args=[self.proforma.pk]))
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_update_prefspec_post_needs_permission(self):
        """Test postin form data to update prefspec needs permission"""
        self.client.force_login(user=self.user)
        payload = {}
        res = self.client.post(reverse('pref_edit', args=[self.proforma.pk]), payload)
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_update_prefspec_get_limited_proforma_owner(self):
        """Test only proforma owner can update prefpsecs"""
        self.client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=160, rpm=3000)

        res = self.client.get(reverse('pref_edit_form', args=[self.proforma.pk]))
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_update_prefspec_post_limited_proforma_owner(self):
        """Test only proforma owner can update prefpsecs"""
        self.client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=160, rpm=3000)

        payload = {
            'qty': ['1', '1', '2'], 'price': [2345, 2345, 2345], 'spec_id': [spec1.pk, spec2.pk, spec3.pk],
        }
        res = self.client.post(reverse('pref_edit', args=[self.proforma.pk]), payload)
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_update_prefspec_get_success(self):
        """Test getting proforma update form successfully."""
        self.client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=160, rpm=3000)
        proforma = self.sample_proforma(req=req, owner=self.ex_user, number=9820009)

        res = self.client.get(reverse('pref_edit_form', args=[proforma.pk]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_prefspec_post_sent_zero_prices_fail(self):
        """Test if all prices are zero will fail."""
        self.client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=160, rpm=3000)
        proforma = self.sample_proforma(req=req, owner=self.ex_user, number=9820009)
        payload = {
            'qty': ['1', '1', '2'], 'price': ['3452345', '2345345', '83975'], 'spec_id': [spec1.pk, spec2.pk, spec3.pk],
        }
        res = self.client.post(reverse('pref_insert_spec_form', args=[proforma.pk]), payload)

        self.assertRedirects(
            res,
            expected_url=reverse('pref_details', args=[proforma.pk]),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )
        response = self.client.get(reverse('pref_details', args=[proforma.pk]))
        prefspecs = proforma.prefspec_set.all().count()
        self.assertEqual(response.context['prefspecs'].count(), prefspecs)
        payload = {
            'qty': ['1', '1', '2'], 'qty_sent': ['1', '1', '1'], 'price': [0, 0, 0], 'spec_id': [spec1.pk, spec2.pk, spec3.pk],
        }
        res = self.client.post(reverse('pref_edit', args=[proforma.pk]), payload)
        self.assertRedirects(
            res,
            expected_url=reverse('pref_edit_form', args=[proforma.pk]),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_update_prefspec_post_sent_empty_prices_fail(self):
        """Test if all prices are empty will fail."""
        self.client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=160, rpm=3000)
        proforma = self.sample_proforma(req=req, owner=self.ex_user, number=9820009)
        payload = {
            'qty': ['1', '1', '2'], 'price': ['3452345', '2345345', '83975'], 'spec_id': [spec1.pk, spec2.pk, spec3.pk],
        }
        res = self.client.post(reverse('pref_insert_spec_form', args=[proforma.pk]), payload)

        self.assertRedirects(
            res,
            expected_url=reverse('pref_details', args=[proforma.pk]),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )
        response = self.client.get(reverse('pref_details', args=[proforma.pk]))
        prefspecs = proforma.prefspec_set.all().count()
        self.assertEqual(response.context['prefspecs'].count(), prefspecs)
        payload = {
            'qty': ['1', '1', '2'], 'qty_sent': ['1', '1', '1'], 'price': ['', '', ''], 'spec_id': [spec1.pk, spec2.pk, spec3.pk],
        }
        res = self.client.post(reverse('pref_edit', args=[proforma.pk]), payload)
        self.assertRedirects(
            res,
            expected_url=reverse('pref_edit_form', args=[proforma.pk]),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_update_prefspec_post_sent_gt_qty_fail(self):
        """Test if qty sent is greater than qty it will fail."""
        self.client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=160, rpm=3000)
        proforma = self.sample_proforma(req=req, owner=self.ex_user, number=9820009)
        payload = {
            'qty': ['1', '1', '2'], 'price': ['3452345', '2345345', '83975'], 'spec_id': [spec1.pk, spec2.pk, spec3.pk],
        }
        res = self.client.post(reverse('pref_insert_spec_form', args=[proforma.pk]), payload)

        self.assertRedirects(
            res,
            expected_url=reverse('pref_details', args=[proforma.pk]),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )
        response = self.client.get(reverse('pref_details', args=[proforma.pk]))
        prefspecs = proforma.prefspec_set.all().count()
        self.assertEqual(response.context['prefspecs'].count(), prefspecs)
        payload = {
            'qty': ['1', '1', '2'], 'qty_sent': ['1', '1', '5'], 'price': ['3452345', '2345345', '83975'], 'spec_id': [spec1.pk, spec2.pk, spec3.pk],
        }
        res = self.client.post(reverse('pref_edit', args=[proforma.pk]), payload)
        self.assertRedirects(
            res,
            expected_url=reverse('pref_edit_form', args=[proforma.pk]),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )
    # Delete
