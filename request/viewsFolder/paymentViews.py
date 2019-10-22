import xlwt
from django.core.cache import cache
import random

from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages

from customer.models import Customer
from request.forms.payment_forms import PaymentSearchForm
from request.views import find_all_obj
from request.models import Xpref
from request.models import Payment
from request import models
from django.contrib.auth.decorators import login_required
import request.templatetags.functions as funcs
from request.forms import payment_forms
from django.http import HttpResponse
from django.utils import timezone


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
def pay_form_prof(request, prof_pk):
    request.session['proforma_pk'] = prof_pk
    return redirect(pay_form)


@login_required
def pay_form(request):
    try:
        proforma = Xpref.objects.get(pk=request.POST['xpref_id'])
        can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_payment', instance=proforma)
        if not proforma.perm:
            messages.error(request, 'پیش فاکتور مورد نظر مجوز نشده و دریافتی برای آن قابل ثبت نیست.')
            # todo: this is too messy. please refactor me.
            if can_add:
                if proforma.owner == request.user:
                    return redirect('pref_details', ypref_pk=proforma.pk)
                else:
                    return redirect('payment_index')
            else:
                return redirect('errorpage')
    except:
        can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_payment')
    if not can_add:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

    img_form = payment_forms.PaymentFileForm()
    if request.method == 'POST':
        form = payment_forms.PaymentFrom(request.POST, request.FILES)
        add_img_form = payment_forms.PaymentFileForm(request.POST or None, request.FILES or None)
        files = request.FILES.getlist('image')
        if form.is_valid() and add_img_form.is_valid():
            payment = form.save(commit=False)
            payment.owner = request.user
            payment.save()
            for f in files:
                img = models.PaymentFiles(image=f, pay=payment)
                img.save()
            return redirect('payment_index')
        else:
            pass
    else:
        if 'proforma_pk' in request.session:
            data = {
                'xpref_id': request.session['proforma_pk'],
            }
            del request.session['proforma_pk']
        else:
            data = {}
        form = payment_forms.PaymentFrom(data)

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

    payment_list = Payment.objects.filter(is_active=True).order_by('date_fa', 'pk').reverse()

    if not request.method == 'POST':
        if 'payment-search-post' in request.session:
            request.POST = request.session['payment-search-post']
            request.method = 'POST'

    form = PaymentSearchForm()

    if request.method == 'POST':
        form = PaymentSearchForm(request.POST or None)
        request.session['payment-search-post'] = request.POST
        if request.POST['customer']:
            if Customer.objects.filter(name=request.POST['customer']):
                customer = Customer.objects.get(name=request.POST['customer'])
                payment_list = payment_list.filter(xpref_id__req_id__customer=customer)
            else:
                payment_list = payment_list.filter(xpref_id__req_id__customer__name__contains=request.POST['customer'])
        if request.POST['date_min']:
            payment_list = payment_list.filter(date_fa__gte=request.POST['date_min'])
        if request.POST['date_max']:
            payment_list = payment_list.filter(date_fa__lte=request.POST['date_max'])

        if request.POST['sort_by']:
            payment_list = payment_list.order_by(f"{request.POST['sort_by']}")
        if request.POST['dsc_asc'] == '2':
            payment_list = payment_list.reverse()

    elif request.method == 'GET':
        form = PaymentSearchForm()

    # payments = Payment.objects.filter(is_active=True).order_by('date_fa').reverse()
    # if not request.user.is_superuser:
    #     payments = payments.filter(Q(owner=request.user) | Q(xpref_id__req_id__colleagues=request.user) | Q(
    #         xpref_id__req_id__owner=request.user))
    #
    # if request.user.is_superuser:
    #     payments = Payment.objects.filter(is_active=True).order_by('date_fa').reverse()
    pref_sum = 0
    sum = 0
    debt_percent = 0
    for payment in payment_list:
        for spec in payment.xpref_id.prefspec_set.all():
            pref_sum += spec.price * spec.qty
        sum += payment.amount
    # considering VAT
    pref_sum *= 1.09
    debt = sum - pref_sum

    if pref_sum != 0:
        debt_percent = debt / pref_sum
    context = {
        'payments': payment_list,
        'amount_sum': sum,
        'pref_sum': pref_sum,
        'debt': debt,
        'debt_percent': debt_percent,
    }
    cache.set('payments_in_sessions', context, 300)
    context.update({
        'title': 'دریافتی ها',
        'showHide': True,
        'form': form,
    })
    return render(request, 'requests/admin_jemco/ypayment/index.html', context)


@login_required
def payment_index_cc(request):
    if 'payment-search-post' in request.session:
        request.session.pop('payment-search-post')
    return redirect('payment_index')


@login_required
def payments_export(request):
    amount_sum = ''
    try:
        context = cache.get('payments_in_sessions')
        payments = context['payments']
        amount_sum = context['amount_sum']
        pref_sum = context['pref_sum']
        debt = context['debt']
        debt_percent = context['debt_percent']
    except:
        payments = Payment.objects.filter(is_active=True)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="payments.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('مبالغ دریافتی')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = (
        'ردیف',
        'شماره پرداخت',
        'تاریخ پرداخت',
        'تاریخ سررسید',
        'مبلغ',
        'نوع سند',
        'مشتری',
        'شماره مجوز',
        'شماره پیش فاکتور',
        'شماره درخواست',
    )

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    # if request.user.is_superuser:
    #     pass
    for payment in payments:
        row_num += 1
        print(payment.type)
        type = payment.type.title if payment.type is not None else None
        due_date = str(payment.due_date) if payment.due_date is not None else None
        exportables = [
            row_num,
            payment.number,
            str(payment.date_fa),
            due_date,
            payment.amount,
            type,
            payment.xpref_id.req_id.customer.name,
            payment.xpref_id.perm_number,
            payment.xpref_id.number,
            payment.xpref_id.req_id.number,
        ]
        # exportables.append(row_num)
        # exportables.append(payment.number)
        # exportables.append(payment.xpref_id.req_id.customer.name)
        # exportables.append(payment.xpref_id.req_id.number)
        # exportables.append(payment.xpref_id.number)
        # exportables.append(payment.amount)
        # exportables.append(str(payment.date_fa))

        for col_num in range(len(exportables)):
            ws.write(row_num, col_num, exportables[col_num], font_style)
    ws.write(len(payments) + 2, 4, amount_sum)
    ws.cols_right_to_left = True
    wb.save(response)
    return response


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
    can_edit = funcs.has_perm_or_is_owner(request.user, 'request.change_payment', payment)
    if not can_edit:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')
    if payment.date_fa:
        payment.date_fa = payment.date_fa.togregorian()
    if payment.due_date:
        payment.due_date = payment.due_date.togregorian()
    form = payment_forms.PaymentFrom(request.POST or None, instance=payment)
    if form.is_valid():
        pay = form.save(commit=False)
        pay.save()
        return redirect('payment_index')
    else:
        pass

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
