from graphene import relay
from graphene_django.types import DjangoObjectType

from core.utils import OwnQuerySet
from request.models import Perm, PermSpec


class PermNode(OwnQuerySet, DjangoObjectType):
    class Meta:
        model = Perm
        filter_fields = ['number']
        interfaces = (relay.Node,)


class PermSpecNode(OwnQuerySet, DjangoObjectType):
    class Meta:
        model = PermSpec
        filter_fields = ['code', 'price']
        interfaces = (relay.Node,)
