import graphene

from incomes.models import Income, IncomeRow

from graphene import Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphene import relay


class IncomeNode(DjangoObjectType):
    class Meta:
        model = Income
        filter_fields = {
            'number': ['exact'],
            'amount': ['exact'],
            'customer__name': ['icontains'],
        }
        interfaces = (relay.Node,)

    assigned_count = graphene.String()
    amount_assigned = graphene.Float()
    amount_not_assigned = graphene.Float()

    def resolve_assigned_count(self, info,):
        return self.incomerow_set.count()

    def resolve_amount_assigned(self, info, **kwargs):
        return self.assigned()

    def resolve_amount_not_assigned(self, info, **kwargs):
        return self.not_assigned()


class IncomeRowNode(DjangoObjectType):
    class Meta:
        model = IncomeRow
        interfaces = (Node,)
        filter_fields = ['amount', 'summary']
