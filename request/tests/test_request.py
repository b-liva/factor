from django.shortcuts import reverse
from django.conf import settings
from django.http.cookie import SimpleCookie
from rest_framework import status
from accounts.tests.test_public_funcs import CustomAPITestCase
from request.models import ReqSpec, Requests


class PublicRequestTests(CustomAPITestCase):
    def setUp(self):
        super().setUp()

    def test_login_required(self):
        """Test request crud operations need authentication: entering request urls needs authentication"""
        res = self.client.get(reverse('req_form'))
        self.assertRedirects(
            res,
            expected_url=settings.LOGIN_URL + '?next=' + reverse('req_form'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_create_reqpart_get_login_required(self):
        """Test getting request part creation form need authentication"""
        res = self.client.get(reverse('part_form', args=[self.req.pk]))
        self.assertRedirects(
            res,
            expected_url=settings.LOGIN_URL + '?next=' + reverse('part_form', args=[self.req.pk]),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )


class PrivateRequestTests(CustomAPITestCase):
    def setUp(self):
        super().setUp()

    def test_create_request_needs_permission(self):
        """Test creating request needs permission(add_requests)"""
        self.client.force_login(user=self.user)
        res = self.client.get(reverse('req_form'))
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_create_request_get_page_success(self):
        """Test create request successful"""
        self.client.force_login(user=self.ex_user)
        res = self.client.get(reverse('req_form'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.context['add_new'])

    def test_create_request_post_needs_permission(self):
        """Test sending post requests needs permission(add_requests)"""
        self.client.force_login(user=self.user)
        payload = {
            'number': 54652,
            'date_fa': "1398-05-06",
        }
        self.client.cookies.update(SimpleCookie({'customer': self.customer.pk}))
        res = self.client.post(reverse('req_form'), payload)
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_create_request_post_data_success(self):
        """Test create request post data success"""
        self.client.force_login(user=self.ex_user)
        payload = {
            'number': 98774455,
            "date_fa": "1398-05-06",
        }
        self.client.cookies.update(SimpleCookie({'customer': self.customer.pk}))

        res = self.client.post(reverse('req_form'), payload)
        req_id = res.url.split('/')[2]
        self.assertRedirects(
            res,
            expected_url=reverse('spec_form', args=[req_id]),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_create_reqspec_get_form_form_needs_permission(self):
        """Test create reqspec, getting form page needs permission"""
        self.client.force_login(user=self.user)
        res = self.client.get(reverse('spec_form', args=[self.req.pk]))

        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_create_reqspec_get_form_limited_to_owner(self):
        """Test reqspec form limited to req owners"""
        self.client.force_login(user=self.ex_user)
        res = self.client.get(reverse('spec_form', args=[self.req.pk]))
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_create_reqspec_get_form_success(self):
        """Test reqspec form limited to req owners
        :return {
        'form': form,
        'req_obj': req,
        'specs': specs,
        'list': list,
        }
        """
        self.client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, number=87463)
        res = self.client.get(reverse('spec_form', args=[req.pk]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.context['req_obj'].pk, req.pk)
        self.assertEqual(len(res.context['specs']), len(req.reqspec_set.filter(is_active=True)))

    def test_create_reqspec_post_need_permission(self):
        """Test posting data to reqspec form needs permission"""
        self.client.force_login(user=self.user)

        res = self.client.post(reverse('spec_form', args=[self.req.pk]), self.reqspec_payload)
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_create_reqspec_post_data_limited_to_owner(self):
        """Test posting data by reqspec form limited by request owner"""
        self.client.force_login(user=self.ex_user)
        res = self.client.post(reverse('spec_form', args=[self.req.pk]))
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_create_reqspec_post_data_success(self):
        """Test posting data from reqspec form successfully"""
        self.client.force_login(user=self.ex_user)

        req = self.sample_request(owner=self.ex_user, number=8834)
        count_before = req.reqspec_set.filter(is_active=True).count()
        res = self.client.post(reverse('spec_form', args=[req.pk]), self.reqspec_payload)
        count_after = req.reqspec_set.filter(is_active=True).count()
        print('res : ', res.context)
        self.assertRedirects(
            res,
            expected_url=reverse('spec_form', args=[req.pk]),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )
        self.assertEqual(count_after, count_before + 1)
        reqspec = ReqSpec.objects.last()
        self.assertEqual(reqspec.kw, self.reqspec_payload['kw'])
        self.assertEqual(reqspec.rpm_new.pk, self.reqspec_payload['rpm_new'])
        self.assertEqual(reqspec.voltage, self.reqspec_payload['voltage'])

    def test_retrieve_request_list(self):
        """Test private list requests: superuser sees all, experts sees themselves"""
        req1 = self.sample_request(owner=self.user, number=1324580)
        req2 = self.sample_request(owner=self.user, number=132458)
        # todo: This route is not being used.
        self.client.force_login(user=self.ex_user)
        req3 = self.sample_request(owner=self.ex_user, number=13245)
        res = self.client.get(reverse('request_index'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.context['all_requests']), 1)

        self.client.force_login(user=self.superuser)
        superuser_res = self.client.get(reverse('request_index'))
        self.assertEqual(superuser_res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(superuser_res.context['all_requests']), 4)

    def test_retrieve_request_report_page_needs_permission(self):
        """Test retrieving request list needs permission"""
        self.client.force_login(user=self.user)
        res = self.client.get(reverse('req_report'))
        self.assertEqual(res.status_code, status.HTTP_302_FOUND)

    def test_retrieve_request_report_page_limited_by_owner(self):
        """Test owners see their list of their requests only"""
        self.client.force_login(user=self.ex_user)
        self.sample_request(owner=self.user, number=9876)
        self.sample_request(owner=self.ex_user, number=9877)
        self.sample_request(owner=self.ex_user, number=9879, is_active=False)
        self.sample_request(owner=self.ex_user, number=9878)
        res = self.client.get(reverse('req_report'))
        reqs = Requests.objects.filter(owner=self.ex_user, is_active=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.context['req_page']), len(reqs))

    def test_request_report_pagination(self):
        """Test request report page pagination"""
        # todo: should be implemented.
        implemented = False
        self.assertTrue(implemented)

    def test_retrieve_request_superuser_success(self):
        """Test superuser can see all requests"""
        req1 = self.sample_request(number=1545, owner=self.ex_user, customer=self.customer)
        req2 = self.sample_request(number=15455, owner=self.superuser, customer=self.customer)
        req3 = self.sample_request(number=1645, owner=self.user, customer=self.customer)

        self.client.force_login(user=self.superuser)
        response = self.client.get(reverse('request_details', args=[req1.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse('request_details', args=[req3.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_request_needs_permission(self):
        """Test retrieving request needs permision(add_requests)"""
        self.client.force_login(user=self.user)
        res = self.client.get(reverse('request_details', args=[self.req.pk]))
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_retrieve_request_owner_success(self):
        """Test success can retrieve own request details"""
        self.client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, number=985344)
        res = self.client.get(reverse('request_details', args=[req.pk]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.context['request'].number, req.number)

    def test_retrieve_request_details_not_found(self):
        """Test retrieving non-existing request redirects to error page"""
        self.client.force_login(user=self.ex_user)
        exist = Requests.objects.filter(pk=99999).exists()
        res = self.client.get(reverse('request_details', args=[99999]))
        self.assertFalse(exist)
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_retrieve_request_details_limited_by_owner(self):
        """Test users can't see other users requests"""
        self.client.force_login(user=self.ex_user)
        res = self.client.get(reverse('request_details', args=[self.req.pk]))
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

# ReqPart
    def test_create_reqpart_get_needs_permission(self):
        """Test getting reqpart creation form needs permission"""
        self.client.force_login(user=self.user)
        res = self.client.get(reverse('part_form', args=[self.req.pk]))
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_create_reqpart_post_needs_permission(self):
        """Test getting reqpart creation form needs permission"""
        self.client.force_login(user=self.user)
        payload = {'qty': 3, 'title': 'براکت جلو'}
        res = self.client.post(reverse('part_form', args=[self.req.pk]), payload)
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_create_reqpart_get_limited_to_owner(self):
        """Test users can get reqpart create form if they are owner of request."""
        self.client.force_login(user=self.ex_user)
        res = self.client.get(reverse('part_form', args=[self.req.pk]))
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )

    def test_create_reqpart_post_limited_to_owner(self):
        """Test users can post reqpart if they are owner of request."""
        self.client.force_login(user=self.ex_user)
        payload = {'qty': 3, 'title': 'براکت جلو'}
        res = self.client.post(reverse('part_form', args=[self.req.pk]), payload)
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )

    def test_create_reqpart_get_success(self):
        """Test users get reqpart create form if they are owner or request."""
        self.client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, number=98734)
        res = self.client.get(reverse('part_form', args=[req.pk]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_reqpart_post_success(self):
        """Test create req part post success"""
        self.client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, number=98734)
        payload = {'qty': 3, 'title': 'براکت جلو'}
        res = self.client.post(reverse('part_form', args=[req.pk]), payload)
        print(res)
        parts = req.reqpart_set.all()
        self.assertRedirects(
            res,
            expected_url=reverse('part_form', args=[req.pk]),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )
        self.assertEqual(parts.count(), 1)
        self.assertEqual(parts.last().qty, payload['qty'])
