from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User
from accounts.formsDir.fbv_forms import UserEditForm
from customer.models import Customer
from customer.forms import CustomerForm, CustomerLimitedForm
import request.templatetags.functions as funcs


def user_index(request):
    users = User.objects.filter(is_customer=True)

    can_list = funcs.has_perm_or_is_owner(request.user, 'customer.index_customer')
    if not can_list:
        messages.error(request, 'متأسفانه خطایی رخ داده است.')
        return redirect('errorpage')

    context = {
        'users': users
    }
    return render(request, 'accounts/fbv/list.html', context)


def user_details(request, user_pk):

    if not User.objects.filter(pk=user_pk):
        messages.error(request, 'متأسفانه خطایی رخ داده است.')
        return redirect('errorpage')

    user = User.objects.get(pk=user_pk)

    can_read = funcs.has_perm_or_is_owner(request.user, 'customer.read_customer', user)
    if not can_read:
        messages.error(request, 'متأسفانه خطایی رخ داده است.')
        return redirect('errorpage')

    context = {
        'user_p': user
    }
    return render(request, 'accounts/fbv/details.html', context)


def user_edit(request, user_pk):
    if not User.objects.filter(pk=user_pk):
        messages.error(request, 'متأسفانه خطایی رخ داده است.')
        return redirect('errorpage')

    user = User.objects.get(pk=user_pk)
    can_edit = funcs.has_perm_or_is_owner(request.user, 'customer.edit_customer', user)
    if not can_edit:
        messages.error(request, 'متأسفانه خطایی رخ داده است.')
        return redirect('errorpage')

    if request.method == 'POST':
        form = UserEditForm(request.POST or None, instance=user)
        if form.is_valid():
            user_item = form.save(commit=False)
            # if there is a need to do something
            user_item.save()
            return redirect('fbv_account_details', user_pk=user.pk)
    if request.method == 'GET':
        form = UserEditForm(instance=user)

    context = {
        'user_p': user,
        'form': form,
    }
    return render(request, 'accounts/fbv/update.html', context)


def customer_profile(request, user_pk):
    if not User.objects.filter(pk=user_pk):
        messages.error(request, 'متأسفانه خطایی رخ داده است.')
        return redirect('errorpage')

    user = User.objects.get(pk=user_pk)
    # user = get_object_or_404(User, pk=user_pk)

    can_read = funcs.has_perm_or_is_owner(request.user, 'customer.read_customer', user)
    if not can_read:
        messages.error(request, 'متأسفانه خطایی رخ داده است.')
        return redirect('errorpage')
    customer_profile = user.customer

    context = {
        'user_p': user,
        'customer': customer_profile,
    }

    return render(request, 'accounts/fbv/customer_details.html', context)


def customer_profile_update(request, user_pk):
    if not User.objects.filter(pk=user_pk):
        messages.error(request, 'متأسفانه خطایی رخ داده است.')
        return redirect('errorpage')

    user = User.objects.get(pk=user_pk)

    can_edit = funcs.has_perm_or_is_owner(request.user, 'customer.edit_customer', user)
    if not can_edit:
        messages.error(request, 'متأسفانه خطایی رخ داده است.')
        return redirect('errorpage')

    customer = user.customer
    customer.date2 = customer.date2.togregorian()
    if request.method == 'POST':
        form = CustomerLimitedForm(request.POST or None, instance=customer)
        if form.is_valid():
            customer_item = form.save(commit=False)
            # do required stuff
            customer_item.save()
            return redirect('fbv_customer_profile', user_pk=user.pk)
    if request.method == 'GET':
        form = CustomerLimitedForm(instance=customer)

    context = {
        'customer': customer,
        'form': form
    }
    return render(request, 'accounts/fbv/customer_update.html', context)
