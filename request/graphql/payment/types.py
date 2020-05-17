import django_filters
import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType

from request.models import Payment, PaymentType


# class PaymentFitlerSet(django_filters.FilterSet)
#     class Meta:
#         model = Payment
#         fields =


class PaymentNode(DjangoObjectType):
    customer_name = graphene.String()
    pk = graphene.Field(type=graphene.Int, source='id')

    def resolve_customer_name(self, info):
        return self.xpref_id.req_id.customer.name

    class Meta:
        model = Payment
        filter_fields = {
            'number': ['exact'],
            'xpref_id__req_id__customer__name': ['icontains'],
            # 'customer_name': ['icontains'] to use this probably i should define a filterset??
        }
        interfaces = (relay.Node,)


class PaymentTypeNode(DjangoObjectType):
    pk = graphene.Field(type=graphene.Int, source='id')

    class Meta:
        model = PaymentType
        filter_fields = '__all__'
        interfaces = (relay.Node,)
