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
        ('pph', _('per hour')),
        ('item', _('item')),
    ]


def get_random_unit_choice():
    return secrets.choice(unit_choices)


class BaseCostFactory(factory.django.DjangoModelFactory):

    owner = factory.SubFactory(UserFactory)
    qty = factory.lazy_attribute(lambda o: faker.random_int())
    price = factory.lazy_attribute(lambda o: faker.random_int())
    unit = factory.lazy_attribute(lambda o: faker.random_choices(unit_choices[0], 1)[0])


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
    motor_type = faker.word()[:2]
    # date_fa = jmodels.jDateField(default=now)
    date_fa = faker.date()
    owner = factory.SubFactory(UserFactory)
    wage = factory.SubFactory(WageCostFactory)
    steel_rebar = factory.SubFactory(SteelrebarCostFactory)
    overhead = factory.SubFactory(OverheadCostFactory)
    steel = factory.SubFactory(SteelCostFactory)
    cu = factory.SubFactory(CuStatorCostFactory)
    alu = factory.SubFactory(AluIgnotCostFactory)
    silicon = factory.SubFactory(SiliconSheetCostFactory)
    cast_iron = factory.SubFactory(CastIronCostFactory)

    standard_parts = factory.lazy_attribute(lambda o: faker.random_int())
    cost_production = factory.lazy_attribute(lambda o: faker.random_int())
    general_cost = factory.lazy_attribute(lambda o: faker.random_int())
    cost_practical = factory.lazy_attribute(lambda o: faker.random_int())

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


def create_brs_tsts_certs(count=5):
    brngs = BearingCostFactory.create_batch(count)
    tsts = TestCostFactory.create_batch(count)
    certs = CertificateCostFactory.create_batch(count)
    return {
        'bearing': brngs,
        'test': tsts,
        'certificate': certs
    }


def create_sample_project_cost(**params):
    pc = ProjectCostFactory.create(**params)
    return pc


def create_sample_project_cost_batch(batch_size, **params):
    pc = ProjectCostFactory.create_batch(batch_size, **params)
    return pc


def create_batch(batch_size, **kwargs):
    import time
    time_start = time.time()
    create_sample_project_cost_batch(batch_size, **kwargs)
    time_end = time.time()
    print("Duration time: ", time_end - time_start)


def create_payload(**kwargs):
    params = create_brs_tsts_certs()
    params['owner'] = kwargs.get('owner')
    pc = create_sample_project_cost(**params)

    payload = {
        'owner': pc.owner.pk,
        'wage': pc.wage.pk,
        'steel_rebar': pc.steel_rebar.pk,
        'overhead': pc.overhead.pk,
        'steel': pc.steel.pk,
        'cu': pc.cu.pk,
        'alu': pc.alu.pk,
        'silicon': pc.silicon.pk,
        'cast_iron': pc.cast_iron.pk,
        'ch_number': pc.ch_number,
        'motor_type': pc.motor_type,
        'date_fa': str(pc.date_fa),
        'bearing': [i.pk for i in pc.bearing.all()],
        'test': [i.pk for i in pc.test.all()],
        'certificate': [i.pk for i in pc.certificate.all()],
        'standard_parts': pc.standard_parts,
        'cost_production': pc.cost_production,
        'general_cost': pc.general_cost,
        'cost_practical': pc.cost_practical,
    }
    return {
        'pc': pc,
        'payload': payload,
    }
