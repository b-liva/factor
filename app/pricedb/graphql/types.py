import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from pricedb.models import PriceDb, MotorDB


class PriceDbType(DjangoObjectType):
    class Meta:
        model = PriceDb
        filter_fields = '__all__'
        interfaces = (relay.Node,)


class MotorDbNode(DjangoObjectType):
    class Meta:
        model = MotorDB
        filter_fields = '__all__'
        interfaces = (relay.Node,)

    profit = graphene.Float()

    def resolve_profit(self, info):
        profit = self.sale_price - self.base_price
        return 100 * profit / self.base_price
