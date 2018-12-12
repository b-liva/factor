# from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from fund.models import Fund, Expense
from . import forms
import request.templatetags.functions as funcs
from django.contrib import messages

import jdatetime


@login_required
def fund_index(request):
    # can_view = has_perm_or_is_owner(request.user, 'fund.view_fund')
    can_view = has_perm_or_is_owner(request.user, 'fund.index_fund')
    if not can_view:
        messages.error(request, 'no access')
        return redirect('errorpage')
    funds = Fund.objects.filter(owner=request.user).order_by('date_fa')
    if request.user.is_superuser:
        # funds = Fund.objects.all().order_by('pk').reverse()
        funds = Fund.objects.all().order_by('date_fa').reverse()
    amounts = {}
    for fund in funds:
        expenses = fund.expense_set.all()
        sum = 0
        for expense in expenses:
            sum += expense.amount
        # amounts[sum] = fund
        amounts[fund] = sum

    context = {
        'funds': funds,
        'amounts': amounts
    }
    return render(request, 'fund/index.html', context)


@login_required
def fund_index2(request):
    # can_view = has_perm_or_is_owner(request.user, 'fund.view_fund')
    can_view = has_perm_or_is_owner(request.user, 'fund.index_fund')
    if not can_view:
        messages.error(request, 'no access')
        return redirect('errorpage')
    funds = Fund.objects.filter(owner=request.user).order_by('date_fa')
    if request.user.is_superuser:
        funds = Fund.objects.all().order_by('pk').reverse()
    amounts = {}
    for fund in funds:
        expenses = fund.expense_set.all()
        sum = 0
        for expense in expenses:
            sum += expense.amount
        # amounts[sum] = fund
        amounts[fund] = sum

    context = {
        'funds': funds,
        'amounts': amounts
    }
    return render(request, 'fund/api/index2.html', context)


@login_required
def fund_details(request, fund_pk):
    fund = Fund.objects.get(pk=fund_pk)
    can_read = funcs.has_perm_or_is_owner(request.user, 'view_fund', fund)
    if not can_read:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')
    expenses = fund.expense_set.all()
    sum = 0
    for e in expenses:
        sum += e.amount
    context = {
        'fund': fund,
        'expenses': expenses,
        'amount_sum': sum
    }
    return render(request, 'fund/details.html', context)


@login_required
def fund_find(request):
    fund = Fund.objects.get(pk=request.POST['fund_pk'])

    return redirect('fund_details', fund_pk=fund.pk)


@login_required
def fund_delete(request, fund_pk):
    fund = Fund.objects.get(pk=fund_pk)
    can_delete = has_perm_or_is_owner(request.user, 'fund.delete_fund', fund)
    if can_delete:
        fund.delete()
        return redirect('fund_index')
    else:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')


@login_required
def expense_form(request, fund_pk):
    fund = Fund.objects.get(pk=fund_pk)
    can_add = has_perm_or_is_owner(request.user, 'expense.add_expense', fund)
    if can_add:
        expenses = fund.expense_set.all()
        sum = 0
        for exp in expenses:
            sum += exp.amount

        return render(request, 'fund/expense/form.html', {
            'fund_pk': fund_pk,
            'expenses': expenses,
            'sum': sum
        })
    messages.error(request, 'عدم دسترسی کافی')
    return redirect('errorpage')


@login_required
def expense_insert(request):

    expense = Expense()
    if request.POST['updating']:
        expense = Expense.objects.get(pk=request.POST['expense_id'])
    fund = Fund.objects.get(pk=request.POST['fund_id'])
    expense.title = request.POST['title']
    expense.amount = request.POST['amount']
    expense.summary = request.POST['summary']
    expense.fund = fund
    expense.save()

    # funds = Fund.objects.all()
    return redirect('expense_form', fund_pk=request.POST['fund_id'])


@login_required
def expense_index(request):
    can_view = has_perm_or_is_owner(request.user, 'fund.view_expense')
    if not can_view:
        messages.error(request, 'no access')
        return redirect('errorpage')
    pass


@login_required
def expense_find(request):
    pass


@login_required
def expense_details(request, fund_pk, expense_pk):
    if not Expense.objects.filter(pk=expense_pk):
        messages.error(request, 'no such expese')
        return redirect('errorpage')

    exp = Expense.objects.get(pk=expense_pk)
    fund = exp.fund
    context = {
        'expense': exp,
        'fund': fund
    }
    return render(request, 'fund/expense/details.html', context)


@login_required
def expense_delete(request, expense_pk, fund_pk):
    exp = Expense.objects.get(pk=expense_pk)
    exp.delete()
    # return redirect('expense_form', fund_pk=fund_pk)
    return redirect('ex_form', fund_pk=fund_pk)


@login_required
def expense_edit(request, expense_pk, fund_pk):
    fund = Fund.objects.get(pk=fund_pk)
    exps = fund.expense_set.all()
    exp = Expense.objects.get(pk=expense_pk)
    updating = True
    return render(request, 'fund/expense/form.html', {
        'expense': exp,
        'expenses': exps,
        'updating': updating,
        'fund_pk': fund_pk,
    })


def has_perm_or_is_owner(user_obj, permissions, instance=None):
    if instance is not None:
        if user_obj == instance.owner:
            return True
    return user_obj.has_perm(permissions)


@login_required
def fform(request):
    can_add = has_perm_or_is_owner(request.user, 'fund.add_fund')
    if not can_add:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

    if request.method == 'POST':
        form = forms.FundForm(request.POST)
        if form.is_valid():
            fund = form.save(commit=False)
            fund.owner = request.user
            fund.save()
            return redirect('ex_form', fund_pk=fund.pk)
    else:
        form = forms.FundForm()

    return render(request, 'fund/fund_form.html', {
        'form': form
    })


@login_required
def ex_form(request, fund_pk):
    fund = Fund.objects.get(pk=fund_pk)
    amount_sum = expenses_sum(fund)

    if request.method == 'POST':
        form = forms.ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.fund = fund
            expense.save()
            return redirect('ex_form', fund_pk=fund.pk)
        else:
            messages.error(request, 'Oops, somethind in form is wrong')
            return redirect('errorpage')
    else:
        form = forms.ExpenseForm()
    expenses = Expense.objects.filter(fund=fund)

    context = {
        'form': form,
        'fund': fund,
        'amount_sum': amount_sum,
        'expenses': expenses
    }
    return render(request, 'fund/expense/expense_form.html', context)


@login_required
def fund_edit_form(request, fund_pk):
    fund_instance = Fund.objects.get(pk=fund_pk)
    can_edit = funcs.has_perm_or_is_owner(request.user, 'fund.edit_fund', fund_instance)
    if not can_edit:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')
    fund_instance.date_fa = fund_instance.date_fa.togregorian()
    form = forms.FundForm(request.POST or None, instance=fund_instance)
    if form.is_valid():
        print(f'fund is: valid')
        fund = form.save(commit=False)
        fund.save()
        return redirect('fund_index')

    context = {
        'form': form
    }
    return render(request, 'fund/fund_form.html', context)


@login_required
def expense_edit_form(request, fund_pk, expense_pk):
    fund_inst = Fund.objects.get(pk=fund_pk)
    expense_instance = Expense.objects.get(pk=expense_pk)
    # expenses = Expense.objects.filter(fund=fund_inst.pk)
    expenses = fund_inst.expense_set.all()

    amount_sum = expenses_sum(fund_inst)

    form = forms.ExpenseForm(request.POST or None, instance=expense_instance)
    fundform = forms.FundForm(request.POST or None, instance=fund_inst)

    if form.is_valid():
        exp = form.save(commit=False)
        exp.fund = fund_inst
        exp.save()
        return redirect('ex_form', fund_pk=fund_inst.pk)
    return render(request, 'fund/expense/expense_form.html', {
        'form': form,
        'fund': fund_inst,
        'expenses': expenses,
        'fundform': fundform,
        'expinst': expense_instance,
        'amount_sum': amount_sum
    })


def exedif(request):
    return HttpResponse('hello')


def expenses_sum(fund):
    expenses = fund.expense_set.all()
    amounts = []
    for e in expenses:
        amounts.append(e.amount)
    amount_sum = sum(amounts)
    return amount_sum