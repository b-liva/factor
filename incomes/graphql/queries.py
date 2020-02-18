from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from incomes.graphql.types import IncomeNode, IncomeRowNode


class Query(object):
    income = relay.Node.Field(IncomeNode)
    all_incomes = DjangoFilterConnectionField(IncomeNode)

    income_row = relay.Node.Field(IncomeRowNode)
    all_income_rows = DjangoFilterConnectionField(IncomeRowNode)
