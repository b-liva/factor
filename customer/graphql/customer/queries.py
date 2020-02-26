import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField

from .types import CustomerNode, CustomerTypeNode, CustomerFilterSet


# class Query(object):
class Query(graphene.ObjectType):
    customer = relay.Node.Field(CustomerNode)
    all_customers = DjangoFilterConnectionField(CustomerNode, filterset_class=CustomerFilterSet)

    customer_type = relay.Node.Field(CustomerTypeNode)
    all_customer_types = DjangoFilterConnectionField(CustomerTypeNode)
