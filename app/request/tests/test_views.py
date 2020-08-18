from django.test import TestCase, Client
from django.shortcuts import reverse
from rest_framework import status
from django.conf import settings

from accounts.tests.test_public_funcs import CustomAPITestCase

from request.models import Requests


class PublicRequestViewsTests(CustomAPITestCase):

    def test_request_list_view(self):
        """Test Login required to see list of requests."""
        response = self.client.get(reverse('request_index'))

        self.assertRedirects(
            response,
            expected_url=settings.LOGIN_URL + '?next=' + reverse('request_index'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )


class PrivateCustomerViewsTest(CustomAPITestCase):
    """Tests Request privately avaible"""



