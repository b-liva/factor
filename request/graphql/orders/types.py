from graphene import relay
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
        filter_fields = ['number', 'customer__name']
        interfaces = (relay.Node,)


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
