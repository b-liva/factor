import math
from django.db.models import Sum, F, FloatField
import graphene
from graphene import relay, Int
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from core.decorators import permission_required
from core.permissions import OrderPermissions
from core.utils import OwnQuerySet
from request.models import (
    Requests,
    ReqSpec,
    ProjectType,
    RpmType,
    IMType,
    ICType,
    IPType
)


class TotalCountMixin(graphene.types.ObjectType):
    @classmethod
    def get_connection(cls):
        class CountableConnection(relay.Connection):
            total_count = Int()

            class Meta:
                name = '{}Connection'.format(cls._meta.name)
                node = cls

            @staticmethod
            def resolve_total_count(root, args, context, info):
                return root.length

        return CountableConnection


class CountableConnectionBase(relay.Connection):

    class Meta:
        abstract = True

    total_count = Int()
    num_pages = Int()

    def resolve_total_count(self, info, **kwargs):
        return self.iterable.count()

    def resolve_num_pages(self, info, *args, **kwargs):
        if 'first' in info.variable_values:
            number_pages = math.ceil(self.iterable.count() / info.variable_values['first'])
        else:
            number_pages = math.ceil(self.iterable.count() / info.variable_values['last'])
        return number_pages


class RequestNode(OwnQuerySet, DjangoObjectType):

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
        connection_class = CountableConnectionBase

    total_kw = Int()
    total_qty = Int()

    @classmethod
    @login_required
    @permission_required([OrderPermissions.ADD_REQUESTS])  # todo: change this to read permission later.
    def get_node(cls, info, id):
        return super(RequestNode, cls).get_node(info, id)

    @login_required
    def resolve_total_kw(self, info, **kwargs):
        total_kw = self.reqspec_set.filter(is_active=True).aggregate(kw=Sum(F('qty') * F('kw'), output_field=FloatField()))['kw']
        if total_kw is None:
            total_kw = 0
        return total_kw

    @login_required
    def resolve_total_qty(self, info):
        total_qty = self.reqspec_set.filter(is_active=True).aggregate(Sum('qty'))['qty__sum']
        if total_qty is None:
            total_qty = 0
        return total_qty


class ReqSpecNode(OwnQuerySet, DjangoObjectType):
    class Meta:
        model = ReqSpec
        filter_fields = '__all__'
        interfaces = (relay.Node,)

    @classmethod
    @login_required
    @permission_required([OrderPermissions.ADD_REQSPEC])  # todo: change this to read permission later.
    def get_node(cls, info, id):
        return super(ReqSpecNode, cls).get_node(info, id)


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
