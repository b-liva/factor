from django.test import TestCase, Client
from request.tests.factory import factories as req_fact
from automation.helpers import helpers

HAS_ATTR_MESSAGE = '{} should have an attribute {}'


class AutomationBase(TestCase):
    def setUp(self):
        self.client = Client()
        self.order = req_fact.RequestFactory.create()
        self.spec1 = req_fact.ReqSpecFactory.create(kw=132, rpm=1500, voltage=380, req_id=self.order)
        self.spec2 = req_fact.ReqSpecFactory.create(kw=18.5, rpm=1500, voltage=380, req_id=self.order)
        self.spec3 = req_fact.ReqSpecFactory.create(kw=18.5, rpm=750, voltage=380, req_id=self.order)

    def assertHasAttr(self, obj, attr, message=None):
        if not hasattr(obj, attr):
            self.fail(HAS_ATTR_MESSAGE.format(obj, attr))


class AutomateOrderHelperTest(AutomationBase):
    def test_spec_not_routine(self):
        res = helpers.spec_is_routine(self.spec3)
        self.assertFalse(res)

    def test_spec_is_routine_decimal(self):
        self.spec2.kw = 18.5
        self.spec2.save()
        res = helpers.spec_is_routine(self.spec2)
        self.assertTrue(res)

    def test_spec_is_routine(self):
        self.spec2.kw = 132.0
        self.spec2.save()
        res = helpers.spec_is_routine(self.spec2)
        self.assertTrue(res)

    def test_order_is_not_routine(self):
        res = helpers.order_is_routine(self.order)
        self.assertFalse(res)

    def test_order_is_routine(self):
        self.spec3.delete()
        res = helpers.order_is_routine(self.order)
        self.assertTrue(res)
