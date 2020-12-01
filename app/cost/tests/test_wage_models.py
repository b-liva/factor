from django.utils.translation import gettext as _
from django.contrib.auth.models import Permission
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from accounts.tests.test_public_funcs import CustomAPITestCase
from cost import models
from cost.models import WageCost

CREATE_WAGE_URL = reverse('cost:create_wage')


class CreateWage:

    def __init__(self, **kwargs):
        self.wage_payload = {
            'qty': 1,
            'price': 2500,
            'unit': ('machine', _('machine')),
        }

    def create_wage(self, **kwargs):
        return models.WageCost.objects.create(**kwargs)


class PublicWageAPITest(CustomAPITestCase):
    """Test the user API (public)"""

    def setUp(self):
        super().setUp()
        self.client_anon = APIClient()
        self.client.force_authenticate(user=self.user)
        self.client_exp = APIClient()
        self.client_exp.force_authenticate(user=self.ex_user)

        cw = CreateWage()
        self.wage_payload = cw.wage_payload
        self.wage_payload['owner'] = self.ex_user
        self.sample_wage = cw.create_wage(**self.wage_payload)

    def test_list_wage_unauthenticated(self):
        """Test that authentication is required for listing wage"""
        res = self.client_anon.get(CREATE_WAGE_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_wage_unauthenticated(self):
        """Test that authentication is required for creating wage"""
        res = self.client_anon.post(CREATE_WAGE_URL, self.wage_payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_wage_fail_unauthenticated(self):
        """Test that authentication is required for retrieving wage"""
        url = reverse('cost:manage_wage', kwargs={'pk': self.sample_wage.pk})
        res = self.client_anon.get(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_wage_fail_unauthenticated(self):
        """Test that anonymous user can't update wage"""
        self.wage_payload['qty'] = 5
        url = reverse('cost:manage_wage', kwargs={'pk': self.sample_wage.pk})
        res = self.client_anon.put(url, self.wage_payload)
        print(res.data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_wage_fail_unauthenticated(self):
        """Test that anonymous user can't update wage"""
        url = reverse('cost:manage_wage', kwargs={'pk': self.sample_wage.pk})
        res = self.client_anon.delete(url)
        exists = WageCost.objects.filter(pk=self.sample_wage.pk).exists()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(exists)


class PrivateWageAPITest(CustomAPITestCase):
    def setUp(self):
        super().setUp()
        self.client_anon = APIClient()
        self.client.force_authenticate(user=self.user)
        self.client_exp = APIClient()
        self.client_exp.force_authenticate(user=self.ex_user)
        self.client_superuser = APIClient()
        self.client_superuser.force_authenticate(user=self.superuser)

        cw = CreateWage()
        self.wage_payload = cw.wage_payload
        self.wage_payload['owner'] = self.ex_user
        self.sample_wage = cw.create_wage(**self.wage_payload)

    def test_create_wage_fails_unauthorized(self):
        """Test that authenticated user with no permission can't create wage(get)"""
        res = self.client.get(CREATE_WAGE_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_wage_post_fails_unauthorized(self):
        """Test that authenticated user with no permission can't create wage(post)"""
        self.wage_payload['owner'] = self.user.pk
        res = self.client.post(CREATE_WAGE_URL, self.wage_payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_wage_post_success(self):
        """Test that authorized user can create wage"""
        self.wage_payload['owner'] = self.ex_user.pk
        res = self.client_exp.post(CREATE_WAGE_URL, self.wage_payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['owner'], self.wage_payload['owner'])

    def test_retrieve_wage_fails_unauthorized(self):
        """Test that user with no permission can't retrieve wage"""

        url = reverse('cost:manage_wage', kwargs={'pk': self.sample_wage.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_wage_success(self):
        """Test that user with read permission can retrieve wage"""

        url = reverse('cost:manage_wage', kwargs={'pk': self.sample_wage.pk})
        res = self.client_exp.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_update_wage_fails_unauthorized(self):
        """Test that user with no permission can't update wage"""
        self.wage_payload['qty'] = 1233

        url = reverse('cost:manage_wage', kwargs={'pk': self.sample_wage.pk})
        res = self.client.put(url, self.wage_payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_wage_fails_unauthorized(self):
        """Test that user with no permission can't update wage"""
        url = reverse('cost:manage_wage', kwargs={'pk': self.sample_wage.pk})
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_wage_success(self):
        """Test that user with update permission can update wage"""
        url = reverse('cost:manage_wage', kwargs={'pk': self.sample_wage.pk})
        self.wage_payload['qty'] = 123
        res = self.client_exp.put(url, self.wage_payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['qty'], self.wage_payload['qty'])

    def test_delete_wage_success(self):
        """Test that user with delete permission can delete wage"""
        wage_pk = self.sample_wage.pk
        url = reverse('cost:manage_wage', kwargs={'pk': wage_pk})

        res = self.client_exp.delete(url)

        exists = WageCost.objects.filter(pk=wage_pk).exists()
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(exists)

    def test_retrieve_wage_obj_need_owner(self):
        """Test that user can't retrieve wage of other users"""
        self.user.user_permissions.add(
            Permission.objects.get(codename='read_wagecost', content_type__app_label='cost'),
        )
        url = reverse('cost:manage_wage', kwargs={'pk': self.sample_wage.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_wage_obj_need_owner(self):
        """Test that user can't update other users wages"""
        self.user.user_permissions.add(
            Permission.objects.get(codename='change_wagecost', content_type__app_label='cost')
        )
        url = reverse('cost:manage_wage', kwargs={'pk': self.sample_wage.pk})
        self.wage_payload['qty'] = 345
        res = self.client.put(url, self.wage_payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_wage_obj_need_owner(self):
        """Test that user can't delete other users wages"""
        self.user.user_permissions.add(
            Permission.objects.get(codename='delete_wagecost', content_type__app_label='cost')
        )
        url = reverse('cost:manage_wage', kwargs={'pk': self.sample_wage.pk})
        res = self.client.delete(url)
        exists = WageCost.objects.filter(pk=self.sample_wage.pk).exists()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(exists)
