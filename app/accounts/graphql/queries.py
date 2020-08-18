import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from .types import UserNode
from accounts.models import User


class Query(object):
    user = relay.Node.Field(UserNode)
    all_users = DjangoFilterConnectionField(UserNode)
    me = graphene.Field(UserNode)
    user_by = graphene.Field(UserNode, username=graphene.String())

    def resolve_user_by(self, info, username):
        if username is not None:
            user = User.objects.get(username=username)
            return user
        return None

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in.')
        return user

