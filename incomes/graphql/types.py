"""
Graphql Types for Income app
"""
import django_filters
import graphene
from graphene import Node, relay
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from incomes.models import Income, IncomeRow, PaymentType
from core.utils import OwnQuerySet


class IncomeFilterSet(django_filters.FilterSet):
    pk = django_filters.NumberFilter(field_name='pk')

    class Meta:
        model = Income
        fields = filter_fields = {
            'owner__last_name': ['icontains'],
            'number': ['exact'],
            'amount': ['exact'],
            'customer__name': ['icontains'],
        }


class IncomeNode(OwnQuerySet, DjangoObjectType):
    """
    Node For Income app with relay interface.
    """
    pk = graphene.Field(type=graphene.Int, source='id')

    class Meta:
        model = Income

        interfaces = (relay.Node,)

    assigned_count = graphene.String()
    amount_assigned = graphene.Float()
    amount_not_assigned = graphene.Float()

    def resolve_assigned_count(self, info):
        return self.incomerow_set.count()

    def resolve_amount_assigned(self, info, **kwargs):
        return self.assigned()

    def resolve_amount_not_assigned(self, info, **kwargs):
        return self.not_assigned()


class IncomeRowNode(OwnQuerySet, DjangoObjectType):
    """Node for incomerow app with relay interface."""
    class Meta:
        model = IncomeRow
        interfaces = (Node,)
        filter_fields = {
            'amount': ['exact', 'gt'],
            'income': ['exact'],
            'summary': ['icontains']
        }

