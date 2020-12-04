import random
import secrets
import factory
from faker import Factory
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from cost import models
from core.tests.factory.factories import UserFactory

faker = Factory.create()
User = get_user_model()


unit_choices = [
        ('kg', _('kg')),
        ('machine', _('machine')),
        ('item', _('item')),
    ]


def get_random_unit_choice():
    return secrets.choice(unit_choices)


class BaseCostFactory(factory.django.DjangoModelFactory):
    # users = UserFactory.create_batch(5)

    # def __int__(self):
    #     super().__init__()
    #     get_user_model().objects.delete()

    owner = factory.SubFactory(UserFactory)
    # qty = faker.random_int()
    qty = factory.lazy_attribute(lambda o: faker.random_int())
    # price = faker.random_int()
    price = factory.lazy_attribute(lambda o: faker.random_int())
    # unit = factory.LazyFunction(get_random_unit_choice)
    # unit = faker.random_choices(unit_choices, 1)
    unit = factory.lazy_attribute(lambda o: faker.random_choices(unit_choices, 1))


class WageCostFactory(BaseCostFactory):
    class Meta:
        model = models.WageCost


class SteelrebarCostFactory(BaseCostFactory):
    class Meta:
        model = models.SteelRebar


class OverheadCostFactory(BaseCostFactory):
    class Meta:
        model = models.OverheadCost


class SteelCostFactory(BaseCostFactory):
    class Meta:
        model = models.Steel


class CuStatorCostFactory(BaseCostFactory):
    class Meta:
        model = models.CuStator


class AluIgnotCostFactory(BaseCostFactory):
    class Meta:
        model = models.AluIngot


class SiliconSheetCostFactory(BaseCostFactory):
    class Meta:
        model = models.SiliconSheet


class CastIronCostFactory(BaseCostFactory):
    class Meta:
        model = models.CastIron


class BearingCostFactory(BaseCostFactory):
    class Meta:
        model = models.Bearing

    name = factory.Sequence(lambda n: 'NU %s' % n)


class TestCostFactory(BaseCostFactory):
    class Meta:
        model = models.Test

    name = factory.Sequence(lambda n: 'Atex %s' % n)


class CertificateCostFactory(BaseCostFactory):
    class Meta:
        model = models.Certificate

    name = factory.Sequence(lambda n: 'Cert %s' % n)


class ProjectCostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ProjectCost

    ch_number = faker.random_int()
    motor_type = faker.name()
    # date_fa = jmodels.jDateField(default=now)

    owner = factory.SubFactory(UserFactory)
    wage = factory.SubFactory(WageCostFactory)
    steel_rebar = factory.SubFactory(SteelrebarCostFactory)
    overhead = factory.SubFactory(OverheadCostFactory)
    steel = factory.SubFactory(SteelCostFactory)
    cu = factory.SubFactory(CuStatorCostFactory)
    alu = factory.SubFactory(AluIgnotCostFactory)
    silicon = factory.SubFactory(SiliconSheetCostFactory)
    cast_iron = factory.SubFactory(CastIronCostFactory)

    standard_parts = faker.random_int()
    cost_production = faker.random_int()
    general_cost = faker.random_int()
    cost_practical = faker.random_int()

    @factory.post_generation
    def bearing(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for br in extracted:
                self.bearing.add(br)

    @factory.post_generation
    def test(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for ts in extracted:
                self.test.add(ts)

    @factory.post_generation
    def certificate(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for cr in extracted:
                self.certificate.add(cr)
