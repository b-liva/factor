import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType

from motordb.models import Motors, MotorsCode, MotorsPrice


class MotorNode(DjangoObjectType):
    class Meta:
        model = Motors
        filter_fields = '__all__'
        interfaces = (relay.Node,)


class MotorCodeNode(DjangoObjectType):
    class Meta:
        model = MotorsCode
        filter_fields = '__all__'
        interfaces = (relay.Node,)


class MotorPriceNode(DjangoObjectType):
    class Meta:
        model = MotorsPrice
        filter_fields = '__all__'
        interfaces = (relay.Node,)
