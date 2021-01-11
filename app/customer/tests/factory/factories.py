from faker import Factory
import factory
from customer.models import Customer, Type
from core.tests.factory.factories import UserFactory


faker = Factory.create()


class CustomerTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Type

    name = factory.Sequence(lambda n: 'customer type %s' % n)


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer
        django_get_or_create = ('code',)

    owner = factory.SubFactory(UserFactory)
    type = factory.SubFactory(CustomerTypeFactory)
    code = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: 'customer %s' % n)
    agent = False
