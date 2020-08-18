from django.shortcuts import reverse
from django.conf import settings
from rest_framework import status
from accounts.tests.test_public_funcs import CustomAPITestCase
from request.models import Payment, Xpref


class PublicPaymentTests(CustomAPITestCase):
    def test_create_payments_login_required(self):
        res = self.client.get(reverse('pay_form'))
        self.assertRedirects(
            res,
            expected_url=settings.LOGIN_URL + '?next=' + reverse('pay_form'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )


class PrivatePaymentTests(CustomAPITestCase):
    # PAYMENT
    # CREATE
    def test_create_payment_get_needs_permission(self):
        """Test create payment getting form needs permission"""
        self.client.force_login(user=self.user)
        res = self.client.get(reverse('pay_form'))

        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_create_payment_post_needs_permission(self):
        """Test create payments posing data needs permission"""
        self.client.force_login(user=self.user)
        res = self.client.get(reverse('pay_form'), self.payment_payload)
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_create_payment_post_limited_by_user(self):
        """Test create Payment posting data limited by user."""
        self.client.force_login(user=self.ex_user)
        res = self.client.post(reverse('pay_form'), self.payment_payload)
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_create_payment_get_successful(self):
        """Test create Payment"""
        self.client.force_login(user=self.ex_user)
        res = self.client.get(reverse('pay_form'))
        payments = Payment.objects.filter(is_active=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.context['xpayments']), len(payments))

    def test_create_payment_post_fail_perm_is_false(self):
        """Test create payment post data will fail if it is not a perm"""
        self.client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=160, rpm=3000)
        proforma = self.sample_proforma(req=req, owner=self.ex_user, number=384985)

        self.payment_payload.update({
            'xpref_id': proforma.pk,
        })
        res = self.client.post(reverse('pay_form'), self.payment_payload)
        exist = Payment.objects.filter(
            amount=self.payment_payload['amount'],
            number=self.payment_payload['number']
        ).exists()
        self.assertFalse(proforma.perm)
        self.assertFalse(exist)
        # self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertRedirects(
            res,
            expected_url=reverse('pref_details', args=[proforma.pk]),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )

    def test_create_payment_post_successful(self):
        """Test create payment post data success."""
        self.client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=160, rpm=3000)
        proforma = self.sample_proforma(req=req, owner=self.ex_user, number=38498598, perm=True)

        self.payment_payload.update({
            'xpref_id': proforma.pk,
        })
        res = self.client.post(reverse('pay_form'), self.payment_payload)
        exist = Payment.objects.filter(
            number=self.payment_payload['number'],
            amount=self.payment_payload['amount'],
        ).exists()
        self.assertTrue(proforma.perm)
        self.assertTrue(exist)
        self.assertRedirects(
            res,
            expected_url=reverse('payment_index'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_create_payment_post_no_proforma_fail(self):
        """Test payment creation fails if no proforma is added."""
        self.client.force_login(user=self.ex_user)
        exist = Xpref.objects.filter(pk=1050).exists()
        self.payment_payload.update({'xpref_id': 1050})
        res = self.client.post(reverse('pay_form'), self.payment_payload)
        self.assertTrue(res.context['form'].errors)
        self.assertFalse(exist)

    # List
    # Retrieve
    def test_retrieve_payment_needs_permission(self):
        """Test retrieving payment needs permission"""
        self.client.force_login(user=self.user)
        res = self.client.get(reverse('payment_details', args=[self.payment.pk]))
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )

    def test_retrieve_payment_limited_by_user(self):
        """Test retrieving payment is limited by user"""
        self.client.force_login(user=self.ex_user)
        res = self.client.get(reverse('payment_details', args=[self.payment.pk]))
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK
        )

    def test_retrieve_payment_success(self):
        """Test retrieving payment needs permission"""
        self.client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, number=987643)

        self.sample_reqspec(owner=self.ex_user, kw=550, rpm=1000)
        self.sample_reqspec(owner=self.ex_user, kw=355, rpm=1500)
        proforma = self.sample_proforma(req=req, owner=self.ex_user, number=983424)
        payment = self.sample_payment(proforma=proforma, owner=self.ex_user, number=5145, amount=25000000)
        res = self.client.get(reverse('payment_details', args=[payment.pk]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.context['payment'].pk, payment.pk)

    # Update
    def test_update_payment_get_needs_permission(self):
        """Test update payment getting form needs permision"""
        self.client.force_login(user=self.user)
        res = self.client.get(reverse('payment_edit', args=[self.payment.pk]))
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_update_payment_post_needs_permission(self):
        """Test update payment posting data needs permision"""
        self.client.force_login(user=self.user)
        res = self.client.post(reverse('payment_edit', args=[self.payment.pk]), self.payment_payload)
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_update_payment_get_limited_by_owner(self):
        """Test update payment getting form limited to owner or super user"""
        self.client.force_login(user=self.ex_user)
        res = self.client.post(reverse('payment_edit', args=[self.payment.pk]), self.payment_payload)
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_update_payment_post_limited_by_owner(self):
        """Test update payment posting data limited to owner or super user"""
        self.client.force_login(user=self.ex_user)
        res = self.client.post(reverse('payment_edit', args=[self.payment.pk]), self.payment_payload)
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_update_payment_get_successful(self):
        """Test update payment getting form successfully"""
        self.client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, number=987643)

        self.sample_reqspec(owner=self.ex_user, kw=550, rpm=1000)
        self.sample_reqspec(owner=self.ex_user, kw=355, rpm=1500)
        proforma = self.sample_proforma(req=req, owner=self.ex_user, number=983424)
        payment = self.sample_payment(proforma=proforma, owner=self.ex_user, number=51459878, amount=25000000)
        res = self.client.get(reverse('payment_edit', args=[payment.pk]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_payment_post_successful(self):
        """Test update payment posting data successfully"""
        self.client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, number=987643)

        self.sample_reqspec(owner=self.ex_user, kw=550, rpm=1000)
        self.sample_reqspec(owner=self.ex_user, kw=355, rpm=1500)
        proforma = self.sample_proforma(req=req, owner=self.ex_user, number=983424)
        payment = self.sample_payment(proforma=proforma, owner=self.ex_user, number=5145, amount=25000000)
        self.payment_payload.update({
            'xpref_id': proforma.pk,
        })
        res = self.client.post(reverse('payment_edit', args=[payment.pk]), self.payment_payload)
        pay_retreived = Payment.objects.get(pk=payment.pk)
        self.assertRedirects(
            res,
            expected_url=reverse('payment_index'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )
        self.assertEqual(self.payment_payload['xpref_id'], pay_retreived.pk)
        self.assertEqual(self.payment_payload['amount'], pay_retreived.amount)
        self.assertEqual(self.payment_payload['number'], pay_retreived.number)
        # self.assertEqual(self.payment_payload['date_fa'], str(pay_retreived.date_fa))
        self.assertEqual(self.payment_payload['summary'], pay_retreived.summary)

    # Delete
    def test_delete_payment_get_needs_permission(self):
        """Test delete payment getting page needs permission"""
        self.client.force_login(user=self.user)
        res = self.client.get(reverse('payment_delete', args=[self.payment.pk]))
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_delete_payment_needs_permission(self):
        """Test delete payment needs permission"""
        self.client.force_login(user=self.user)
        res = self.client.delete(reverse('payment_delete', args=[self.payment.pk]))
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_delete_payment_get_limited_by_owner(self):
        """Test delete payment getting page limited by owner"""
        self.client.force_login(user=self.ex_user)
        res = self.client.delete(reverse('payment_delete', args=[self.payment.pk]))
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )

    def test_delete_payment_limited_by_owner(self):
        """Test delete payment limited by owner"""
        self.client.force_login(user=self.ex_user)
        res = self.client.delete(reverse('payment_delete', args=[self.payment.pk]))
        self.assertRedirects(
            res,
            expected_url=reverse('errorpage'),
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
        )
