from django.db.models import Sum, F, FloatField
from graphene import relay, Int, String
from graphene_django.types import DjangoObjectType

from request.models import (
    Requests,
    ReqSpec,
    ProjectType,
    RpmType,
    IMType,
    ICType,
    IPType
)


class RequestNode(DjangoObjectType):
    class Meta:
        model = Requests
        filter_fields = {
            'number': ['exact'],
            'customer__name': ['icontains'],
            'is_active': ['exact'],
            'finished': ['exact'],
            'date_fa': ['exact', 'gte'],
            'xpref': ['isnull']
        }
        interfaces = (relay.Node,)

    total_kw = Int()
    total_qty = Int()

    def resolve_total_kw(self, info, **kwargs):
        total_kw = self.reqspec_set.filter(is_active=True).aggregate(kw=Sum(F('qty') * F('kw'), output_field=FloatField()))['kw']
        if total_kw is None:
            total_kw = 0
        return total_kw

    def resolve_total_qty(self, info):
        total_qty = self.reqspec_set.filter(is_active=True).aggregate(Sum('qty'))['qty__sum']
        if total_qty is None:
            total_qty = 0
        return total_qty


class ReqSpecNode(DjangoObjectType):
    class Meta:
        model = ReqSpec
        filter_fields = '__all__'
        interfaces = (relay.Node,)


# Not using relays

class ProjectTypeType(DjangoObjectType):
    class Meta:
        model = ProjectType
        fields = '__all__'


class RpmTypeNode(DjangoObjectType):
    class Meta:
        model = RpmType
        filter_fields = '__all__'
        interfaces = (relay.Node,)


class IMTypeNode(DjangoObjectType):
    class Meta:
        model = IMType
        filter_fields = '__all__'
        interfaces = (relay.Node,)


class ICTypeNode(DjangoObjectType):
    class Meta:
        model = ICType
        filter_fields = '__all__'
        interfaces = (relay.Node,)


class IPTypeNode(DjangoObjectType):
    class Meta:
        model = IPType
        filter_fields = '__all__'
        interfaces = (relay.Node,)
