import accounts.graphql.queries
import customer.graphql.schema_temp
import request.graphql.perm.queries
import request.graphql.proforma.queries
import request.graphql.orders.queries
import request.graphql.payment.queries
import customer.graphql.customer.queries
import pricedb.graphql.queries
import motordb.graphql.queries
import incomes.graphql.queries
# mutations
import customer.graphql.customer.mutations
import request.graphql.orders.mutations
import request.graphql.proforma.mutations
import request.graphql.payment.mutations
import incomes.graphql.mutations
import graphene
from graphene_django.debug import DjangoDebug

from customer.models import Customer


class Query(
    accounts.graphql.queries.Query,
    request.graphql.orders.queries.Query,
    request.graphql.perm.queries.Query,
    request.graphql.proforma.queries.Query,
    request.graphql.payment.queries.Query,
    customer.graphql.customer.queries.Query,
    pricedb.graphql.queries.Query,
    incomes.graphql.queries.Query,
    motordb.graphql.queries.Query,
    # customer.graphql.schema_temp.Query,
    graphene.ObjectType
):
    debug = graphene.Field(DjangoDebug, name='_debug')


class Mutations(
    # customer.graphql.customer.mutations.TempMutation,
    customer.graphql.customer.mutations.CustomerModelMutations,
    request.graphql.orders.mutations.RequestModelMutations,
    request.graphql.proforma.mutations.ProformaModelMutation,
    request.graphql.payment.mutations.PaymentModelMutation,
    incomes.graphql.mutations.IncomeModelMutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutations)
