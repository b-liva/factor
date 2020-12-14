from django.shortcuts import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.conf import settings
from accounts.tests.test_public_funcs import CustomAPITestCase
from core.tests.factory import factories as core_factories


class TestPublicCost(CustomAPITestCase):

    def setUp(self):
        super().setUp()
        self.client_anon = APIClient()

    def test_prevents_unauth_user_to_get_proforma_profit(self):
        url = reverse('proforma_profit2', kwargs={'ypref_pk': self.proforma.pk})
        res = self.client_anon.get(url)
        self.assertRedirects(
            res,
            expected_url=settings.LOGIN_URL + '?next=' + reverse('proforma_profit2', kwargs={'ypref_pk': self.proforma.pk}),
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

    def test_prevents_user_with_no_permission_to_get_proforma_profit(self):
        self.client.force_login(self.user)
        url = reverse('proforma_profit2', kwargs={'ypref_pk': self.proforma.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_get_proforma_profit(self):
        self.client.force_login(self.superuser)
        url = reverse('proforma_profit2', kwargs={'ypref_pk': self.proforma.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(
            res,
            expected_url=reverse('default_cost', kwargs={'ypref_pk': self.proforma.pk}),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_302_FOUND
        )
