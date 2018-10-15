from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from fund.models import Fund, Expense
import request.functions


@login_required
def fund_form(request):
    # fund.save()
    can_add = has_perm_or_is_owner(request.user, 'fund.add_fund')
    if can_add:
        funds = Fund.objects.all()
        btn = 'Next'
        return render(request, 'fund/form.html', {'funds': funds, 'btn': btn})
    messages.error(request, 'You have not enough access')
    return redirect('errorpage')


@login_required
def fund_insert(request):
    fund = Fund()
    if request.POST['updating']:
        fund = Fund.objects.get(pk=request.POST['fund_id'])
    fund.title = request.POST['title']
    fund.summary = request.POST['summary']
    fund.owner = request.user
    fund.save()
    return redirect('expense_form', fund_pk=fund.pk)
    # return render(request, 'fund/form.html', {'fund_id': fund_id})


@login_required
def fund_index(request):
    funds = Fund.objects.filter(owner=request.user)
    if request.user.is_superuser:
        funds = Fund.objects.all()
    amounts = {}
    for fund in funds:
        expenses = fund.expense_set.all()
        sum = 0
        for expense in expenses:
            sum += expense.amount
        amounts[sum] = fund

    return render(request, 'fund/index.html', {
        'funds': funds,
        'amounts': amounts
    })


@login_required
def fund_details(request, fund_pk):
    fund = Fund.objects.get(pk=fund_pk)
    expenses = fund.expense_set.all()
    return render(request, 'fund/details.html', {
        'fund': fund,
        'expenses': expenses,
    })


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
        messages.error(request, 'You have not enough access')
        return redirect('errorpage')


@login_required
def fund_edit(request, fund_pk):

    fund = Fund.objects.get(pk=fund_pk)
    can_edit = has_perm_or_is_owner(request.user, 'fund.change_fund', fund)
    if can_edit:

        updating = True
        btn = 'Save'
        return render(request, 'fund/form.html', {
            'updating': updating,
            'fund': fund,
            'btn': btn
        })
    else:
        messages.error(request, 'You have not enough access')
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
    messages.error(request, 'You have not enough access')
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
    pass


@login_required
def expense_find(request):
    pass


@login_required
def expense_details(request):
    pass


@login_required
def expense_delete(request, expense_pk, fund_pk):
    exp = Expense.objects.get(pk=expense_pk)
    exp.delete()
    return redirect('expense_form', fund_pk=fund_pk)


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
