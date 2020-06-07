from django.db.models import Sum, F, FloatField
import django_filters
import graphene
from graphene import relay, InputObjectType
from graphene_django import DjangoObjectType

from request.graphql.orders.types import ReqSpecNode
from request.models import Xpref, PrefSpec, ReqSpec


class ProformaFilterSet(django_filters.FilterSet):
    # This will be added to fields by default as ['exact'] so there is no need to add it explicitly.
    customer_pk = django_filters.NumberFilter(field_name='req_id__customer__id')

    class Meta:
        model = Xpref
        fields = {
            'number': ['exact'],
            'number_td': ['exact'],
            'req_id__customer__name': ['icontains']
        }


class ProformaNode(DjangoObjectType):
    customer_name = graphene.String()
    pk = graphene.Field(type=graphene.Int, source='id')

    def resolve_customer_name(self, info):
        return self.req_id.customer.name

    class Meta:
        model = Xpref
        filter_fields = {
            'number': ['exact'],
            'number_td': ['exact'],
            'req_id__customer__name': ['icontains']
        }

        interfaces = (relay.Node,)
    specs_no_proforma = graphene.List(ReqSpecNode)
    amount_total = graphene.Float()
    paid_total = graphene.Float()
    unpaid_total = graphene.Float()

    def resolve_specs_no_proforma(self, info):
        specs = ReqSpec.objects.filter(req_id=self.req_id)
        return specs

    def resolve_amount_total(self, info):
        total_amount = Xpref.objects.filter(id=self.id, perm=True).aggregate(
            amount=Sum(1.09 * F('prefspec__price') * F('prefspec__qty'),
                    output_field=FloatField()))['amount']
        total_amount = total_amount if total_amount is not None else 0

        return total_amount

    def resolve_paid_total(self, info):
        paid_total = Xpref.objects.filter(id=self.id).aggregate(amount=Sum('incomerow__amount'))['amount']
        paid_total = paid_total if paid_total is not None else 0
        return paid_total

    def resolve_unpaid_total(self, info):
        total_amount = Xpref.objects.filter(id=self.id, perm=True).aggregate(
            amount=Sum(1.09 * F('prefspec__price') * F('prefspec__qty'),
                       output_field=FloatField()))['amount']
        paid_total = Xpref.objects.filter(id=self.id).aggregate(amount=Sum('incomerow__amount'))['amount']
        total_amount = total_amount if total_amount is not None else 0
        paid_total = paid_total if paid_total is not None else 0
        return total_amount - paid_total


class PrefSpecNode(DjangoObjectType):
    class Meta:
        model = PrefSpec
        filter_fields = '__all__'
        interfaces = (relay.Node,)


class ProformaSpecInput(InputObjectType):
    id = graphene.ID()
    qty = graphene.Int()
    price = graphene.Float()
