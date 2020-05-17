import django_filters
import graphene
from django.db.models import Sum
from graphene import relay, Node
from graphene_django.types import DjangoObjectType
from graphql_relay import from_global_id


from customer.models import Customer, Type
from request.models import PrefSpec


class CustomerFilterSet(django_filters.FilterSet):
    pk = django_filters.NumberFilter(field_name='pk')

    class Meta:
        model = Customer
        fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains']
        }


class CustomerNode(DjangoObjectType):
    # pk = graphene.Field(type=graphene.Int, source='id')

    class Meta:
        model = Customer
        interfaces = (relay.Node,)

    customer_total_kw = graphene.Int()
    sales_qty = graphene.Int()
    sales_kw = graphene.Float()
    amount_received = graphene.Float()
    amount_receivable = graphene.Float()
    sales_amount = graphene.Float()

    def resolve_customer_total_kw(self, info):
        return self.total_kw()['amount']

    def resolve_sales_qty(self, info):
        return self.sales_qty()

    def resolve_sales_kw(self, info):
        return self.sales_kw()

    def resolve_amount_received(self, info):
        return self.total_received()['amount']

    def resolve_amount_receivable(self, info):
        return self.total_receivable()

    def resolve_sales_amount(self, info):
        return self.sales_amount()


class CustomerTypeNode(DjangoObjectType):

    class Meta:
        model = Type
        filter_fields = {
            'name': ['icontains']
        }
        interfaces = (relay.Node,)
