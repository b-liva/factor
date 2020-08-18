from django.db.models import Sum, F, FloatField
import django_filters
import graphene
from graphene import relay, InputObjectType
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from core.decorators import permission_required
from core.permissions import ProformaPermissions
from core.utils import OwnQuerySet
from request.graphql.orders.types import ReqSpecNode
from request.models import Xpref, PrefSpec, ReqSpec


class ProformaFilterSet(django_filters.FilterSet):
    # This will be added to fields by default as ['exact'] so there is no need to add it explicitly.
    customer_pk = django_filters.NumberFilter(field_name='req_id__customer__id')

    class Meta:
        model = Xpref
        fields = {
            'number': ['exact'],
            'req_id': ['exact'],
            'number_td': ['exact'],
            'req_id__customer__name': ['icontains']
        }


class ProformaNode(OwnQuerySet, DjangoObjectType):
    customer_name = graphene.String()
    pk = graphene.Field(type=graphene.Int, source='id')

    def resolve_customer_name(self, info):
        return self.req_id.customer.name

    class Meta:
        model = Xpref
        filter_fields = {
            'number': ['exact'],
            'number_td': ['exact'],
            'req_id__customer__name': ['icontains']
        }

        interfaces = (relay.Node,)
    specs_no_proforma = graphene.List(ReqSpecNode)
    amount_total = graphene.Float()
    paid_total = graphene.Float()
    unpaid_total = graphene.Float()

    @classmethod
    @login_required
    @permission_required([ProformaPermissions.ADD_PROFORMA])  # todo: change this to read permission later.
    def get_node(cls, info, id):
        return super(ProformaNode, cls).get_node(info, id)

    def resolve_specs_no_proforma(self, info):
        pref_specs = self.prefspec_set.all()
        reqspec_eq_ids = [x.reqspec_eq.pk for x in pref_specs]
        new_specs = ReqSpec.objects.filter(req_id=self.req_id).exclude(id__in=reqspec_eq_ids)
        return new_specs

    def resolve_amount_total(self, info):
        total_amount = Xpref.objects.filter(id=self.id, perm=True).aggregate(
            amount=Sum(1.09 * F('prefspec__price') * F('prefspec__qty'),
                    output_field=FloatField()))['amount']
        total_amount = total_amount if total_amount is not None else 0

        return total_amount

    def resolve_paid_total(self, info):
        paid_total = Xpref.objects.filter(id=self.id).aggregate(amount=Sum('incomerow__amount'))['amount']
        paid_total = paid_total if paid_total is not None else 0
        return paid_total

    def resolve_unpaid_total(self, info):
        total_amount = Xpref.objects.filter(id=self.id, perm=True).aggregate(
            amount=Sum(1.09 * F('prefspec__price') * F('prefspec__qty'),
                       output_field=FloatField()))['amount']
        paid_total = Xpref.objects.filter(id=self.id).aggregate(amount=Sum('incomerow__amount'))['amount']
        total_amount = total_amount if total_amount is not None else 0
        paid_total = paid_total if paid_total is not None else 0
        return total_amount - paid_total


class PrefSpecNode(OwnQuerySet, DjangoObjectType):
    class Meta:
        model = PrefSpec
        filter_fields = '__all__'
        interfaces = (relay.Node,)

    @classmethod
    @login_required
    @permission_required([ProformaPermissions.ADD_PREF_SPEC])  # todo: change this to read permission later.
    def get_node(cls, info, id):
        return super(PrefSpecNode, cls).get_node(info, id)


class ProformaSpecInput(InputObjectType):
    eqId = graphene.ID()
    id = graphene.ID()
    qty = graphene.Int()
    price = graphene.Float()
