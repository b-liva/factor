import random

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages

from request.views import find_all_obj
from request.models import Xpref
from request.models import Payment
from request import models
from django.contrib.auth.decorators import login_required
import request.templatetags.functions as funcs
from request.forms import payment_forms


# add payment to the prefactor
@login_required
def payment_form(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_payment')
    if not can_add:
        messages.error(request, 'Sorry, No way to access')
        return redirect('errorpage')
    reqs, xprefs, xpayments = find_all_obj()
    return render(request, 'requests/admin_jemco/ypayment/form.html', {
        'reqs': reqs,
        'xprefs': xprefs,
        'xpayments': xpayments
    })


@login_required
def pay_form(request):
    img_form = payment_forms.PaymentFileForm()
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_payment')
    if not can_add:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')
    if request.method == 'POST':
        form = payment_forms.PaymentFrom(request.POST, request.FILES)
        add_img_form = payment_forms.PaymentFileForm(request.POST or None, request.FILES or None)
        files = request.FILES.getlist('image')
        print(f'files are: {files}')
        if form.is_valid() and add_img_form.is_valid():
            print('forms are valid')
            payment = form.save(commit=False)
            payment.owner = request.user
            payment.customer = payment.xpref_id.req_id.customer
            payment.save()
            print(f'payment id is: {payment.pk}')
            for f in files:
                img = models.PaymentFiles(image=f, pay=payment)
                img.save()
            return redirect('payment_index')
        else:
            print('forms are not valid')
    else:
        form = payment_forms.PaymentFrom()

    payments = Payment.objects.filter(is_active=True)
    return render(request, 'requests/admin_jemco/ypayment/payment_form.html', {
        'form': form,
        'img_form': img_form,
        'xpayments': payments
    })


@login_required
def payment_insert(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_payment')
    if not can_add:
        messages.error(request, 'Sorry, No way to access')
        return redirect('errorpage')

    xpref = Xpref.objects.get(number=request.POST['xpref_no'])
    payment = Payment()
    payment.xpref_id = xpref
    payment.amount = request.POST['amount']
    payment.number = request.POST['number']
    payment.date_fa = request.POST['date_fa']
    payment.summary = request.POST['summary']
    payment.owner = request.user
    payment.customer = xpref.req_id.customer
    payment.save()
    msg = 'payment added successfully'

    reqs, xprefs, xpayments = find_all_obj()

    payments = Payment.objects.filter(is_active=True)
    return render(request, 'requests/admin_jemco/ypayment/index.html', {
        'msg': msg,
        'reqs': reqs,
        'xprefs': xprefs,
        'xpayments': xpayments,
        'payments': payments
    })


@login_required
def payment_index(request):

    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_payment')
    if not can_add:
        messages.error(request, 'Sorry, No way to access')
        return redirect('errorpage')

    # payments = Payment.objects.all().order_by('date_fa').reverse()
    payments = Payment.objects.filter(is_active=True, owner=request.user).order_by('date_fa').reverse()
    if request.user.is_superuser:
        payments = Payment.objects.filter(is_active=True).order_by('date_fa').reverse()
    pref_sum = 0
    sum = 0
    debt_percent = 0
    for payment in payments:
        for spec in payment.xpref_id.prefspec_set.all():
            pref_sum += spec.price * spec.qty
        sum += payment.amount
    # considering VAT
    pref_sum *= 1.09
    debt = sum - pref_sum

    if pref_sum != 0:
        debt_percent = debt / pref_sum

    context = {
        'payments': payments,
        'amount_sum': sum,
        'pref_sum': pref_sum,
        'debt': debt,
        'debt_percent': debt_percent,
        'title': 'پرداخت ها',
        'showHide': True,
    }
    return render(request, 'requests/admin_jemco/ypayment/index.html', context)


@login_required
def payment_index_deleted(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.index_deleted_payment')
    if not can_add:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

    # payments = Payment.objects.all().order_by('date_fa').reverse()
    payments = Payment.objects.filter(is_active=False, owner=request.user).order_by('date_fa').reverse()
    if request.user.is_superuser:
        payments = Payment.objects.filter(is_active=False).order_by('date_fa').reverse()
    pref_sum = 0
    sum = 0
    debt_percent = 0
    for payment in payments:
        for spec in payment.xpref_id.prefspec_set.all():
            pref_sum += spec.price * spec.qty
        sum += payment.amount
    # considering VAT
    pref_sum *= 1.09
    debt = sum - pref_sum

    if pref_sum != 0:
        debt_percent = debt / pref_sum

    context = {
        'payments': payments,
        'amount_sum': sum,
        'pref_sum': pref_sum,
        'debt': debt,
        'debt_percent': debt_percent,
        'title': 'پرداخت های حذف شده',
        'showHide': False,
    }
    return render(request, 'requests/admin_jemco/ypayment/index.html', context)


@login_required
def payment_find(request):
    if not request.POST['payment_no']:
        return redirect('payment_index')
    if not Payment.objects.filter(number=request.POST['payment_no']):
        messages.error(request, 'پرداخت مورد نظر یافت نشد')
        return redirect('payment_index')
    payment = Payment.objects.filter(is_active=True).get(number=request.POST['payment_no'])
    return redirect('payment_details', ypayment_pk=payment.pk)


@login_required
def payment_details(request, ypayment_pk):
    if not Payment.objects.filter(is_active=True).filter(pk=ypayment_pk) and not request.user.is_superuser:
        messages.error(request, 'صفحه مورد نظر یافت نشد')
        return redirect('errorpage')
    payment = Payment.objects.get(pk=ypayment_pk)
    can_read = funcs.has_perm_or_is_owner(request.user, 'request.read_payment', payment)
    if not can_read:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')
    images = models.PaymentFiles.objects.filter(pay=payment)
    context = {
        'payment': payment,
        'images': images,
    }
    return render(request, 'requests/admin_jemco/ypayment/payment_details.html', context)


@login_required
def payment_delete(request, ypayment_pk):
    payment = Payment.objects.get(pk=ypayment_pk)
    can_delete = funcs.has_perm_or_is_owner(request.user, 'request.delete_payment', payment)
    if not can_delete:
        messages.error(request, 'No access!')
        return redirect('errorpage')
    if request.method == 'GET':
        context = {
            'id': payment.pk,
            'fn': 'payment_del',
        }
        return render(request, 'general/confirmation_page.html', context)
    elif request.method == 'POST':
        # payment.delete()
        payment.is_active = False
        payment.temp_number = payment.number
        rand_num = random.randint(100000, 200000)
        while Payment.objects.filter(number=rand_num):
            rand_num = random.randint(100000, 200000)
        payment.number = rand_num
        payment.save()
    payments = Payment.objects.filter(is_active=True)
    msg = 'payment deleted successfully...'
    # return render(request, 'requests/admin_jemco/ypayment/index.html', {'payments': payments, 'msg':msg})
    return redirect('payment_index')


@login_required
def payment_edit(request, ypayment_pk):
    # 1- check for permissions
    # 2 - find proforma and related images and specs
    # 3 - make request image form
    # 4 - prepare image names to use in template
    # 5 - get the list of files from request
    # 6 - if form is valid the save request and its related images
    # 7 - render the template file
    payment = Payment.objects.filter(is_active=True).get(pk=ypayment_pk)
    can_edit = funcs.has_perm_or_is_owner(request.user, 'request.edit_payment', payment)
    if not can_edit:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')
    if payment.date_fa:
        payment.date_fa = payment.date_fa.togregorian()
    form = payment_forms.PaymentFrom(request.POST or None, instance=payment)
    if form.is_valid():
        print('form is valid')
        pay = form.save(commit=False)
        pay.save()
        return redirect('payment_index')
    else:
        print('payment form is not valid')

    return render(request, 'requests/admin_jemco/ypayment/payment_form.html', {
        'form': form,
    })


def testimage(request):
    payment = models.Payment.objects.filter(is_active=True).last()
    form = payment_forms.PaymentFileForm()
    files = False
    if request.method == 'POST':
        files = request.FILES.getlist('image')
        print(f'files: {files} and paymentis: {payment}')
        if form.is_valid():
            for f in files:
                img = models.PaymentFiles(image=f, payment=payment)
                img.save()
            return redirect('testimage')

    return render(request, 'requests/admin_jemco/ypayment/test.html', {
        'form': form,
        'payment': payment,
        'fiels': files
    })