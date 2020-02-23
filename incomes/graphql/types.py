"""
Graphql Types for Income app
"""
import graphene
from graphene import Node, relay
from graphene_django.types import DjangoObjectType
from incomes.models import Income, IncomeRow


class IncomeNode(DjangoObjectType):
    """
    Node For Income app with relay interface.
    """
    class Meta:
        model = Income
        filter_fields = {
            'owner__last_name': ['icontains'],
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
    """Node for incomerow app with relay interface."""
    class Meta:
        model = IncomeRow
        interfaces = (Node,)
        filter_fields = ['amount', 'summary']
