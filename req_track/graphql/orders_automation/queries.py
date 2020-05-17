import graphene
import graphene_django
from req_track.models import ReqEntered
from .types import AutomationOrderNode


class Query(object):
    automation_orders = graphene.List(AutomationOrderNode)

    def resolve_automation_orders(self, info, **kwargs):
        # if not info.context.user.is_superuser:
        if info.context.user.is_superuser:
            return ReqEntered.objects.filter(owner_text__contains=info.context.user.last_name, is_request=True, is_entered=False)
        return ReqEntered.objects.filter(is_request=True, is_entered=False)
