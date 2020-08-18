from graphene_django.types import DjangoObjectType
from req_track.models import ReqEntered


class AutomationOrderNode(DjangoObjectType):

    class Meta:
        model = ReqEntered
