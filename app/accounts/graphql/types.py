import jdatetime
from graphene import relay, Int, Float, List, String, JSONString
from graphene_django import DjangoObjectType
from graphql_relay import to_global_id

from accounts.models import User
from req_track.models import ReqEntered
from request.models import Requests


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = {
            'is_active': ['exact'],
            'is_customer': ['exact'],
            'sales_exp': ['exact']
        }
        interfaces = (relay.Node,)

    order_not_entered_count = Int()
    order_entered_count = Int()
    order_no_proforma_count = Int()
    percent_entered = Float()
    permissions = List(String)
    permission_json = List(JSONString)

    def resolve_order_not_entered_count(self, info):
        return ReqEntered.objects.filter(is_entered=False, is_request=True,
                                         owner_text__icontains=self.last_name).count()

    def resolve_order_entered_count(self, info):
        return Requests.objects.filter(is_active=True, owner=self).count()

    def resolve_order_no_proforma_count(self, info):
        date = jdatetime.date(month=10, day=1, year=1397)
        reqs = Requests.objects.filter(
            is_active=True,
            finished=False,
            date_fa__gte=date,
            owner=self,
            xpref__isnull=True
        )
        return reqs.count()

    def resolve_percent_entered(self, info):
        user_orders = Requests.objects.filter(is_active=True, owner=self).count()
        all_orders = Requests.objects.filter(is_active=True).count()
        return 100 * user_orders / all_orders

    def resolve_permissions(self, info):
        return self.get_all_permissions()

    def resolve_permission_json(self, info):
        permissions = self.get_all_permissions()
        perms_json = [{
            'action': perm.split('.')[1].split('_')[0],
            'subject': perm.split('.')[1].split('_')[1],
            # 'conditions': {
            #     'ownerId': to_global_id('user', self.pk)
            # }
        } for perm in permissions]
        return perms_json
