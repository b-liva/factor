from graphene import relay
from graphene_django.types import DjangoObjectType

from request.models import Perm, PermSpec


class PermNode(DjangoObjectType):
    class Meta:
        model = Perm
        filter_fields = ['number']
        interfaces = (relay.Node,)


class PermSpecNode(DjangoObjectType):
    class Meta:
        model = PermSpec
        filter_fields = ['code', 'price']
        interfaces = (relay.Node,)
