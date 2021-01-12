import jdatetime
from django.shortcuts import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.conf import settings
from accounts.tests.test_public_funcs import CustomAPITestCase
from core.date import Date
from request.models import Xpref, PrefSpec
from request.tests.factory import factories
from request.tests.factory.base_proformas import BaseProformaFactories


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

    def test_prevent_unauth_user_total_profit(self):
        url = reverse('total_profit')
        res = self.client_anon.get(url)
        self.assertRedirects(
            res,
            expected_url=settings.LOGIN_URL + '?next=' + url,
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )


class PrivateTestCost(CustomAPITestCase):

    def setUp(self):
        super().setUp()
        self.client_exp = APIClient()
        # self.ex_user = core_factories.create_user()
        # self.ex_user = core_factories.add_user_to_groupe(self.ex_user)
        self.client_exp.force_login(user=self.ex_user)

        self.proforma = factories.ProformaFactory.create()
        factories.ProformaSpecFactory.create(xpref_id=self.proforma, qty=1, price=1000000000, kw=132, rpm=1500)

    def prepare_prof_routine_not_routine_specs(self):
        import jdatetime
        date = jdatetime.date(year=1399, month=7, day=15)
        #         # date = date.togregorian()

        self.proforma.date_fa = date
        self.proforma.save()

        factories.ProformaSpecFactory.create(xpref_id=self.proforma, qty=1, price=160000000, kw=18.5, rpm=3000)
        factories.ProformaSpecFactory.create(xpref_id=self.proforma, qty=1, price=160000000, kw=2500, rpm=3000)

    def test_prevents_user_with_no_permission_to_get_proforma_profit(self):
        self.client.force_login(self.user)
        url = reverse('prof_profit', kwargs={'ypref_pk': self.proforma.pk})
        res = self.client.get(url)
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )

    def test_superuser_get_proforma_profit(self):
        self.client.force_login(self.ex_user)

        url = reverse('prof_profit', kwargs={'ypref_pk': self.proforma.pk})
        res = self.client.get(url)
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )

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
        self.assertEqual(kw132['power'], 132)
        self.assertEqual(round(kw132['profit'], 1), 120533012.00)
        self.assertEqual(round(kw132['percent'], 2), 13.71)
        self.assertEqual(round(kw18['power'], 1), 18.5)
        self.assertEqual(round(kw18['profit'], 1), 30185024.80)
        self.assertEqual(round(kw18['percent'], 2), 23.25)
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
        cost_file_date_fa = Date.get_date_fa_from_file_name(cost_file_name)
        self.client.force_login(self.superuser)
        self.prepare_prof_routine_not_routine_specs()

        url = reverse('prof_profit', kwargs={'ypref_pk': self.proforma.pk})
        res = self.client.get(url)

        self.assertIn('cost_file', res.context)
        self.assertIn('name', res.context['cost_file'])
        self.assertIn('date_fa', res.context['cost_file'])
        self.assertEqual(res.context['cost_file']['name'], cost_file_name)
        self.assertEqual(res.context['cost_file']['date_fa'], cost_file_date_fa)

    def test_prof_profit_post_discount(self):
        self.client.force_login(self.superuser)
        prof = factories.ProformaFactory.create(number=153)
        factories.ProformaSpecFactory.create(xpref_id=prof, price=1000000000, kw=132, rpm=1500, qty=3)
        factories.ProformaSpecFactory.create(xpref_id=prof, price=500000000, kw=90, rpm=1500, qty=2)
        url = reverse('prof_profit', kwargs={'ypref_pk': prof.pk})
        post_data = {
            'un90_disc': 10,
            'up90_disc': 15
        }
        res = self.client.post(url, data=post_data)
        discount = {
            'lte__90': 10,
            'gt__90': 15,
        }
        self.assertIn('discount', res.context)
        self.assertDictEqual(res.context['discount'], discount)
        self.assertEqual(res.context['proforma']['price'], 3450000000)

    def test_materials_cost_for_prof_profit(self):
        self.client.force_login(self.superuser)
        url = reverse('prof_profit', kwargs={'ypref_pk': self.proforma.pk})
        res = self.client.get(url)
        self.assertIn('material_cost', res.context)
        self.assertEqual(res.context['material_cost']['silicon'], 330000)
        self.assertEqual(res.context['material_cost']['cu'], 2100000)
        self.assertEqual(res.context['material_cost']['dicast'], 220000)
        self.assertEqual(res.context['material_cost']['steel'], 150000)
        self.assertEqual(res.context['material_cost']['alu'], 500000)

    def test_adjust_materials_cost_prof_profit_post(self):
        self.client.force_login(self.superuser)
        self.prepare_prof_routine_not_routine_specs()
        discount_payload = {
            'lte__90': 0,
            'gt__90': 0,
        }
        materials_payload = {
            "silicon": "300,000",
            "cu": "210,000,0",
            "alu": "500,000",
            "steel": "150,000",
            "dicast": "220,000",
        }
        materials_payload = {
            "silicon": 300000,
            "cu": 2100000,
            "alu": 500000,
            "steel": 150000,
            "dicast": 220000,
        }
        payload = dict()
        payload.update(discount_payload)
        payload.update(materials_payload)

        url = reverse('prof_profit', kwargs={'ypref_pk': self.proforma.pk})
        res = self.client.post(url, data=payload)

        self.assertDictEqual(res.context['material_cost'], materials_payload)

        specs_profit = res.context['specs']['pspecs_with_profit']
        specs_not_profit = res.context['specs']['pspecs_no_profit']
        kw18 = kw132 = None

        for sp in specs_profit:
            if round(sp['power']) == 132:
                kw132 = sp
            elif round(sp['power'], 1) == 18.5:
                kw18 = sp
        self.assertEqual(kw132['power'], 132)
        self.assertEqual(round(kw132['profit'], 1), 146069012.00)
        self.assertEqual(round(kw132['percent'], 2), 17.11)
        self.assertEqual(round(kw18['power'], 1), 18.5)
        self.assertEqual(round(kw18['profit'], 1), 33410624.80)
        self.assertEqual(round(kw18['percent'], 2), 26.39)
        self.assertEqual(len(specs_profit), 2)
        self.assertEqual(len(specs_not_profit), 1)

    def test_current_profit_sets_today_in_session(self):
        self.client.force_login(self.superuser)

        today = jdatetime.date.today()

        url = reverse('current_profit', kwargs={'ypref_pk': self.proforma.pk})
        response = self.client.get(url)
        self.assertEqual(
            self.client.session.get('current_profit_date'),
            str(today)
        )
        self.assertRedirects(
            response=response,
            expected_url=reverse('prof_profit', kwargs={'ypref_pk': self.proforma.pk}),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )

    def test_current_profit_picks_today_date(self):
        self.client.force_login(self.superuser)

        prof_date = jdatetime.date(year=1399, month=3, day=6)  # file: 1399-02-14:20200503
        self.proforma.date_fa = prof_date
        self.proforma.save()

        today = jdatetime.date.today()

        session = self.client.session
        session.update({
            'current_profit_date': str(today),
        })
        session.save()

        url = reverse('prof_profit', kwargs={'ypref_pk': self.proforma.pk})
        response = self.client.get(url)
        self.assertEqual(response.context['prof'].date_fa, self.proforma.date_fa)
        self.assertNotIn('current_profit_date', self.client.session)
        self.assertEqual(response.context['prof'], self.proforma)
        self.assertEqual(response.context['cost_file']['name'], "20201102")

    def test_total_profit_fails_no_permission(self):
        url = reverse('total_profit')
        self.client.force_login(self.user)
        res = self.client.get(url)
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )

    def test_total_profit_fails_with_exp_user(self):
        self.client.force_login(self.ex_user)
        url = reverse('total_profit')
        res = self.client.get(url)
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )

    def test_total_profit_success_with_superuser(self):
        self.client.force_login(self.superuser)
        url = reverse('total_profit')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_perms(self):
        self.client.force_login(self.superuser)
        PrefSpec.objects.all().delete()
        Xpref.objects.all().delete()

        BaseProformaFactories().base_proformas()

        url = reverse('total_profit')
        response = self.client.get(url)
        self.assertEqual(response.context['proforma_count'], 0)
        self.assertEqual(round(response.context['cost'], 2), 0)
        self.assertEqual(round(response.context['price'], 2), 0)
        self.assertEqual(round(response.context['profit'], 2), 0)
        self.assertEqual(response.context['percent'], None)

    def test_total_profit(self):
        self.client.force_login(self.superuser)
        PrefSpec.objects.all().delete()
        Xpref.objects.all().delete()

        BaseProformaFactories().base_proformas()
        Xpref.objects.update(perm=True)

        prof1 = factories.ProformaFactory.create(number=155)
        date_str = '20201014'
        date = Date.get_date_from_date_str(date_str)
        date_fa = jdatetime.date.fromgregorian(date=date, locale='fa_IR')
        prof1.date_fa = date_fa
        prof1.perm = False
        prof1.save()
        factories.ProformaSpecFactory.create(xpref_id=prof1, price=160000000, kw=18.5, rpm=3000, qty=1)
        factories.ProformaSpecFactory.create(xpref_id=prof1, price=1000000000, kw=132, rpm=1500, qty=2)

        url = reverse('total_profit')
        response = self.client.get(url)
        self.assertIn('cost', response.context)
        self.assertIn('price', response.context)
        self.assertIn('profit', response.context)
        self.assertIn('percent', response.context)

        self.assertEqual(response.context['proforma_count'], 3)
        self.assertEqual(round(response.context['cost'], 2), 4784590556.00)
        self.assertEqual(round(response.context['price'], 2), 5400000000.00)
        self.assertEqual(round(response.context['profit'], 2), 615409444.00)
        self.assertEqual(round(response.context['percent'], 2), 12.86)
