import sys

import graphene
from django.db.models import Sum
from graphql import GraphQLError
from graphene import relay
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql_relay import from_global_id

from accounts.models import User
from .forms.form import IncomeModelForm, IncomeRowModelForm
import request.templatetags.functions as funcs
from ..models import Income
from utils.graphql import utils as graphql_utils


class IncomeModelFormMutation(DjangoModelFormMutation):
    class Meta:
        form_class = IncomeModelForm

    '''
    1 - One way to make mutations work with foreign keys is to find the actual model id using from_global_id() method.
    2 - and the other way is to change to_global_id() method in a customNode and use it as the interface to prevent changing
    the id to a encoded one 
    3 - and the 3rd way is to change get_node_from_global_id() method so that id first changes to 
    model id by from_global_id() and then pass it to the super method.
    '''
    # @classmethod
    # def mutate_and_get_payload(cls, root, info, **input):
    #     print(input)
    #     customer = from_global_id(input['customer'])[1]
    #     input['customer'] = customer
    #     print(input)
    #     return super().mutate_and_get_payload(root, info, **input)

    @classmethod
    # @login_required
    def perform_mutate(cls, form, info):
        """ Checks for permission and then perform the mutate.
        :param form:
        :param info:
        :return:
        """
        owner = form.cleaned_data['owner']
        customer = form.cleaned_data['customer']
        can_add = funcs.has_perm_or_is_owner(owner, 'incomes.add_income')

        if not can_add:
            sys.tracebacklimit = -1
            # traceback.format_exc()
            raise RuntimeError('No permission to do that.')
        return super().perform_mutate(form, info)

    @classmethod
    def get_form_kwargs(cls, root, info, **input):
        owner = info.context.user
        owner = User.objects.get(pk=4)
        input['owner'] = str(owner.pk)
        attrs = ['customer', 'type']
        input = graphql_utils.from_globad_bulk(attrs, input)
        kwargs = {"data": input}

        global_id = input.pop("id", None)
        if global_id:
            node_type, pk = from_global_id(global_id)
            instance = cls._meta.model._default_manager.get(pk=pk)
            kwargs["instance"] = instance

        return kwargs


class IncomeRowModelFormMutation(DjangoModelFormMutation):
    class Meta:
        form_class = IncomeRowModelForm

    @classmethod
    def perform_mutate(cls, form, info):
        # todo: every perform_update override can lead to an update problem although it works on creation.
        owner = form.cleaned_data['owner']
        can_add = funcs.has_perm_or_is_owner(owner, 'incomes.add_incomerow')
        print(owner, can_add)
        if not can_add:
            sys.tracebacklimit = -1
            raise GraphQLError('No permission to do that.')

        proforma = form.cleaned_data['proforma']
        income = form.cleaned_data['income']
        amount = form.cleaned_data['amount']
        print(proforma)
        print(income)
        print(amount)
        if proforma.req_id.customer != income.customer:
            sys.tracebacklimit = -1
            raise GraphQLError("customer mismatch")
        # TODO: two checks should be done.
        # 1- sum of income rows shouldn't be more than income amount,
        # 2- proforma income rows sum should be less than proforma amount

        proforma_assigns = proforma.incomerow_set.aggregate(sum=Sum('amount'))
        if proforma_assigns['sum'] is None:
            proforma_assigns['sum'] = 0
        print(proforma_assigns)
        income_assings = income.incomerow_set.aggregate(sum=Sum('amount'))
        if income_assings['sum'] is None:
            income_assings['sum'] = 0
        remained_income = income.amount - income_assings['sum']
        print(remained_income)
        proforma_remained = proforma.total_proforma_price_vat()['price_vat'] - proforma_assigns['sum']
        print(proforma_remained)

        if amount > remained_income:
            raise GraphQLError('مبلغ بزرگتر از مانده دریافتی')

        if (proforma_remained - amount) <= 0:
            raise GraphQLError('proforma amount not sufficient')

        return super().perform_mutate(form, info)

    @classmethod
    def get_form_kwargs(cls, root, info, **input):
        owner = info.context.user
        owner = User.objects.get(pk=4)
        input['owner'] = str(owner.pk)
        attrs = ['income', 'proforma']
        input = graphql_utils.from_globad_bulk(attrs, input)
        kwargs = {"data": input}

        global_id = input.pop("id", None)
        if global_id:
            node_type, pk = from_global_id(global_id)
            instance = cls._meta.model._default_manager.get(pk=pk)
            kwargs["instance"] = instance

        return kwargs


class DeleteIncome(relay.ClientIDMutation):

    class Input:
        income_id = graphene.ID()

    msg = graphene.String()
    number = graphene.Int()

    @classmethod
    def mutate_and_get_payload(cls, root, info, income_id):
        pid = from_global_id(income_id)[1]
        income = Income.objects.get(pk=pid)
        income.delete()
        return cls(
            msg=f"واریزی شماره {income.number} با موفقیت حذف گردید.",
            number=income.number
        )


class IncomeModelMutation(object):
    income_mutation = IncomeModelFormMutation.Field()
    income_row_mutation = IncomeRowModelFormMutation.Field()
    delete_income = DeleteIncome.Field()
