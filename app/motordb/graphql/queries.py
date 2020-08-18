import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField

from .types import MotorNode, MotorPriceNode, MotorCodeNode


class Query(object):
    motor = relay.Node.Field(MotorNode)
    all_motors = DjangoFilterConnectionField(MotorNode)

    motor_price = relay.Node.Field(MotorPriceNode)
    all_motor_prices = DjangoFilterConnectionField(MotorPriceNode)

    motor_code = relay.Node.Field(MotorCodeNode)
    all_motor_codes = DjangoFilterConnectionField(MotorCodeNode)
