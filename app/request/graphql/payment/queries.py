from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from .types import PaymentNode, PaymentTypeNode


class Query(object):
    payment = relay.Node.Field(PaymentNode)
    all_payments = DjangoFilterConnectionField(PaymentNode)

    payment_type = relay.Node.Field(PaymentTypeNode)
    all_payment_types = DjangoFilterConnectionField(PaymentTypeNode)
