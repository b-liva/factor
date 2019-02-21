import json
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db import models
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.timezone import now
import datetime
import jdatetime
from django.core import serializers
from .models import (
    Requests,
    ReqSpec,
    Prefactor,
    PrefactorVerification,
    PrefSpec,
    Xpref,
    Payment,
    XprefVerf
)
from customer.models import Customer
from django.contrib.auth.decorators import login_required

import request.templatetags.functions as funcs

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
    specs = ReqSpec.objects.filter(is_active=True).filter(req_id=req)
    spec = ReqSpec.objects.filter(is_active=True).get(pk=spec_pk)
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
    payments = Payment.objects.filter(is_active=True)
    amount = 0
    for payment in payments:
        amount += payment.amount
    return amount


def find_kw(spc_kw, rqs):
    for r in rqs:
        spc = r.reqspec_set.all()
        for s in spc:
            spc_kw += s.kw * s.qty
    return spc_kw


def find_proformas(amount, profs):
    # amount = 0
    # print(profs)
    for p in profs:
        prefspc = p.prefspec_set.all()
        for p in prefspc:
            amount += p.price * p.qty
        print(p)
        # amount = p.objects.aggregate(Sum('amount'))
        # print(f'amount : {amount}')
        # amount += amount
    return amount


def find_payment(pay_amnt, pmnts):
    amount = pmnts.aggregate(amount__sum=Sum('amount'))
    # print(amount)
    if amount['amount__sum']:
        pay_amnt += amount['amount__sum']
    return pay_amnt


def kwjs(request, *args, **kwargs):
    days = 30
    # print(days)
    if request.method == "POST":
        days = int(request.POST['days'])
        print(f'request is post and days: {days}')
    ntoday = datetime.date.today()
    today = jdatetime.date.today()
    startDate = today + jdatetime.timedelta(-days)
    # print(f'startDate: {startDate}')
    tdelta = 1
    endDate = startDate + jdatetime.timedelta(tdelta)
    req_nums = []
    req_nums_dict = {}
    req_kw_dict = {}
    proformas_nums_dict = {}
    proformas_amount_dict = {}
    payments_nums_dict = {}
    payments_amnt_dict = {}
    temp = 0
    temp_proforma = 0
    temp_payment = 0
    spc_kw = 0
    amnt = 0

    requests_obj_temp = Requests.objects.filter(is_active=True)
    i = 1
    for r in requests_obj_temp:
        spc = r.reqspec_set.all()
        for s in spc:
            spc_kw += s.kw * s.qty
        # print(f'#{i} - {r} - {spc_kw}')
        i += 1
    spc_kw = 0
    amnt = 0
    pay_amnt = 0
    while endDate <= today + jdatetime.timedelta(1):
        # requests = Requests.objects.filter(date_fa__range=(startDate, endDate)).count()
        # requests = Requests.objects.filter(date_fa__in=(startDate, endDate)).count()
        requests = Requests.objects.filter(is_active=True).filter(date_fa__gte=startDate).filter(
            date_fa__lt=endDate).count()
        requests_obj_temp = Requests.objects.filter(is_active=True).filter(date_fa__gte=startDate).filter(
            date_fa__lt=endDate)
        proformas = Xpref.objects.filter(is_active=True).filter(date_fa__gte=startDate).filter(
            date_fa__lt=endDate).count()
        proformas_obj_temp = Xpref.objects.filter(is_active=True).filter(date_fa__gte=startDate).filter(
            date_fa__lt=endDate)
        payments = Payment.objects.filter(is_active=True).filter(date_fa__gte=startDate).filter(
            date_fa__lt=endDate).count()
        payments_obj_temp = Payment.objects.filter(is_active=True).filter(date_fa__gte=startDate).filter(
            date_fa__lt=endDate)

        spc_kw = find_kw(spc_kw, requests_obj_temp)
        amnt = find_proformas(amnt, proformas_obj_temp)
        pay_amnt = find_payment(pay_amnt, payments_obj_temp)

        # print(f'outside amount: {pay_amnt}')

        # print(spc)
        # if spc['kw__sum']:
        #     spc_kw += spc['kw__sum']

        if len(req_nums):
            req_nums.append(req_nums[-1] + requests)
        else:
            req_nums.append(requests)
        temp += requests
        temp_proforma += proformas
        temp_payment += payments
        req_nums_dict[str(startDate)] = temp
        req_kw_dict[str(startDate)] = spc_kw
        proformas_nums_dict[str(startDate)] = temp_proforma
        proformas_amount_dict[str(startDate)] = amnt
        payments_nums_dict[str(startDate)] = temp_payment
        payments_amnt_dict[str(startDate)] = pay_amnt

        startDate = endDate
        endDate = endDate + jdatetime.timedelta(tdelta)

    # print(f'total kw: {spc_kw}')
    data = {
        'reqs': req_kw_dict,
        'proformas': proformas_amount_dict,
        'payments': payments_amnt_dict,
    }
    # print(f'data passed is: {data}')
    return JsonResponse(data, safe=False)


def agentjs(request):
    days = 30
    if request.method == "POST":
        days = int(request.POST['days'])
        print(f'request is post and days: {days}')
    today = jdatetime.date.today()
    startDate = today + jdatetime.timedelta(-days)
    endDate = today + jdatetime.timedelta(1)

    agents = Customer.objects.filter(agent=True)
    agent_data = {}
    kw_total = 0
    temp = {}
    for a in agents:
        temp = {}
        spc_kw = 0
        # reqs = a.requests_set.all()
        reqs = a.requests_set.filter(date_fa__gte=startDate).filter(date_fa__lt=endDate)
        spc_kw = find_kw(spc_kw, reqs)
        temp['kw'] = spc_kw
        js = serializers.serialize('json', [a, ])
        temp['customer_name'] = a.name
        temp['customer'] = js

        agent_data[a.pk] = temp
        # agent_data = temp

    # print(agent_data)
    return JsonResponse(agent_data, safe=False)


@login_required
def dashboard(request):
    # rq, rq_dict = kwjs()
    # rq = kwjs(),
    # print(f'requests: {rq}')
    # print(f'request dict: {rq_dict}')
    if request.user.is_customer:
        # return redirect('customer_dashboard', pk=request.user.pk)
        return redirect('customer_dashboard')
    if not request.user.is_superuser:
        return redirect(sales_expert_dashboard)
    routine_kw, project_kw, services_kw, ex_kw, allKw, qtys = find_routine_kw()
    project_kw += ex_kw
    num_of_requests = no_of_requests()
    orders = Orders()
    last_n_requests = orders.last_orders()
    # print(f'order numbers: {len(last_n_requests)}')
    total_payments = find_total_payment()

    agent_data = agentjs(request)
    tqty = ReqSpec.objects.filter(is_active=True).all()
    # hot_products = ReqSpec.objects.filter(is_active=True).filter(kw__gt=0).values('kw', 'rpm').annotate(reqspec_qty=models.Sum('qty'), perc=(models.Sum('qty')/100))\
    #     .order_by('reqspec_qty').reverse()

    """
        hot products
    """
    hot_products = ReqSpec.objects \
        .exclude(type__title='تعمیرات') \
        .exclude(type__title='سایر') \
        .filter(is_active=True) \
        .filter(kw__gt=0) \
        .values('kw', 'rpm') \
        .annotate(
        reqspec_qty=models.Sum('qty')).order_by('reqspec_qty').reverse()
    total_qty = hot_products.aggregate(models.Sum('reqspec_qty'))

    """
        Daily kw, proforma and proformas
    """
    daily_kw = ReqSpec.objects.exclude(type__title='تعمیرات').filter(is_active=True).values('req_id__date_fa').annotate(
        request_sum=models.Sum(models.F('kw') * models.F('qty'), output_field=models.FloatField())).order_by(
        'req_id__date_fa').reverse()
    daily_avg = daily_kw.aggregate(
        request_avg=models.Avg(models.F('kw') * models.F('qty'), output_field=models.FloatField()))

    daily_sum = ReqSpec.objects.exclude(type__title='تعمیرات').filter(is_active=True).values(
        'req_id__date_fa').aggregate(
        request_sum=models.Sum(models.F('kw') * models.F('qty'), output_field=models.FloatField()))
    daily_avg = daily_sum['request_sum'] / daily_kw.count()
    # daily_proformas = Requests.objects.values('date_fa').annotate(models.Sum('xpref__'))
    daily_proformas = Xpref.objects.filter(is_active=True).values('req_id__date_fa').annotate(
        count=models.Count('id')).reverse()
    # daily_prof_amounts = PrefSpec.objects.values('xpref_id__date_fa')\
    #     .annotate(count=models.Count('xpref_id')).reverse()
    daily_prof_amounts = Xpref.objects.filter(is_active=True).values('date_fa') \
        .annotate(
        count=models.Count('id'),
        # amount=PrefSpec.objects
        #         .aggregate(new_amount=models.Avg(
        #         1.09 * models.F('qty') * models.F('price'), output_field=models.IntegerField()
        #     )
        # )
    ).order_by('date_fa').reverse()
    daily_prof_amounts = daily_prof_amounts.annotate(
        amount=models.Sum(
            1.09 * models.F('prefspec__qty') * models.F('prefspec__price'), output_field=models.IntegerField()
        ))
    daily_prof2 = Xpref.objects.filter(is_active=True).values('date_fa') \
        .aggregate(
        sum=models.Sum(1.09 * models.F('prefspec__qty') * models.F('prefspec__price'),
                       output_field=models.IntegerField()),
        avg=models.Avg(1.09 * models.F('prefspec__qty') * models.F('prefspec__price'),
                       output_field=models.IntegerField())
    )

    daily_prof = PrefSpec.objects.filter(is_active=True).values('xpref_id__date_fa').annotate(
        count=models.Count(
            Xpref.objects.values('date_fa').count()
        ),
        sum=models.Sum(1.09 * models.F('qty') * models.F('price'),
                       output_field=models.IntegerField()),
    ).order_by('xpref_id__date_fa').reverse()

    date_fa = daily_prof.last()['xpref_id__date_fa']
    diff = timezone.datetime.now().date() - date_fa.togregorian()
    daily_prof2['avg_profs'] = daily_prof2['sum'] / diff.days

    daily_kw_avg = daily_prof.aggregate(avg=models.Avg('sum'))

    daily_payments = Payment.objects.filter(is_active=True).values('date_fa').annotate(
        amount=models.Sum(models.F('amount'))
    ).order_by('date_fa').reverse()

    daily_payments_sum = daily_payments.aggregate(models.Sum('amount'))

    for d in daily_payments:
        print(f"payments: {d}")

    context = {
        # 'routine_kw': intcomma(routine_kw),
        'routine_kw': routine_kw,
        'project_kw': project_kw,
        'services_kw': services_kw,
        'ex_kw': ex_kw,
        'allKw': allKw,
        'qtys': qtys,
        'num_of_reqs': num_of_requests,
        'last_n_requests': last_n_requests,
        'total_payments': total_payments,
        'agent_data': agent_data,
        'hot_products': hot_products,
        'total_qty': total_qty,
        'daily_kw': daily_kw,
        'daily_avg': daily_avg,
        'daily_proformas': daily_proformas,
        'daily_prof_amounts': daily_prof_amounts,
        'daily_prof': daily_prof,
        'daily_prof2': daily_prof2,
        'daily_kw_avg': daily_kw_avg,
        'daily_payments': daily_payments,
        'daily_payments_sum': daily_payments_sum,
        'daily_sum': daily_sum,
        # 'rq': rq,
        # 'rq_dict': rq_dict,
    }
    return render(request, 'requests/admin_jemco/dashboard.html', context)


@login_required
def dashboard2(request):
    pass


@login_required
def sales_expert_dashboard(request):
    owner = request.user
    orders = Requests.objects.distinct().filter(reqspec__type__title='روتین', is_active=True)
    orders_agent = orders.filter(customer__agent=True)
    orders_customer = orders.filter(customer__agent=False)

    reqsCount = Requests.objects.filter(reqspec__type__title='روتین', is_active=True).count()
    reqsAgentCount = Requests.objects.filter(customer__agent=True, reqspec__type__title='روتین', is_active=True).count()
    reqsCustomerCount = Requests.objects.filter(customer__agent=False, reqspec__type__title='روتین', is_active=True).count()

    qty = ReqSpec.objects.filter(type__title='روتین', req_id__is_active=True).aggregate(
        request_qty=models.Sum(models.F('qty')))
    megaWatt = ReqSpec.objects.filter(type__title='روتین', req_id__is_active=True).aggregate(
        request_qty=models.Sum(models.F('kw') * models.F('qty'), output_field=models.FloatField()))
    qty_agent = ReqSpec.objects.filter(type__title='روتین', req_id__is_active=True,
                                       req_id__customer__agent=True).aggregate(
        request_qty=models.Sum(models.F('qty')))

    megaWatt_agent = ReqSpec.objects.filter(type__title='روتین', req_id__is_active=True,
                                            req_id__customer__agent=True).aggregate(
        request_qty=models.Sum(models.F('kw') * models.F('qty'), output_field=models.FloatField()))
    qty_customer = ReqSpec.objects.filter(type__title='روتین', req_id__is_active=True,
                                          req_id__customer__agent=False).aggregate(
        request_qty=models.Sum(models.F('qty')))

    megaWatt_customer = ReqSpec.objects.filter(type__title='روتین', req_id__is_active=True,
                                               req_id__customer__agent=False).aggregate(
        request_qty=models.Sum(models.F('kw') * models.F('qty'), output_field=models.FloatField()))
    context = {
        'orders_count': orders.count(),
        'reqsCount': reqsCount,
        'count': {
            'agent': {
                'row': {
                    'value': reqsAgentCount,
                    'percent': 100 * reqsAgentCount / reqsCount,
                },
                'orders': {
                    'value': orders_agent.count(),
                    'percent': 100 * orders_agent.count() / orders.count(),
                },
            },
            'customer': {
                'row': {
                    'value': reqsCustomerCount,
                    'percent': 100 * reqsCustomerCount / reqsCount,
                },
                'orders': {
                    'value': orders_customer.count(),
                    'percent': 100 * orders_customer.count() / orders.count(),
                },
            },
            'total': {
                'orders': orders.count(),
                'row': reqsCount,
            },
        },
        'qty': {
            'agent': {
                'value': qty_agent['request_qty'],
                'percent': 100 * qty_agent['request_qty'] / qty['request_qty'],
            },
            'customer': {
                'value': qty_customer['request_qty'],
                'percent': 100 * qty_customer['request_qty'] / qty['request_qty'],
            },
            'total': qty['request_qty'],
        },
        'megaWatt': {
            'agent': {
                'value': megaWatt_agent['request_qty'],
                'percent': 100 * megaWatt_agent['request_qty'] / megaWatt['request_qty'],
            },
            'customer': {
                'value': megaWatt_customer['request_qty'],
                'percent': 100 * megaWatt_customer['request_qty'] / megaWatt['request_qty'],
            },
            'total': megaWatt['request_qty'],

        },
    }
    return render(request, 'requests/admin_jemco/dashboard/dashboard.html', context)


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
    num_of_reqs = Requests.objects.filter(is_active=True).all().count()
    return num_of_reqs


def find_routine_kw():
    # ReqSpec is a class and ReqSpec() is an instance of it
    # command bellow works for clas and not working for instance

    routine_specs = ReqSpec.objects.filter(is_active=True).filter(type__title='روتین')
    project_specs = ReqSpec.objects.filter(is_active=True).filter(type__title='پروژه')
    services_specs = ReqSpec.objects.filter(is_active=True).filter(type__title='تعمیرات')
    ex_specs = ReqSpec.objects.filter(is_active=True).filter(type__title='ضد انفجار')
    # routine_specs = ReqSpec.objects.filter(kw__lte=450)
    # project_specs = ReqSpec.objects.filter(kw__gt=450)
    allSpecs = ReqSpec.objects.filter(is_active=True).filter(is_active=True)
    allKw = 0
    routine_kw = 0
    project_kw = 0
    services_kw = 0
    ex_kw = 0
    for spec in routine_specs:
        routine_kw += spec.kw * spec.qty
    for spec in project_specs:
        project_kw += spec.kw * spec.qty
    for spec in services_specs:
        services_kw += spec.kw * spec.qty
    for spec in ex_specs:
        ex_kw += spec.kw * spec.qty
    for spec in allSpecs:
        allKw += spec.kw * spec.qty

    routine_qty = routine_specs.aggregate(models.Sum('qty'))
    project_qty = project_specs.aggregate(models.Sum('qty'))
    services_qty = services_specs.aggregate(models.Sum('qty'))

    all_qty = sum([routine_qty['qty__sum'], project_qty['qty__sum'], services_qty['qty__sum']])

    qtys = {
        'routine_qty': routine_qty,
        'project_qty': project_qty,
        'services_qty': services_qty,
        'all_qty': all_qty,
    }

    return routine_kw, project_kw, services_kw, ex_kw, allKw, qtys


def find_last_reqs():
    pass


def specs_of_orders(orders):
    pass


class Orders:
    def last_orders(self):
        # last_n_requests = Requests.objects.filter()[:10].order_by('pub_date').reverse()
        last_n_requests = Requests.objects.filter(is_active=True).order_by('date_fa').reverse()
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
    # print(reqspec.count())
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
    xpref = Xpref.objects.filter(is_active=True).filter(pk=xpref_no)
    xpref = Xpref()
    xpref.number = xpref_no
    xpref.req_id = Requests.objects.get(pk=req_no)
    xpref.save()
    for i in spec_ids:
        j = int(i)
        print(str(i) + ':' + str(spec_prices[x]))
        # r = PrefSpec.objects.filter(pk=spec_ids[x])
        spec = ReqSpec.objects.filter(is_active=True).get(pk=j)

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
    xprefs = Xpref.objects.filter(is_active=True).all()

    return render(request, 'requests/admin_jemco/report/report.html', {'xprefs': xprefs})


def find_xpref(request):
    # xpref_obj = Xpref()
    # if 'xpref_no' in request.POST:
    #     xpref_no = request.POST['xpref_no']
    #     xpref_obj = Xpref.objects.get(pk=xpref_no)

    xpref = Xpref.objects.filter(is_active=True).get(number=request.POST['xpref_no'])
    xpref = get_object_or_404(Xpref, number=request.POST['xpref_no'])
    return render(request, 'requests/admin_jemco/prefactor/find_xpref.html', {'xpref_obj': xpref})


def xpref_link(request, xpref_id):
    xpref = Xpref.objects.filter(is_active=True).get(pk=xpref_id)
    xpref_specs = xpref.prefspec_set.all()
    return render(request, 'requests/admin_jemco/report/xpref_details.html', {
        'xpref': xpref,
        'xpref_specs': xpref_specs
    })


def edit_xpref(request, xpref_id):
    xpref = Xpref.objects.filter(is_active=True).get(pk=xpref_id)
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
    xpref = Xpref.objects.filter(is_active=True).get(pk=request.POST['xpref_no'])
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
    payments = Payment.objects.filter(is_active=True)
    return render(request, 'requests/admin_jemco/prefactor/payments/payments.html', {'payments': payments})


def find_all_obj():
    reqs = Requests.objects.filter(is_active=True)
    xprefs = Xpref.objects.filter(is_active=True)
    xpayment = Payment.objects.filter(is_active=True)
    return reqs, xprefs, xpayment


@login_required
def xpref_ver_create(request, error=''):
    xprefs = Xpref.objects.filter(is_active=True)
    return render(request, 'requests/admin_jemco/prefactor/verifications/create.html', {
        'xprefs': xprefs, 'error': error
    })


def create_xverf(request):
    if request.method == 'POST':
        if request.POST['number'] and request.POST['summary']:
            print(request.POST['xpref_id'])
            if Xpref.objects.filter(is_active=True).get(pk=request.POST['xpref_id']):
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
                    xprefs = Xpref.objects.filter(is_active=True)
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
