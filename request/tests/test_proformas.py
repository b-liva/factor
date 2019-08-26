import unittest
from django.test import TestCase, Client
from django.shortcuts import reverse
from django.conf import settings
from rest_framework import status
from accounts.tests import test_public_funcs as funcs
from request.forms.forms import ProformaForm
from request.models import Requests, ReqSpec, Xpref, PrefSpec


class PublicProformaTests(TestCase):
    def setUp(self):
        self.user = funcs.sample_user(username='userone')
        self.client = Client()

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


class PrivateProformaTest(TestCase):
    def setUp(self):
        self.user = funcs.sample_user(username='user')
        self.superuser = funcs.sample_superuser(username='superuser')
        self.ex_user = funcs.login_as_expert(username='ex_user')
        self.customer = funcs.sample_customer(owner=self.user, name='samplecustomer')
        self.req = funcs.sample_request(owner=self.user, customer=self.customer, number=981010)
        self.params = {

        }
        self.spec1 = funcs.sample_reqspec(owner=self.user, req=self.req, kw=55, rpm=1000)
        self.spec2 = funcs.sample_reqspec(owner=self.user, req=self.req, kw=315, rpm=1500)
        self.spec3 = funcs.sample_reqspec(owner=self.user, req=self.req, kw=160, rpm=3000)
        self.proforma = funcs.sample_proforma(req=self.req, owner=self.user, number=981000)
        self.client = Client(enforce_csrf_checks=False)

    def test_create_proforma_need_permission(self):
        """Test creating proforma need permissions"""

        self.client.force_login(user=self.user)
        res = self.client.get(reverse('pro_form'))
        # self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_create_proforma_get_page_successful(self):
        """Test create proforma"""
        self.client.force_login(user=self.ex_user)
        res = self.client.get(reverse('pro_form'))
        # print(res.context)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.context['message'], 'ثبت پیش فاکتور')

    def test_create_proforma_post_data_successful(self):
        """Test create proforma post page"""
        self.client.force_login(user=self.ex_user)
        req = funcs.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = funcs.sample_reqspec(owner=self.ex_user, req=req, kw=55, rpm=1000)
        spec2 = funcs.sample_reqspec(owner=self.ex_user, req=req, kw=315, rpm=1500)
        spec3 = funcs.sample_reqspec(owner=self.ex_user, req=req, kw=160, rpm=3000)
        payload = {
            # 'req_id': self.req.pk,
            'req_id': req.pk,
            'date_fa': ['۱۳۹۸-۰۶-۰۳'],
            'exp_date_fa': ['۱۳۹۸-۰۶-۰۳'],
            'summary': ['somte data goes heree.....'],
        }
        res = self.client.post(reverse('pro_form'), payload)
        self.assertRedirects(
            res,
            expected_url=reverse('prof_spec_form', args=[payload['req_id']]),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_create_proforma_by_req_colleague_successful(self):
        """Test req colleague can add proforma"""
        new_ex_user = funcs.login_as_expert(username='new_ex_user')
        self.client.force_login(user=new_ex_user)
        req = funcs.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        req.colleagues.add(self.user)
        print(req.colleagues.all())
        spec1 = funcs.sample_reqspec(owner=self.ex_user, req=req, kw=55, rpm=1000)
        spec2 = funcs.sample_reqspec(owner=self.ex_user, req=req, kw=315, rpm=1500)
        spec3 = funcs.sample_reqspec(owner=self.ex_user, req=req, kw=160, rpm=3000)
        payload = {
            # 'req_id': self.req.pk,
            'req_id': req.pk,
            'date_fa': ['۱۳۹۸-۰۶-۰۳'],
            'exp_date_fa': ['۱۳۹۸-۰۶-۰۳'],
            'summary': ['somte data goes heree.....'],
        }
        res = self.client.post(reverse('pro_form'), payload)
        self.assertRedirects(
            res,
            expected_url=reverse('prof_spec_form', args=[payload['req_id']]),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_create_proforma_no_req_fail(self):
        """Test proforma creation fails if no request is added."""
        # todo: additional failure tests needed.
        self.client.force_login(user=self.ex_user)
        req = funcs.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = funcs.sample_reqspec(owner=self.ex_user, req=req, kw=55, rpm=1000)
        spec2 = funcs.sample_reqspec(owner=self.ex_user, req=req, kw=315, rpm=1500)
        spec3 = funcs.sample_reqspec(owner=self.ex_user, req=req, kw=160, rpm=3000)
        payload = {
            # 'req_id': self.req.pk,
            'req_id': '',
            'date_fa': ['۱۳۹۸-۰۶-۰۳'],
            'exp_date_fa': ['۱۳۹۸-۰۶-۰۳'],
            'summary': ['somte data goes heree.....'],
        }
        res = self.client.post(reverse('pro_form'), payload)
        # print(res.context['form'].errors)
        self.assertTrue(res.context['form'].errors)

    def test_create_prefspec_user_not_req_owner_nor_prof_owner(self):
        """Test create prefspec needs permission
        :return redirect to error page
        """
        # todo: should be implemented or not? create pref spec need add_prefspec permission explicitly
        self.user = funcs.sample_user(username='thisUserIsSoLongAsYouCanSee')
        self.client.force_login(user=self.user)
        req = funcs.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = funcs.sample_reqspec(owner=self.user, req=req, kw=55, rpm=1000)
        spec2 = funcs.sample_reqspec(owner=self.user, req=req, kw=315, rpm=1500)
        spec3 = funcs.sample_reqspec(owner=self.user, req=req, kw=160, rpm=3000)
        proforma = funcs.sample_proforma(req=req, owner=self.ex_user, number=9820009)
        url = reverse('prof_spec_form', args=[proforma.pk])
        res = self.client.get(url)
        # self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_create_prefspec_user_is_req_owner(self):
        """Test req owner can add prespec to proforma"""
        self.client.force_login(user=self.user)
        req = funcs.sample_request(owner=self.user, customer=self.customer, number=981515)
        spec1 = funcs.sample_reqspec(owner=self.user, req=req, kw=55, rpm=1000)
        spec2 = funcs.sample_reqspec(owner=self.user, req=req, kw=315, rpm=1500)
        spec3 = funcs.sample_reqspec(owner=self.user, req=req, kw=160, rpm=3000)
        proforma = funcs.sample_proforma(req=req, owner=self.ex_user, number=9820009)
        url = reverse('prof_spec_form', args=[proforma.pk])
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_prefspec_user_is_proforma_owner(self):
        """Test proforma owner can add prespec to proforma"""
        self.client.force_login(user=self.user)
        req = funcs.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = funcs.sample_reqspec(owner=self.ex_user, req=req, kw=55, rpm=1000)
        spec2 = funcs.sample_reqspec(owner=self.ex_user, req=req, kw=315, rpm=1500)
        spec3 = funcs.sample_reqspec(owner=self.ex_user, req=req, kw=160, rpm=3000)
        proforma = funcs.sample_proforma(req=req, owner=self.user, number=9820009)
        url = reverse('prof_spec_form', args=[proforma.pk])
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_prefspec_create_form_page_success(self):
        """Test get prefspec form page"""
        self.client.force_login(user=self.ex_user)
        req = funcs.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = funcs.sample_reqspec(owner=self.ex_user, req=req, kw=55, rpm=1000)
        spec2 = funcs.sample_reqspec(owner=self.ex_user, req=req, kw=315, rpm=1500)
        spec3 = funcs.sample_reqspec(owner=self.ex_user, req=req, kw=160, rpm=3000)
        proforma = funcs.sample_proforma(req=req, owner=self.ex_user, number=982020)
        url = reverse('prof_spec_form', args=[proforma.pk])
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_prefspec_limited_by_user(self):
        """Test prefspec creation is limited by owner of proforma"""
        self.client.force_login(user=self.ex_user)
        self.ex_user.username = 'somethingveryspecific'
        self.ex_user.save()
        req = funcs.sample_request(owner=self.user, customer=self.customer, number=981515)
        spec1 = funcs.sample_reqspec(owner=self.user, req=req, kw=55, rpm=1000)
        spec2 = funcs.sample_reqspec(owner=self.user, req=req, kw=315, rpm=1500)
        spec3 = funcs.sample_reqspec(owner=self.user, req=req, kw=160, rpm=3000)
        proforma = funcs.sample_proforma(req=req, owner=self.user, number=982020)
        url = reverse('prof_spec_form', args=[proforma.pk])
        res = self.client.get(url)
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

