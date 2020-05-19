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

    def resolve_specs_no_proforma(self, info):
        # proforma = Xpref.objects.get(number=9820555)
        pspecs = self.prefspec_set.all()
        specs = ReqSpec.objects.filter(req_id=self.req_id).exclude(prefspec__in=pspecs)
        # specs = ReqSpec.objects.filter(req_id=self.req_id, prefspec__isnull=True)
        return specs


class PrefSpecNode(DjangoObjectType):
    class Meta:
        model = PrefSpec
        filter_fields = '__all__'
        interfaces = (relay.Node,)


class ProformaSpecInput(InputObjectType):
    id = graphene.ID()
    qty = graphene.Int()
    price = graphene.Float()
