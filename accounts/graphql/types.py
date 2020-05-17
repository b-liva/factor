import jdatetime
from graphene import relay, Int, Float
from graphene_django import DjangoObjectType

from accounts.models import User
from req_track.models import ReqEntered
from request.models import Requests


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = {
            'is_customer': ['exact'],
            'sales_exp': ['exact']
        }
        interfaces = (relay.Node,)

    order_not_entered_count = Int()
    order_entered_count = Int()
    order_no_proforma_count = Int()
    percent_entered = Float()

    def resolve_order_not_entered_count(self, info):
        print(info.context.user)
        print(self.last_name)
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
