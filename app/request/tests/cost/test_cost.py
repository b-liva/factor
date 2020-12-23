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
from request.helpers import helpers

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

    def prepare_prof_routine_not_routine_specs(self):
        import jdatetime
        date = jdatetime.date(year=1399, month=7, day=15)
        #         # date = date.togregorian()

        self.proforma.date_fa = date
        self.proforma.save()

        factories.ProformaSpecFactory.create(xpref_id=self.proforma, price=160000000, kw=18.5, rpm=3000)
        factories.ProformaSpecFactory.create(xpref_id=self.proforma, price=160000000, kw=2500, rpm=3000)

    def test_prevents_user_with_no_permission_to_get_proforma_profit(self):
        self.client.force_login(self.user)
        url = reverse('prof_profit', kwargs={'ypref_pk': self.proforma.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_get_proforma_profit(self):
        self.client.force_login(self.superuser)

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

    def test_save_data_to_cache(self):
        pass

    def test_get_data_from_cache(self):
        pass

    def test_calculate_proforma_profit(self):
        self.client.force_login(self.superuser)

        self.prepare_prof_routine_not_routine_specs()
        url = reverse('prof_profit', kwargs={'ypref_pk': self.proforma.pk})
        res = self.client.get(url)

        self.assertIn('proforma', res.context)
        proforma_result = res.context['proforma']
        self.assertEqual(proforma_result['cost'], 1009281963.20)

        self.assertEqual(round(proforma_result['profit'], 2), 150718036.80)
        self.assertEqual(round(proforma_result['percent'], 2), 14.93)

    def test_proforma_profit_path_with_specs(self):
        self.client.force_login(self.superuser)
        self.prepare_prof_routine_not_routine_specs()

        url = reverse('prof_profit', kwargs={'ypref_pk': self.proforma.pk})
        res = self.client.get(url)

        self.assertIn('specs', res.context)
        self.assertTrue(type(res.context['specs']), dict())

        self.assertIn('pspecs_with_profit', res.context['specs'])
        self.assertIn('pspecs_no_profit', res.context['specs'])
        specs_profit = res.context['specs']['pspecs_with_profit']
        specs_not_profit = res.context['specs']['pspecs_no_profit']
        kw18 = kw132 = None

        for sp in specs_profit:
            if round(sp['power']) == 132:
                kw132 = sp
            elif round(sp['power'], 1) == 18.5:
                kw18 = sp
        for sp in specs_not_profit:
            print('not profit: ', sp)
        self.assertEqual(kw132['power'], 132)
        self.assertEqual(round(kw132['profit'], 1), 120533012.00)
        self.assertEqual(round(kw132['percent'], 2), 13.71)
        self.assertEqual(round(kw18['power'], 1), 18.5)
        self.assertEqual(round(kw18['profit'], 1), 30185024.80)
        self.assertEqual(round(kw18['percent'], 2),  23.25)
        self.assertEqual(len(specs_profit), 2)
        self.assertEqual(len(specs_not_profit), 1)

    def test_proforma_profit_path_context_has_proforma_object(self):
        self.client.force_login(self.superuser)
        self.prepare_prof_routine_not_routine_specs()

        url = reverse('prof_profit', kwargs={'ypref_pk': self.proforma.pk})
        res = self.client.get(url)

        self.assertIn('prof', res.context)
        self.assertEqual(res.context['prof'].pk, self.proforma.pk)

    def test_proforma_profit_path_context_has_file_date(self):
        cost_file_name = "20201002"
        cost_file_date_fa = helpers.get_date_fa_from_file_name(cost_file_name)
        self.client.force_login(self.superuser)
        self.prepare_prof_routine_not_routine_specs()

        url = reverse('prof_profit', kwargs={'ypref_pk': self.proforma.pk})
        res = self.client.get(url)

        self.assertIn('cost_file', res.context)
        self.assertIn('name', res.context['cost_file'])
        self.assertIn('date_fa', res.context['cost_file'])
        self.assertEqual(res.context['cost_file']['name'], cost_file_name)
        self.assertEqual(res.context['cost_file']['date_fa'], cost_file_date_fa)
