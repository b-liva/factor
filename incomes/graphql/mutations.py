import sys
from django.db.models import Sum
from graphql import GraphQLError
from graphene_django.forms.mutation import DjangoModelFormMutation

from .forms.form import IncomeModelForm, IncomeRowModelForm
import request.templatetags.functions as funcs


class IncomeModelFormMutation(DjangoModelFormMutation):
    class Meta:
        form_class = IncomeModelForm

    @classmethod
    # @login_required
    def perform_mutate(cls, form, info):
        """ Checks for permission and then perform the mutate.
        :param form:
        :param info:
        :return:
        """
        owner = form.cleaned_data['owner']

        can_add = funcs.has_perm_or_is_owner(owner, 'incomes.add_income')

        if not can_add:
            sys.tracebacklimit = -1
            # traceback.format_exc()
            raise RuntimeError('No permission to do that.')
        return super().perform_mutate(form, info)


class IncomeRowModelFormMutation(DjangoModelFormMutation):
    class Meta:
        form_class = IncomeRowModelForm

    @classmethod
    def perform_mutate(cls, form, info):
        owner = form.cleaned_data['owner']
        can_add = funcs.has_perm_or_is_owner(owner, 'incomes.add_incomerow')

        if not can_add:
            sys.tracebacklimit = -1
            raise GraphQLError('No permission to do that.')

        proforma = form.cleaned_data['proforma']
        income = form.cleaned_data['income']
        amount = form.cleaned_data['amount']

        if proforma.req_id.customer != income.customer:
            sys.tracebacklimit = -1
            raise GraphQLError("customer mismatch")
        # TODO: two checks should be done.
        # 1- sum of income rows shouldn't be more than income amount,
        # 2- proforma income rows sum should be less than proforma amount

        proforma_assigns = proforma.incomerow_set.aggregate(sum=Sum('amount'))
        remained_income = income.amount - income.incomerow_set.aggregate(sum=Sum('amount'))['sum']
        proforma_remained = proforma.total_proforma_price_vat()['price_vat'] - proforma_assigns['sum']

        if amount > remained_income:
            raise GraphQLError('can not do that.')

        if (proforma_remained - amount) <= 0:
            raise GraphQLError('proforma amount not sufficient')

        return super().perform_mutate(form, info)


class IncomeModelMutation(object):
    income_mutation = IncomeModelFormMutation.Field()
    income_row_mutation = IncomeRowModelFormMutation.Field()
