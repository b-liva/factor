import django_filters
import graphene
from graphene import relay, Node
from graphene_django.types import DjangoObjectType
from graphql_relay import from_global_id

from customer.models import Customer, Type


class CustomerFilterSet(django_filters.FilterSet):
    pk = django_filters.NumberFilter(field_name='pk')

    class Meta:
        model = Customer
        fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains']
        }


class CustomerNode(DjangoObjectType):
    pk = graphene.Field(type=graphene.Int, source='id')

    class Meta:
        model = Customer
        # filter_fields is now a duplication and will be deleted.
        filter_fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains']
        }
        interfaces = (relay.Node,)

    customer_total_kw = graphene.Int()

    def resolve_customer_total_kw(self, info):
        return self.total_kw()['amount']


class CustomerTypeNode(DjangoObjectType):

    class Meta:
        model = Type
        filter_fields = {
            'name': ['icontains']
        }
        interfaces = (relay.Node,)
