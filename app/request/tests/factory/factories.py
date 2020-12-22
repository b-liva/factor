from faker import Factory
import factory
from core.tests.factory.factories import UserFactory
from request.models import PrefSpec, Xpref, ReqSpec, Requests, RpmType, ICType, IMType, IPType, IEType, ProjectType
from customer.tests.factory.factories import CustomerFactory


faker = Factory.create()

kw = [
    '18.5',
    '75',
    '90',
    '132',
    '250',
    '450',
]
rpm = [1000, 1500, 3000]
poles = [2, 4, 6]
voltage = [380, 400]

im = ['IMB3', 'IMB35']
ip = ['IP55', 'IP56']
ic = ['IC411', 'IC611']
ie = ['IE2', 'IE3']


class ImTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IMType

    title = factory.lazy_attribute(lambda o: faker.random_choices(im, 1)[0])


class IPTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IPType

    title = factory.lazy_attribute(lambda o: faker.random_choices(ip, 1)[0])


class IcTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ICType

    title = factory.lazy_attribute(lambda o: faker.random_choices(ic, 1)[0])


class IeTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IEType

    title = factory.lazy_attribute(lambda o: faker.random_choices(ie, 1)[0])


class ProjectTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProjectType

    title = faker.word()
    summary = faker.text()


class RpmTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RpmType

    rpm = factory.lazy_attribute(lambda o: faker.random_choices(rpm, 1)[0])
    pole = factory.lazy_attribute(lambda o: faker.random_choices(poles, 1)[0])


class RequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Requests
        django_get_or_create = ('temp_number',)

    customer = factory.SubFactory(CustomerFactory)
    owner = factory.SubFactory(UserFactory)
    number = faker.random_int()
    temp_number = faker.random_int()


class ReqSpecFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ReqSpec

    code = faker.random_int()
    req_id = factory.SubFactory(RequestFactory)
    owner = factory.SubFactory(UserFactory)
    type = factory.SubFactory(ProjectTypeFactory)
    qty = faker.random_int()
    kw = factory.lazy_attribute(lambda o: faker.random_choices(kw, 1)[0])
    rpm_new = factory.SubFactory(RpmTypeFactory)
    voltage = factory.lazy_attribute(lambda o: faker.random_choices(voltage, 1)[0])
    im = factory.SubFactory(ImTypeFactory)
    ip = factory.SubFactory(IPTypeFactory)
    ic = factory.SubFactory(IcTypeFactory)
    ie = factory.SubFactory(IeTypeFactory)


class ProformaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Xpref

    owner = factory.SubFactory(UserFactory)
    req_id = factory.SubFactory(RequestFactory)
    number = faker.random_int()


class ProformaSpecFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PrefSpec

    owner = factory.SubFactory(UserFactory)
    xpref_id = factory.SubFactory(ProformaFactory)
    reqspec_eq = factory.SubFactory(ReqSpecFactory)
    im = factory.SubFactory(ImTypeFactory)
    ip = factory.SubFactory(IPTypeFactory)
    ic = factory.SubFactory(IcTypeFactory)
    qty = factory.lazy_attribute(lambda o: faker.random_int())
    price = factory.lazy_attribute(lambda o: faker.random_int())
    kw = factory.lazy_attribute(lambda o: faker.random_choices(kw, 1)[0])
    rpm = factory.lazy_attribute(lambda o: faker.random_choices(rpm, 1)[0])
    voltage = 380
