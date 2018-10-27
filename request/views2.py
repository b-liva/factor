import json

from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages


from request.views import allRequests, find_all_obj
from .models import Requests
from .models import ReqSpec
from .models import Prefactor
from .models import PrefactorVerification
from .models import PrefSpec
from .models import Xpref
from .models import Payment
from .models import XprefVerf
from customer.models import Customer
from django.contrib.auth.decorators import login_required
import request.functions as funcs

from . import views

# Create your views here.


@login_required
# add a new request to the system
def request_form(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_request')
    if not can_add:
        messages.error(request, 'Sorry, You need some priviliges to do this.')
        return redirect('errorpage')
    req = Requests()
    customers = Customer.objects.all()
    return render(request, 'requests/admin_jemco/yrequest/form.html', {
        'req': req,
        'customers': customers,
    })


@login_required
def request_insert(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_request')
    if not can_add:
        messages.error(request, 'No Priviliges')
        return redirect('errorpage')
    if request.method == 'POST':
        if request.POST['req_no']:
            req = Requests()
            req.number = request.POST['req_no']
            req.summary = request.POST['req_summary']
            req.date_fa = request.POST['date_fa']
            req.customer = Customer.objects.get(pk=request.POST['customer_id'])
            req.image = request.FILES['req_file']
            req.owner = request.user
            req.pub_date = timezone.datetime.now()
            req.save()
            return redirect('reqSpec_form', req_pk=req.pk)
        else:
            return render(request, 'requests/admin_jemco/yrequest/form.html', {'error': 'some field is empty'})
    return render(request, 'requests/admin_jemco/yrequest/form.html')


@login_required
def request_index(request):
    # requests = Requests.objects.all()
    requests = Requests.objects.filter(owner=request.user)
    return render(request, 'requests/admin_jemco/yrequest/index.html', {'all_requests': requests})


@login_required
def request_find(request):
    req = Requests.objects.get(number=request.POST['req_no'])
    return redirect('request_details', request_pk=req.pk)


@login_required
def request_read(request, request_pk):
    req = Requests.objects.get(pk=request_pk)
    reqspecs = req.reqspec_set.all()
    kw = total_kw(request_pk)

    return render(request, 'requests/admin_jemco/yrequest/details.html', {
        'request': req,
        'reqspecs': reqspecs,
        'total_kw': kw
    })


@login_required
def request_delete(request, request_pk):
    req = Requests.objects.get(pk=request_pk)
    req.delete()
    return redirect('request_index')


@login_required
def request_edit(request, request_pk):
    return HttpResponse('request Edit' + str(request_pk))


@login_required
def pref_add(request):
    return render(request, 'test.html', {'is_add': True})


@login_required
def pref_insert(request):
    print('added to the db...')
    return render(request, 'test.html', {'is_add': True})


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

    payments = Payment.objects.all()
    return render(request, 'requests/admin_jemco/ypayment/index.html', {
        'msg': msg,
        'reqs': reqs,
        'xprefs': xprefs,
        'xpayments': xpayments,
        'payments': payments
    })


@login_required
def payment_index(request):
    payments = Payment.objects.all()
    pref_sum = 0
    sum = 0

    for payment in payments:
        for spec in payment.xpref_id.prefspec_set.all():
            pref_sum += spec.price
        sum += payment.amount
    debt = sum - pref_sum
    debt_percent = debt / pref_sum
    return render(request, 'requests/admin_jemco/ypayment/index.html', {
        'payments': payments,
        'amount_sum': sum,
        'pref_sum': pref_sum,
        'debt': debt,
        'debt_percent': debt_percent,
    })


@login_required
def payment_find(request):
    payment = Payment.objects.get(number=request.POST['payment_no'])
    return redirect('payment_details', ypayment_pk=payment.pk)


@login_required
def payment_details(request, ypayment_pk):
    payment = Payment.objects.get(pk=ypayment_pk)
    return render(request, 'requests/admin_jemco/ypayment/payment_details.html', {'payment': payment})


@login_required
def payment_delete(request, ypayment_pk):
    payment = Payment.objects.get(pk=ypayment_pk)
    can_delete = funcs.has_perm_or_is_owner(request.user, 'request.delete_payment', payment)
    if not can_delete:
        messages.error(request, 'No access!')
        return redirect('errorpage')
    payment.delete()
    payments = Payment.objects.all()
    msg = 'payment deleted successfully...'
    # return render(request, 'requests/admin_jemco/ypayment/index.html', {'payments': payments, 'msg':msg})
    return redirect('payment_index')


@login_required
def payment_edit(request, ypayment_pk):
    payment = Payment.objects.get(pk=ypayment_pk)
    can_edit = funcs.has_perm_or_is_owner(request.user, 'request.edit_payment', payment)
    if not can_edit:
        messages.error(request, 'No access for you')
        return redirect('errorpage')
    return HttpResponse('payment payment_edit')


# add spec to the prefactor
@login_required
def pref_spec_add(request):
    return HttpResponse('prefactor spec add')


@login_required
def pref_spec_details(request, ypref_spec_pk):
    return HttpResponse('prefactor spec details')


@login_required
def pref_spec_del(request, ypref_spec_pk):
    return HttpResponse('prefactor spec delete')


@login_required
def pref_spec_edit(request, ypref_spec_pk):
    return HttpResponse('prefactor spec edit')


@login_required
def pref(request, ypref_pk):
    if request.method == 'POST':
        if '_METHOD' not in request.POST:
            # Do post request
            return HttpResponse('this is a post request')
        else:
            if request.POST['_METHOD'] == 'PUT':
                # Do put request
                return HttpResponse('this is a put request')
            elif request.POST['_METHOD'] == 'DELETE':
                return HttpResponse('this is a delete request')

    elif request.method == 'GET':
        list = allRequests()
        return render(request, 'test.html', {
            'ypref_pk': ypref_pk,
            'is_add': False,
        })
        # return render(request, 'requests/admin_jemco/prefactor/create2.html', {
        #     'list': list,
        #     'ypref_pk': ypref_pk
        # })
        # return render(request, 'test.html', {'ypref_pk': ypref_pk})


    # return HttpResponse('this is from a single line of code for: ' + str(ypref_ipk))



def total_kw(req_id):
    req = Requests.objects.get(pk=req_id)
    reqspecs = req.reqspec_set.all()
    total_kw = 0
    for reqspec in reqspecs:
        total_kw += reqspec.kw * reqspec.qty
    return total_kw

