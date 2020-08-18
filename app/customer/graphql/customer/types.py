import django_filters
import graphene
from django.db.models import Sum, F, FloatField
from graphene import relay, Node
from graphene_django.types import DjangoObjectType
from graphql_relay import from_global_id


from customer.models import Customer, Type
from request.models import PrefSpec, Xpref
from request.graphql.proforma.types import ProformaNode


class CustomerFilterSet(django_filters.FilterSet):
    pk = django_filters.NumberFilter(field_name='pk')

    class Meta:
        model = Customer
        fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains']
        }


class CustomerNode(DjangoObjectType):
    # pk = graphene.Field(type=graphene.Int, source='id')

    class Meta:
        model = Customer
        interfaces = (relay.Node,)

    customer_total_kw = graphene.Int()
    sales_qty = graphene.Int()
    sales_kw = graphene.Float()
    amount_received = graphene.Float()
    amount_receivable = graphene.Float()
    sales_amount = graphene.Float()
    unpaid_proformas = graphene.List(ProformaNode)
    sale_total = graphene.Float()
    paid_total = graphene.Float()
    unpaid_total = graphene.Float()

    def resolve_customer_total_kw(self, info):
        return self.total_kw()['amount']

    def resolve_sales_qty(self, info):
        return self.sales_qty()

    def resolve_sales_kw(self, info):
        return self.sales_kw()

    def resolve_amount_received(self, info):
        return self.total_received()['amount']

    def resolve_amount_receivable(self, info):
        return self.total_receivable()

    def resolve_sales_amount(self, info):
        return self.sales_amount()

    def resolve_unpaid_proformas(self, info):
        unpaid = Xpref.objects.raw('SELECT *, total_proforma - total_income as diff FROM ( SELECT DISTINCT p.id, p.number, p.perm as is_perm, customer.name, customer.id as customer_id, SUM(DISTINCT 1.09*spec.qty * spec.price) as total_proforma, COALESCE(SUM(DISTINCT income.amount), 0) as total_income FROM request_xpref p INNER JOIN request_prefspec spec ON p.id=spec.xpref_id_id LEFT JOIN incomes_incomerow income ON p.id=income.proforma_id INNER JOIN request_requests req ON req.id=p.req_id_id INNER JOIN customer_customer customer ON req.customer_id=customer.id GROUP BY p.id ) as x WHERE customer_id=%s AND is_perm=1 AND (total_proforma - total_income > 0 OR total_proforma - total_income IS NULL) ORDER BY diff DESC', [self.id])
        return unpaid

    def resolve_sale_total(self, info):
        sale = PrefSpec.objects.filter(
            xpref_id__req_id__customer_id=self.id,
            xpref_id__perm=True).aggregate(
            amount=Sum(1.09 * F('price') * F('qty'),
                       output_field=FloatField()))['amount']
        sale = sale if sale is not None else 0
        return sale

    def resolve_paid_total(self, info):
        paid = Customer.objects.filter(id=self.id).aggregate(amount=Sum('income__incomerow__amount'))['amount']
        paid = paid if paid is not None else 0
        return paid

    def resolve_unpaid_total(self, info):
        sale = PrefSpec.objects.filter(
            xpref_id__req_id__customer_id=self.id,
            xpref_id__perm=True).aggregate(
            amount=Sum(1.09 * F('price') * F('qty'),
                       output_field=FloatField()))['amount']

        paid = Customer.objects.filter(id=self.id).aggregate(amount=Sum('income__incomerow__amount'))['amount']
        sale = sale if sale is not None else 0
        paid = paid if paid is not None else 0
        return sale - paid


class CustomerTypeNode(DjangoObjectType):

    class Meta:
        model = Type
        filter_fields = {
            'name': ['icontains']
        }
        interfaces = (relay.Node,)
