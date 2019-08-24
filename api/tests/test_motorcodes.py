from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.shortcuts import reverse
from accounts.tests import test_public_funcs as funcs
from motordb.models import MotorsCode
from request.models import IMType, IPType, ICType, IEType

MOTORCODES_URL = reverse('apivs:motorscode-list')


class PublicMotorCodesTest(APITestCase):
    def setUp(self):
        """set up for public access"""
        self.user = funcs.sample_user(username='user', password='passowrd123')
        self.client = APIClient()
        self.motorcode = funcs.sample_motorcode(owner=self.user, code=9900, kw=450, speed=1500, voltage=380)

    def test_retrieve_motorcode_list_login_required(self):
        """Test accessing motor codes needs authentication"""
        res = self.client.get(MOTORCODES_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_motorcode_login_required(self):
        """Test retrieve a motor code need authentication"""
        res = self.client.get(reverse('apivs:motorscode-detail', args=[self.motorcode.pk]))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateMotorCodesTests(APITestCase):
    def setUp(self):
        """setup for private motorcodes access"""
        self.user = funcs.sample_user(username='user', password='password123')
        self.superuser = funcs.sample_superuser(username='superuser')
        self.ex_user = funcs.login_as_expert(username='ex_user')
        self.client = APIClient()
        self.motorcode = funcs.sample_motorcode(owner=self.user, code=9900, kw=450, speed=1500, voltage=380)
        self.im = IMType.objects.create(title='IMB3')
        self.ip = IPType.objects.create(title='IP55')
        self.ic = ICType.objects.create(title='IC411')
        self.ie = IEType.objects.create(title='IE1')
        self.payload = {
            'owner': self.user.pk,
            'code': 99009900,
            'kw': 132,
            'speed': 1500,
            'voltage': 380,
            'ip': self.ip.pk,
            'ic': self.ic.pk,
            'im': self.im.pk,
            'ie': self.ie.pk,
        }

    def test_create_motor_code_needs_permission_api(self):
        """Test creating motor codes needs permission (add_motorcode)"""
        self.client.force_authenticate(user=self.user)

        res = self.client.post(MOTORCODES_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_motor_code_successful(self):
        """Test create motorcode successful"""
        self.client.force_authenticate(user=self.ex_user)
        res = self.client.post(MOTORCODES_URL, self.payload)
        exist = MotorsCode.objects.filter(
            code=self.payload['code'],
            kw=self.payload['kw'],
            speed=self.payload['speed'],
            voltage=self.payload['voltage'],
            ip=self.payload['ip'],
            ic=self.payload['ic'],
            im=self.payload['im'],
            ie=self.payload['ie'],
        ).exists()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['code'], str(self.payload['code']))
        self.assertEqual(res.data['owner'], self.ex_user.pk)
        self.assertTrue(exist)

    def test_retrieve_motor_codes_list_need_permission_api(self):
        """Test retrieving motor codes list needs permission (list_motorscode)"""
        self.client.force_authenticate(user=self.user)
        res = self.client.get(MOTORCODES_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_motor_codes_list_not_limited_by_user_api(self):
        """Test retrieving motor codes list successful"""
        self.client.force_authenticate(user=self.ex_user)
        funcs.sample_motorcode(owner=self.ex_user, code=235435, kw=132, speed=1500, voltage=380)
        funcs.sample_motorcode(owner=self.ex_user, code=1435, kw=160, speed=1500, voltage=380)
        funcs.sample_motorcode(owner=self.user, code=25435, kw=355, speed=3000, voltage=400)
        res = self.client.get(MOTORCODES_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 4)
        # todo: sorting needs to be done.
        # ....

    def test_retrieve_motor_code_needs_permission_api(self):
        """Test retrieve motor code needs permission"""
        self.client.force_authenticate(user=self.user)
        res = self.client.get(reverse('apivs:motorscode-detail', args=[self.motorcode.pk]))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_motor_code_not_limited_by_user_api(self):
        """Test retrieve motor code successful"""
        self.client.force_authenticate(user=self.ex_user)
        res = self.client.get(reverse('apivs:motorscode-detail', args=[self.motorcode.pk]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['code'], str(self.motorcode.code))

    def test_update_motor_code_needs_permission(self):
        """Test updating a motor code need permission(change_motorscode)"""
        self.client.force_authenticate(user=self.user)
        payload = {
            'code': 55222,
        }
        res = self.client.patch(reverse('apivs:motorscode-detail', args=[self.motorcode.pk]), payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_motor_code_not_limited_by_user(self):
        """Test update a motor code"""
        self.client.force_authenticate(user=self.ex_user)
        payload = {
            'code': 2345,
        }
        res = self.client.patch(reverse('apivs:motorscode-detail', args=[self.motorcode.pk]), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['code'], str(payload['code']))

    def test_delete_motor_code_needs_permissions(self):
        """Test deleting a motor code needs permission(delete_motorscode)"""
        self.client.force_authenticate(user=self.user)
        res = self.client.delete(reverse('apivs:motorscode-detail', args=[self.motorcode.pk]))
        exist = MotorsCode.objects.filter(pk=self.motorcode.pk).exists()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(exist)

    def test_delete_motor_code_not_limited_by_user(self):
        """Test delete a motor code"""
        self.client.force_authenticate(user=self.ex_user)
        res = self.client.delete(reverse('apivs:motorscode-detail', args=[self.motorcode.pk]))
        exist = MotorsCode.objects.filter(pk=self.motorcode.pk).exists()
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(exist)
