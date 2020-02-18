from graphene import ObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from .forms.form import IncomeModelForm, IncomeRowModelForm


class IncomeModelFormMutation(DjangoModelFormMutation):
    class Meta:
        form_class = IncomeModelForm


class IncomeRowModelFormMutation(DjangoModelFormMutation):
    class Meta:
        form_class = IncomeRowModelForm


class IncomeModelMutation(object):
    income_mutation = IncomeModelFormMutation.Field()
    income_row_mutation = IncomeRowModelFormMutation.Field()
