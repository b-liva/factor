import json

from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

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
from .viewsFolder import permission


# Create your views here.
def errorpage(request):
    return render(request, 'fund/error.html')


def request_page(request):
    allRequests = Requests.objects.all()
    return render(request, 'requests/admin_jemco/allRequests.html', {'allRequests': allRequests})
    # return render(request, 'requests/requests.html', {'allRequests': allRequests})


def prefactors_page(request):
    allPrefactos = Prefactor.objects
    return render(request, 'requests/admin_jemco/prefactors.html', {'allPrefactors': allPrefactos})
    # return render(request, 'requests/views.html', {'allPrefactors': allPrefactos})


def prefactors_verification_page(request):
    allPrefVerifications = PrefactorVerification.objects
    return render(request, 'requests/admin_jemco/prefVerificationsPage.html',
                  {'allPrefVerifications': allPrefVerifications})
    # return render(request, 'requests/prefVerificationsPage.html', {'allPrefVerifications': allPrefVerifications})


def request_details(request, request_id):
    req = get_object_or_404(Requests, pk=request_id)
    specs = req.reqspec_set.all()
    return render(request, 'requests/admin_jemco/request/req_details.html', {'request': req, 'specs': specs})
    # return render(request, 'requests/req_details.html', {'request': req, 'specs': specs})


def prefactor_details(request, pref_id):
    pref = get_object_or_404(Prefactor, pk=pref_id)
    return render(request, 'requests/pref_details.html', {'prefactor': pref})


def pref_ver_details(request, pref_ver_id):
    pref_ver = get_object_or_404(PrefactorVerification, pk=pref_ver_id)
    return render(request, 'requests/pref_ver_details.html', {'pref_ver': pref_ver})


def allTable(request):
    # x = Requests.objects.get(pk=1)
    x2 = Requests.objects.all()
    # y = x.prefactor_set.all()
    # z = Prefactor.objects.get(pk=1).prefactorverification_set

    return render(request, 'prefactors/homepage.html', {
        'reqs': x2,
        # 'prefs': y
    })


def find_pref(request):
    pref_no = request.POST['pref_no']
    prefactor = Prefactor.objects.get(number=pref_no)
    related_request = prefactor.request_id
    pre_ver = prefactor.prefactorverification_set.all()

    return render(
        request,
        'requests/results.html',
        {'prefactor': prefactor, 'verification': pre_ver, 'related_request': related_request}
    )


# @login_required(login_url='login')
@login_required
def create_req(request):
    if request.method == 'POST':
        if request.POST['req_no']:
            print(request.POST['customer_id'])
            req = Requests()
            req.number = request.POST['req_no']
            req.summary = request.POST['req_summary']
            req.customer = Customer.objects.get(pk=request.POST['customer_id'])
            # req.image = request.FILES['req_file']
            req.pub_date = timezone.datetime.now()
            req.save()
            return redirect('create_spec', req_pk=req.pk)
        else:
            return render(request, 'requests/admin_jemco/request/create.html', {'error': 'some field is empty'})
    return render(request, 'requests/admin_jemco/request/create.html')


def create_spec(request, req_pk):
    req_obj = get_object_or_404(Requests, pk=req_pk)
    specs = req_obj.reqspec_set.all()
    # req_obj = Requests(pk=req_pk)
    print(req_obj.number)
    return render(request, 'requests/admin_jemco/request/create_spec.html', {'req_obj': req_obj, 'specs': specs})
    # return render(request, 'requests/form.html', {'req_obj': req_obj, 'specs': specs})


def edit_xspec(request, spec_pk, req_pk):
    req = Requests.objects.get(pk=req_pk)
    specs = ReqSpec.objects.filter(req_id=req)
    spec = ReqSpec.objects.get(pk=spec_pk)
    updating = True
    # specs = PrefSpec.objects.all()
    return render(request, 'requests/admin_jemco/request/create_spec.html', {
        'spec': spec,
        'specs': specs,
        'req_obj': req,
        'updating': updating
    })


def save_spec(request):
    if request.method == 'POST':
        spec = ReqSpec()
        if request.POST['updating']:
            spec = ReqSpec.objects.get(pk=request.POST['spec_pk'])

        related_req = Requests(pk=request.POST['req_id'])
        spec.req_id = related_req
        spec.qty = request.POST['qty']
        spec.type = request.POST['type']
        spec.kw = request.POST['kw']
        spec.rpm = request.POST['rpm']
        spec.voltage = request.POST['voltage']
        spec.ic = request.POST['ic']
        spec.ip = request.POST['ip']
        spec.summary = request.POST['summary']
        # if request.POST['price']:
        #     spec.price = request.POST['price']
        spec.save()
        return redirect('create_spec', req_pk=related_req.pk)


def del_spec(request, spec_id):
    # print(request.content_params)
    print(spec_id)
    spec = get_object_or_404(ReqSpec, pk=spec_id)

    req = spec.req_id
    spec.delete()
    return redirect('create_spec', req_pk=req.pk)


# @login_required
# def create_req(request):
#     if request.method == 'POST':
#         if request.POST['req_no'] and request.POST['req_summary']:
#             req = Requests()
#             req.number = request.POST['req_no']
#             req.summary = request.POST['req_summary']
#             req.image = request.FILES['req_file']
#             req.pub_date = timezone.datetime.now()
#             req.save()
#             req_spec = ReqSpec()
#             req_spec.req_id = req.number
#             req_spec.kw = request.POST['kw']
#             req_spec.rpm = request.POST['rpm']
#             req_spec.id = request.POST['id']
#             req_spec.ip = request.POST['ip']
#             req_spec.save(
#
#             )
#             return redirect('allTables')
#         else:
#             return render(request, 'requests/details.html', {'error': 'some field is empty'})
#     return render(request, 'requests/details.html')

@login_required
def create_pref(request):
    if request.method == 'POST':
        if request.POST['number'] and request.POST['summary'] and request.FILES:

            if Requests.objects.get(number=request.POST['req_number']):
                try:
                    related_req = Requests.objects.get(number=request.POST['req_number'])
                    pref = Prefactor()
                    pref.number = request.POST['number']
                    pref.request_id = related_req
                    pref.summary = request.POST['summary']
                    pref.image = request.FILES['image']
                    pref.pub_date = timezone.datetime.now()
                    pref.save()
                    return redirect('allTables')
                except Requests.DoesNotExist:
                    return render(request, 'prefactors/create.html', {'error': 'no such request'})
        else:
            list = allRequests()
            return render(request, 'prefactors/create.html', {'list': list, 'error': 'some field is empty'})
    return render(request, 'requests/admin_jemco/request/create.html')


@login_required
def createpage(request):
    req = Requests()
    customers = Customer.objects.all()
    return render(request, 'requests/admin_jemco/request/create.html', {
        'req': req,
        'customers': customers,
    })
    # return render(request, 'requests/details.html', {'req': req})


@login_required
def createprefpage(request):
    list = allRequests()
    print(list)
    return render(request, 'requests/admin_jemco/prefactor/create.html', {'list': list})
    # return render(request, 'views/details.html', {'list': list})


@login_required
def create_verf_page(request, error=''):
    list = allPref()
    return render(request, 'requests/admin_jemco/prefVerification/create.html', {'list': list, 'error': error})
    # return render(request, 'prefVerification/details.html', {'list': list, 'error': error})


def create_verf(request):
    print(request)
    if request.method == 'POST':
        if request.POST['number'] and request.POST['summary'] and request.FILES:
            if Prefactor.objects.get(number=request.POST['pref_number']):
                try:
                    related_pref = Prefactor.objects.get(number=request.POST['pref_number'])
                    verf = PrefactorVerification()
                    verf.number = request.POST['number']
                    verf.pref_id = related_pref
                    verf.summary = request.POST['summary']
                    verf.image = request.FILES['image']
                    verf.pub_date = timezone.datetime.now()
                    verf.save()
                    return redirect('allTables')
                except Prefactor.DoesNotExist:
                    return render(request, 'prefVerification/create.html', {'error': 'no such request'})
        else:
            allprefactors = allPref()
            return render(request, 'prefVerification/create.html',
                          {'error': 'some field is empty', 'list': allprefactors})
    return render(request, 'prefVerification/create.html')


def allPref():
    allPref = Prefactor.objects.all()
    list = []
    for pref in allPref:
        list.append(pref.number)
    list.sort()
    return list


def allRequests():
    allreq = Requests.objects.all()
    list = []
    for req in allreq:
        list.append(req.number)
    list.sort()
    return list


def find_total_payment():
    payments = Payment.objects.all()
    amount = 0
    for payment in payments:
        amount += payment.amount
    return amount


@login_required
def dashboard(request):
    routine_kw, project_kw, allKw = find_routine_kw()
    num_of_requests = no_of_requests()
    orders = Orders()
    last_n_requests = orders.last_orders()
    total_payments = find_total_payment()
    context = {
                      'routine_kw': intcomma(routine_kw),
                      'project_kw': intcomma(project_kw),
                      'allKw': intcomma(allKw),
                      'num_of_reqs': num_of_requests,
                      'last_n_requests': last_n_requests,
                      'total_payments': total_payments
                  }
    return render(request, 'requests/admin_jemco/dashboard.html', context)


@login_required
def dashboard2(request):
    routine_kw, project_kw, allKw = find_routine_kw()
    num_of_requests = no_of_requests()
    orders = Orders()
    last_n_requests = orders.last_orders()
    total_payments = find_total_payment()
    context = {
                      'routine_kw': intcomma(routine_kw),
                      'project_kw': intcomma(project_kw),
                      'allKw': intcomma(allKw),
                      'num_of_reqs': num_of_requests,
                      'last_n_requests': last_n_requests,
                      'total_payments': total_payments
                  }
    return render(request, 'requests/admin_jemco/dashboard2.html', context)


def no_of_requests():
    num_of_reqs = Requests.objects.all().count()
    return num_of_reqs


def find_routine_kw():
    # ReqSpec is a class and ReqSpec() is an instance of it
    # command bellow works for clas and not working for instance

    routine_specs = ReqSpec.objects.filter(kw__lte=450)
    project_specs = ReqSpec.objects.filter(kw__gt=450)
    allSpecs = ReqSpec.objects.all()
    allKw = 0
    routine_kw = 0
    project_kw = 0
    for spec in routine_specs:
        routine_kw += spec.kw * spec.qty

    for spec in project_specs:
        project_kw += spec.kw * spec.qty
    for spec in allSpecs:
        allKw += spec.kw * spec.qty

    return routine_kw, project_kw, allKw


def find_last_reqs():
    pass


def specs_of_orders(orders):
    pass


class Orders:
    def last_orders(self):
        # last_n_requests = Requests.objects.filter()[:10].order_by('pub_date').reverse()
        last_n_requests = Requests.objects.all().order_by('customer__requests__pub_date').reverse()
        return last_n_requests


def create_pref_spec(request):
    Reqs = Requests.objects.all()
    return render(request, 'requests/admin_jemco/prefactor/create_spec_pref01.html', {'reqs': Reqs})


def create_spec_pref_findReq(request):
    req = Requests.objects.get(number=request.POST['req_no'])
    # xpref = Xpref()
    # xpref.req_id = req
    # xpref.number = request.POST['pref_no']
    # xpref.save()
    # print('***&&&&****')
    # print(request.POST['req_no'])
    a = req
    reqspec = a.reqspec_set.all()
    print(reqspec.count())
    return render(request, 'requests/admin_jemco/prefactor/create_spec_pref02.html', {
        'reqspec': reqspec,
        'req_id': req.pk,
        # 'xpref_no': xpref
    })


def save_pref_spec(request):
    reqs = Requests.objects.all()
    req_no = request.POST['req_no']
    xpref_no = request.POST['xpref']
    spec_prices = request.POST.getlist('price')
    spec_ids = request.POST.getlist('spec_id')
    x = 0
    xpref = Xpref.objects.filter(pk=xpref_no)
    xpref = Xpref()
    xpref.number = xpref_no
    xpref.req_id = Requests.objects.get(pk=req_no)
    xpref.save()
    for i in spec_ids:
        j = int(i)
        print(str(i) + ':' + str(spec_prices[x]))
        # r = PrefSpec.objects.filter(pk=spec_ids[x])
        spec = ReqSpec.objects.get(pk=j)

        pref_spec = PrefSpec()
        pref_spec.type = spec.type
        if spec_prices[x] == '':
            pref_spec.price = 0
        else:
            pref_spec.price = spec_prices[x]
        pref_spec.kw = spec.kw
        pref_spec.rpm = spec.rpm
        pref_spec.voltage = spec.voltage
        pref_spec.ip = spec.ip
        pref_spec.ic = spec.ic
        pref_spec.summary = spec.summary
        pref_spec.xpref_id = xpref
        pref_spec.save()
        x += 1

    return render(request, 'requests/admin_jemco/prefactor/create_spec_pref01.html', {
        'reqs': reqs
    })


def xreq_pref_spec(request):
    xprefs = Xpref.objects.all()

    return render(request, 'requests/admin_jemco/report/report.html', {'xprefs': xprefs})


def find_xpref(request):
    # xpref_obj = Xpref()
    # if 'xpref_no' in request.POST:
    #     xpref_no = request.POST['xpref_no']
    #     xpref_obj = Xpref.objects.get(pk=xpref_no)

    xpref = Xpref.objects.get(number=request.POST['xpref_no'])
    xpref = get_object_or_404(Xpref, number=request.POST['xpref_no'])
    return render(request, 'requests/admin_jemco/prefactor/find_xpref.html', {'xpref_obj': xpref})


def xpref_link(request, xpref_id):
    xpref = Xpref.objects.get(pk=xpref_id)
    xpref_specs = xpref.prefspec_set.all()
    return render(request, 'requests/admin_jemco/report/xpref_details.html', {
        'xpref': xpref,
        'xpref_specs': xpref_specs
    })


def edit_xpref(request, xpref_id):
    xpref = Xpref.objects.get(pk=xpref_id)
    spec_prices = request.POST.getlist('price')
    xspec = xpref.prefspec_set.all()
    x = 0
    for item in xspec:
        item.price = spec_prices[x]
        item.save()
        x += 1

    msg = 'Proforma was updated'
    return render(request, 'requests/admin_jemco/report/xpref_details.html', {
        'xpref': xpref,
        'xpref_specs': xspec,
        'msg': msg,
    })


def add_payment_page(request):
    reqs, xprefs, xpayments = find_all_obj()

    return render(request, 'requests/admin_jemco/prefactor/payments/add_payment.html', {
        'reqs': reqs,
        'xprefs': xprefs,
        'xpayments': xpayments
    })


def add_payment(request):
    xpref = Xpref.objects.get(pk=request.POST['xpref_no'])
    payment = Payment()
    payment.xpref_id = xpref
    payment.amount = request.POST['amount']
    payment.number = request.POST['number']
    payment.summary = request.POST['summary']
    payment.save()
    msg = 'payment added successfully'

    reqs, xprefs, xpayments = find_all_obj()

    return render(request, 'requests/admin_jemco/prefactor/payments/add_payment.html', {
        'msg': msg,
        'reqs': reqs,
        'xprefs': xprefs,
        'xpayments': xpayments
    })


def payments(request):
    payments = Payment.objects.all()
    return render(request, 'requests/admin_jemco/prefactor/payments/payments.html', {'payments': payments})


def find_all_obj():
    reqs = Requests.objects.all()
    xprefs = Xpref.objects.all()
    xpayment = Payment.objects.all()
    return reqs, xprefs, xpayment


@login_required
def xpref_ver_create(request, error=''):
    xprefs = Xpref.objects.all()
    return render(request, 'requests/admin_jemco/prefactor/verifications/create.html', {
        'xprefs': xprefs, 'error': error
    })


def create_xverf(request):
    if request.method == 'POST':
        if request.POST['number'] and request.POST['summary']:
            print(request.POST['xpref_id'])
            if Xpref.objects.get(pk=request.POST['xpref_id']):
                try:
                    related_pref = Xpref.objects.get(pk=request.POST['xpref_id'])
                    verf = XprefVerf()
                    verf.number = request.POST['number']
                    verf.xpref = related_pref
                    verf.summary = request.POST['summary']
                    # verf.image = request.FILES['image']
                    # verf.pub_date = timezone.datetime.now()
                    verf.save()
                    msg = 'verification saved successfully'
                    xprefs = Xpref.objects.all()
                    # return redirect('create_verf_page')
                    return render(request, 'requests/admin_jemco/prefactor/verifications/create.html', {
                        'msg': msg,
                        'xprefs': xprefs
                    })
                except Prefactor.DoesNotExist:
                    return render(request, 'prefVerification/create.html', {'error': 'no such request'})
        else:
            allprefactors = allPref()
            return render(request, 'prefVerification/create.html',
                          {'error': 'some field is empty', 'list': allprefactors})
    return render(request, 'prefVerification/create.html')
