from graphene import relay
from graphene_django import DjangoObjectType

from accounts.models import User


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = {
            'is_customer': ['exact'],
            'sales_exp': ['exact']
        }
        interfaces = (relay.Node,)
