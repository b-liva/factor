from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from .types import UserNode


class Query(object):
    user = relay.Node.Field(UserNode)
    all_users = DjangoFilterConnectionField(UserNode)
