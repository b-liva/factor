from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from cost.models import WageCost, Bearing, ProjectCost
from cost.tests.factory import factories

User = get_user_model()


class FactoryTest(APITestCase):

    def test_create_wage_cost(self):
        wage = factories.WageCostFactory()
        wage_obj = WageCost.objects.filter().last()
        self.assertEqual(wage.pk, wage_obj.pk)

    def test_create_bearing_cost(self):
        bearing = factories.BearingCostFactory()
        bearing_obj = Bearing.objects.last()
        self.assertEqual(bearing.pk, bearing_obj.pk)

    def test_create_project_cost(self):

        bearings = factories.BearingCostFactory.create_batch(5)
        tests = factories.TestCostFactory.create_batch(5)
        certs = factories.CertificateCostFactory.create_batch(5)

        pc = factories.ProjectCostFactory.create(bearing=bearings, test=tests, certificate=certs)

        pc_obj = ProjectCost.objects.last()

        self.assertEqual(pc.pk, pc_obj.pk)
        self.assertEqual(pc_obj.bearing.count(), len(bearings))

    def test_wage_specific_user(self):
        user = User.objects.create(
            username='basir',
            password='somepass'
        )
        wage = factories.WageCostFactory(owner=user)
        wage_obj = WageCost.objects.last()

        self.assertEqual(wage_obj.owner.pk, user.pk)
        self.assertEqual(wage_obj.owner.username, user.username)
