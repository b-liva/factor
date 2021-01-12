from django.test import TestCase, Client
from request.tests.factory import factories as req_fact
from automation.helpers import helpers
from customer.tests.factory import factories as cu_factory

HAS_ATTR_MESSAGE = '{} should have an attribute {}'


class AutomationBase(TestCase):
    def setUp(self):
        self.client = Client()
        self.order = req_fact.RequestFactory.create()
        IMB3 = req_fact.ImTypeFactory.create(title='IMB3')
        IP55 = req_fact.IPTypeFactory.create(title='IP55')
        IC411 = req_fact.IcTypeFactory.create(title='IC411')
        IE1 = req_fact.IeTypeFactory.create(title='IE1')

        payload = {'voltage': 380, 'req_id': self.order, 'im': IMB3, 'ip': IP55, 'ic': IC411, 'ie': IE1}
        self.spec1 = req_fact.ReqSpecFactory.create(kw=132, rpm=1500, **payload)
        self.spec2 = req_fact.ReqSpecFactory.create(kw=18.5, rpm=1500, **payload)
        self.spec3 = req_fact.ReqSpecFactory.create(kw=18.5, rpm=750, **payload)
        self.proforma = req_fact.ProformaFactory.create(req_id=self.order)

    def assertHasAttr(self, obj, attr, message=None):
        if not hasattr(obj, attr):
            self.fail(HAS_ATTR_MESSAGE.format(obj, attr))


class AutomateOrderHelperTest(AutomationBase):
    def test_spec_not_routine(self):
        # res = helpers.spec_is_routine(self.spec3)
        res = self.spec3.spec_is_routine()
        self.assertFalse(res)

    def test_spec_is_routine_decimal(self):
        self.spec2.kw = 18.5
        self.spec2.save()
        # res = helpers.spec_is_routine(self.spec2)
        res = self.spec2.spec_is_routine()
        self.assertTrue(res)

    def test_spec_is_routine(self):
        self.spec2.kw = 132.0
        self.spec2.save()
        # res = helpers.spec_is_routine(self.spec2)
        res = self.spec2.spec_is_routine()
        self.assertTrue(res)

    def test_order_is_not_routine(self):
        res = self.order.order_is_routine()
        self.assertFalse(res)

    def test_order_is_not_routine_imb35(self):
        self.spec3.delete()

        im = req_fact.ImTypeFactory.create(title='IMB35')
        self.spec1.im = im
        self.spec1.save()
        res = self.order.order_is_routine()
        self.assertFalse(res)
        self.assertFalse(res)

    def test_order_is_not_routine_ip56(self):
        self.spec3.delete()

        ip = req_fact.IPTypeFactory.create(title='IP56')
        self.spec1.ip = ip
        self.spec1.save()
        res = self.order.order_is_routine()
        self.assertFalse(res)

    def test_order_is_not_routine_ic611(self):
        self.spec3.delete()

        ic = req_fact.IcTypeFactory.create(title='IC611')
        self.spec1.ic = ic
        self.spec1.save()
        res = self.order.order_is_routine()
        self.assertFalse(res)

    def test_order_is_not_routine_ie1(self):
        self.spec3.delete()

        ie = req_fact.IeTypeFactory.create(title='IE2')
        self.spec1.ie = ie
        self.spec1.save()
        res = self.order.order_is_routine()
        self.assertFalse(res)

    def test_order_is_routine(self):
        self.spec3.delete()
        res = self.order.order_is_routine()
        self.assertTrue(res)

    def test_generate_proforma_number(self):
        req_fact.ProformaFactory.create(number=9813255)
        req_fact.ProformaFactory.create(number=9813250)
        req_fact.ProformaFactory.create(number=9813200)
        res = helpers.generate_proforma_number()
        self.assertEqual(res, 9813255 + 1)

    def test_create_proforma_from_order(self):
        req_fact.ProformaFactory.create(number=9813255)
        req_fact.ProformaFactory.create(number=9813250)
        req_fact.ProformaFactory.create(number=9813200)
        res = helpers.create_proforma_from_order(self.order)
        self.assertEqual(res.number, 9813255 + 1)
        self.assertEqual(res.owner, self.order.owner)
        self.assertEqual(res.req_id, self.order)

    def test_create_proforma_specs(self):
        self.spec3.delete()
        helpers.create_proforma_specs(self.proforma)
        specs = self.proforma.prefspec_set.all()
        self.assertEqual(specs.count(), 2)
        self.assertEqual(132, specs[0].kw)

    def test_get_spec_price(self):
        res = self.spec1.get_spec_price()
        self.assertEqual(round(res, 2), 1580000000.00)

    def test_get_spec_price_400v(self):
        self.spec1.voltage = 400
        self.spec1.save()
        res = self.spec1.get_spec_price()
        self.assertEqual(round(res, 2), round(1580000000.00 * 1.1, 2))

    def test_get_spec_price_base(self):
        agent = cu_factory.CustomerFactory.create(agent=True)
        self.order.customer = agent
        self.order.save()

        res = self.spec1.get_spec_price()
        self.assertEqual(round(res, 2), 1410000000.00)
