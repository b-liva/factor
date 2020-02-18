import graphene
from graphene_django.types import DjangoObjectType

from customer.models import Customer


class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer


class Query(object):
    customer = graphene.Field(CustomerType,
                              id=graphene.Int(),
                              name=graphene.String(),
                              code=graphene.Int()
                              )
    all_customers = graphene.List(CustomerType,
                                  name=graphene.String())
    customers_count = graphene.Int()

    def resolve_all_customers(self, info, **kwargs):
        print(info)
        print(kwargs)
        print(self)
        name = kwargs.get('name')
        if name is not None:
            return Customer.objects.filter(name__icontains=name)
        return Customer.objects.all()

    def resolve_customers_count(self, info, **kwargs):
        return Customer.objects.count()

    def resolve_customer(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')
        code = kwargs.get('code')

        if id is not None:
            return Customer.objects.get(id=id)
        if name is not None:
            return Customer.objects.get(name=name)
        if code is not None:
            return Customer.objects.get(code=code)
        return None

