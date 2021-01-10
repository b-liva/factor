from django.shortcuts import reverse
from rest_framework import status
from automation.tests.helpers.test_helpers import AutomationBase
from request.models import Xpref


class ProformaAutomation(AutomationBase):

    def test_redirect_req_report_if_order_not_routine(self):
        url = reverse('order_valid', kwargs={'request_pk': self.order.pk})
        response = self.client.get(url)
        proformas = Xpref.objects.filter(is_active=True)
        self.assertRedirects(
            response,
            expected_url=reverse('req_report'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_302_FOUND
        )
        self.assertEqual(proformas.count(), 1)

    def test_create_proforma_if_order_is_routine(self):
        self.spec3.delete()
        url = reverse('order_valid', kwargs={'request_pk': self.order.pk})
        response = self.client.get(url)
        proforma = self.order.xpref_set.order_by('pk').last()
        proformas = Xpref.objects.filter(is_active=True)
        self.assertRedirects(
            response,
            expected_url=reverse('pref_details', kwargs={'ypref_pk': proforma.pk}),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_302_FOUND
        )

        self.assertEqual(proformas.count(), 2)
