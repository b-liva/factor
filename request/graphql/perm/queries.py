from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from .types import PermNode, PermSpecNode


class Query(object):
    perm = relay.Node.Field(PermNode)
    all_perms = DjangoFilterConnectionField(PermNode)

    perm_spec = relay.Node.Field(PermSpecNode)
    all_perm_specs = DjangoFilterConnectionField(PermSpecNode)
