from graphene import relay, Float, Field, List
import graphene

from graphene_django.filter import DjangoFilterConnectionField
from .types import ProformaNode, PrefSpecNode, ProformaFilterSet, PrefSpecSummary, CustomerBySale
from core.utilities.permit import sales_total, income_total, specs_sold_by_qty
from core.utilities.customer import customer_by_sale


class Query(object):
    proforma = relay.Node.Field(ProformaNode)
    all_proformas = DjangoFilterConnectionField(ProformaNode, filterset_class=ProformaFilterSet)

    pref_spec = relay.Node.Field(PrefSpecNode)
    all_pref_specs = DjangoFilterConnectionField(PrefSpecNode)

    sales_total = Float(days=graphene.Int())
    income_total = Float(days=graphene.Int())
    specs_sold_by_qty = List(PrefSpecSummary, days=graphene.Int())
    customer_by_sale = graphene.List(CustomerBySale, days=graphene.Int())

    def resolve_sales_total(self, info, days):
        return sales_total(days)

    def resolve_income_total(self, info, days):
        return income_total(days)

    def resolve_specs_sold_by_qty(self, info, days):
        return specs_sold_by_qty(days)

    def resolve_customer_by_sale(self, info, days):
        return customer_by_sale(days)
