import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from .types import UserNode


class Query(object):
    user = relay.Node.Field(UserNode)
    all_users = DjangoFilterConnectionField(UserNode)
    me = graphene.Field(UserNode)

    def resolve_me(self, info):
        user = info.context.user
        print('user', user)
        if user.is_anonymous:
            raise Exception('Not logged in.')
        return user

