import django_filters
import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from request.models import Xpref, PrefSpec


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


class PrefSpecNode(DjangoObjectType):
    class Meta:
        model = PrefSpec
        filter_fields = '__all__'
        interfaces = (relay.Node,)
