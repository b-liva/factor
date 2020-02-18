import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType

from customer.models import Customer, Type


class CustomerNode(DjangoObjectType):

    class Meta:
        model = Customer
        filter_fields = {
            'name': ['exact', 'icontains']
        }
        interfaces = (relay.Node,)

    customer_total_kw = graphene.Int()

    def resolve_customer_total_kw(self, info):
        return self.total_kw()['amount']


class CustomerTypeNode(DjangoObjectType):

    class Meta:
        model = Type
        filter_fields = {
            'name': ['icontains']
        }
        interfaces = (relay.Node,)
