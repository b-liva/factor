import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from .types import PriceDbType, MotorDbNode


class Query(object):
    price_db = relay.Node.Field(PriceDbType)
    all_price_dbs = DjangoFilterConnectionField(PriceDbType)

    motor_db = relay.Node.Field(MotorDbNode)
    all_motor_db = DjangoFilterConnectionField(MotorDbNode)
