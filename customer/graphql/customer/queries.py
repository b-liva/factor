import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField

from .types import CustomerNode, CustomerTypeNode


class Query(object):
    customer = relay.Node.Field(CustomerNode)
    all_customers = DjangoFilterConnectionField(CustomerNode)

    customer_type = relay.Node.Field(CustomerTypeNode)
    all_customer_types = DjangoFilterConnectionField(CustomerTypeNode)
