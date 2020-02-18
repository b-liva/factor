import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from request.models import Xpref, PrefSpec


class ProformaNode(DjangoObjectType):
    customer_name = graphene.String()

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
