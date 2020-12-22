import datetime

from django.core.cache import cache
from django.shortcuts import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.conf import settings
from accounts.tests.test_public_funcs import CustomAPITestCase
from core.tests.factory import factories as core_factories
from request.models import Xpref
from request.tests.factory import factories


class TestPublicCost(CustomAPITestCase):

    def setUp(self):
        super().setUp()
        self.client_anon = APIClient()
        self.proforma = factories.ProformaFactory.create()
        factories.ProformaSpecFactory.create(xpref_id=self.proforma, price=1000000000, kw=132, rpm=1500)

    def test_prevents_unauth_user_to_get_proforma_profit(self):

        url = reverse('prof_profit', kwargs={'ypref_pk': self.proforma.pk})
        res = self.client_anon.get(url)
        self.assertRedirects(
            res,
            expected_url=settings.LOGIN_URL + '?next=' + reverse('prof_profit', kwargs={'ypref_pk': self.proforma.pk}),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )


class PrivateTestCost(CustomAPITestCase):

    def setUp(self):
        super().setUp()
        self.client_exp = APIClient()
        self.ex_user = core_factories.create_user()
        self.ex_user = core_factories.add_user_to_groupe(self.ex_user)
        self.client_exp.force_authenticate(user=self.ex_user)

        self.proforma = factories.ProformaFactory.create()
        factories.ProformaSpecFactory.create(xpref_id=self.proforma, price=1000000000, kw=132, rpm=1500)

    def test_prevents_user_with_no_permission_to_get_proforma_profit(self):
        self.client.force_login(self.user)
        # print('item01: ', self.proforma.prefspec_set.all())
        url = reverse('prof_profit', kwargs={'ypref_pk': self.proforma.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_get_proforma_profit(self):
        self.client.force_login(self.superuser)

        # print('item02: ', self.proforma.prefspec_set.all())
        url = reverse('prof_profit', kwargs={'ypref_pk': self.proforma.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(
            res,
            expected_url=reverse('default_cost', kwargs={'ypref_pk': self.proforma.pk}),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_302_FOUND
        )

    def test_if_request_has_filter_data(self):
        self.client.force_login(self.superuser)

        url = reverse('prof_profit', kwargs={'ypref_pk': self.proforma.pk})
        res = self.client.get(url)
        ca = cache.get('item')
        self.assertEqual(ca['first'], 1)
        print(res.context['only_test'])

    def test_save_data_to_cache(self):
        pass

    def test_get_data_from_cache(self):
        pass

    def test_calculate_proforma_profit(self):
        self.client.force_login(self.superuser)

        # date = datetime.date(2020, 10, 15)

        import jdatetime
        date = jdatetime.date(year=1399, month=7, day=15)
        date = date.togregorian()

        self.proforma.pub_date = date
        self.proforma.save()

        factories.ProformaSpecFactory.create(xpref_id=self.proforma, price=160000000, kw=18.5, rpm=3000)
        factories.ProformaSpecFactory.create(xpref_id=self.proforma, price=160000000, kw=2500, rpm=3000)
        for a in self.proforma.prefspec_set.all():
            print(a.kw, a.rpm, a.price)
        url = reverse('prof_profit', kwargs={'ypref_pk': self.proforma.pk})
        res = self.client.get(url)
        # self.assertIn('pspecs_with_profit', res.context)
        # self.assertIn('pspecs_no_profit', res.context)
        # specs_profit = res.context['pspecs_with_profit']
        # specs_not_profit = res.context['pspecs_no_profit']
        # self.assertIsNotNone(specs_profit)
        # self.assertIsNotNone(specs_not_profit)
        # self.assertEqual(len(specs_profit), 2)
        # self.assertEqual(len(specs_not_profit), 1)

        self.assertIn('proforma', res.context)
        proforma_result = res.context['proforma']
        self.assertEqual(proforma_result['cost'], 1016225963.20)

        self.assertEqual(round(proforma_result['profit'], 2), 143774036.80)
        self.assertEqual(round(proforma_result['percent'], 2), 14.15)
