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
        print(res.context['form'].errors)
        self.assertTrue(res.context['form'].errors)
        self.assertFalse(exist)

    # List
    # Retrieve
    # Update
    # Delete

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
            len(res.context['reqspec']),
            req.reqspec_set.filter(is_active=True).count()
        )

    def test_create_prefspec_post_is_req_owner(self):
        """Test req owner can post prefspec data"""
        self.client.force_login(user=self.user)
        req = self.sample_request(owner=self.user, customer=self.customer, number=981515)
        spec1 = self.sample_reqspec(owner=self.user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.user, req_id=req, kw=160, rpm=3000)
        proforma = self.sample_proforma(req=req, owner=self.ex_user, number=9820009)

        res = self.client.post(reverse('pref_insert_spec_form', args=[proforma.pk]))
        print('res: ****: ', res)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

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
    # List
    # Retrieve
    # Update - Get
    # Update - Post
    # Delete
