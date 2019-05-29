import json
from django.utils.timezone import now
import request.templatetags.functions as funcs
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db import models
from django.db.models import Sum, Q, Avg, FloatField, F
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
import datetime
import jdatetime
from django.core import serializers
from .models import (
    Requests,
    ReqSpec,
    PrefSpec,
    Xpref,
    Payment,
)
from customer.models import Customer
from django.contrib.auth.decorators import login_required


# Create your views here.
def errorpage(request):
    return render(request, 'fund/error.html')


def request_details(request, request_id):
    req = get_object_or_404(Requests, pk=request_id)
    specs = req.reqspec_set.all()
    return render(request, 'requests/admin_jemco/request/req_details.html', {'request': req, 'specs': specs})
    # return render(request, 'requests/req_details.html', {'request': req, 'specs': specs})


def find_kw(spc_kw, rqs):
    for r in rqs:
        spc = r.reqspec_set.all()
        for s in spc:
            spc_kw += s.kw * s.qty
    return spc_kw


def find_proformas(amount, profs):
    for p in profs:
        prefspc = p.prefspec_set.all()
        for p in prefspc:
            amount += p.price * p.qty
        print(p)
    return amount


def find_payment(pay_amnt, pmnts):
    amount = pmnts.aggregate(amount__sum=Sum('amount'))
    if amount['amount__sum']:
        pay_amnt += amount['amount__sum']
    return pay_amnt


def kwjs(request):
    days = 30
    if request.method == "POST":
        days = int(request.POST['days'])
        print(f'request is post and days: {days}')
    today = jdatetime.date.today()
    startDate = today + jdatetime.timedelta(-days)

    requests = ReqSpec.objects\
        .filter(req_id__is_active=True, req_id__date_fa__gte=startDate, req_id__date_fa__lt=today)\
        .values('req_id__date_fa').annotate(sum=Sum(F('kw') * F('qty'), output_field=FloatField())).order_by('req_id__date_fa')

    req_kw_dict = {
        str(x['req_id__date_fa']): x['sum'] for x in requests
    }

    proformas = PrefSpec.objects.filter(xpref_id__is_active=True, xpref_id__date_fa__gte=startDate, xpref_id__date_fa__lt=today)\
        .values('xpref_id__date_fa').annotate(sum=Sum(F('price') * F('qty') * 1.09, output_field=FloatField()))\
        .order_by('xpref_id__date_fa')

    proformas_amount_dict = {
        str(x['xpref_id__date_fa']): x['sum'] for x in proformas
    }

    payments = Payment.objects.filter(is_active=True, date_fa__gte=startDate, date_fa__lt=today)\
        .values('date_fa').annotate(sum=Sum('amount'))\
        .order_by('date_fa')

    payments_amnt_dict = {
        str(x['date_fa']): x['sum'] for x in payments
    }

    data = {
        'reqs': req_kw_dict,
        'proformas': proformas_amount_dict,
        'payments': payments_amnt_dict,
    }
    return JsonResponse(data, safe=False)


def agentjs(request):
    days = 30
    if request.method == "POST":
        days = int(request.POST['days'])
    today = jdatetime.date.today()
    startDate = today + jdatetime.timedelta(-days)
    endDate = today + jdatetime.timedelta(1)

    agents_total_kw = ReqSpec.objects.values('req_id__customer', 'req_id__customer__name').filter(
        req_id__customer__agent=True).filter(req_id__date_fa__gte=startDate, req_id__date_fa__lt=endDate).distinct().annotate(
        sum=Sum(F('qty') * F('kw'), output_field=FloatField()))

    agenst_status_list = [{
        'customer_name': a['req_id__customer__name'],
        'customer': a['req_id__customer'],
        'kw': a['sum'],
    } for a in agents_total_kw]
    agent_data = {
        a['customer']: a for a in agenst_status_list
    }
    return JsonResponse(agent_data, safe=False)


@login_required
def dashboard(request):
    if request.user.is_customer:
        # return redirect('customer_dashboard', pk=request.user.pk)
        return redirect('customer_dashboard')
    if not request.user.is_superuser:
        return redirect(sales_expert_dashboard)

    agent_data = agentjs(request)

    """
        hot products
    """
    hot_products = ReqSpec.objects.exclude(Q(type__title='تعمیرات') | Q(type__title='سایر')) \
        .filter(req_id__is_active=True, kw__gt=0).values('kw', 'rpm') \
        .annotate(reqspec_qty=models.Sum('qty')).order_by('reqspec_qty').reverse()
    total_qty = hot_products.aggregate(Sum('reqspec_qty'))

    """
        Daily kw
    """
    daily_kw = ReqSpec.objects.filter(req_id__is_active=True).exclude(type__title='تعمیرات').values('req_id__date_fa') \
        .annotate(request_sum=models.Sum(models.F('kw') * models.F('qty'), output_field=models.FloatField())).order_by(
        'req_id__date_fa').reverse()
    daily_avg = daily_kw.aggregate(request_avg=models.Avg('request_sum'))
    daily_sum = daily_kw.aggregate(request_total=models.Sum('request_sum'))

    """
        Daily proformas
    """
    daily_prof_list = Xpref.objects.filter(is_active=True).values('date_fa') \
        .annotate(
        amount=models.Sum(
            1.09 * models.F('prefspec__qty') * models.F('prefspec__price'), output_field=models.IntegerField()
        )) \
        .annotate(
        count=models.Count('id'),
    ).order_by('date_fa').reverse()

    daily_prof = {
        'list': daily_prof_list,
        'sum': daily_prof_list.aggregate(sum=Sum('amount')),
        'avg': daily_prof_list.aggregate(avg=Avg('amount')),
    }

    """
        Daily Payments
    """
    daily_payments_list = Payment.objects.filter(is_active=True).values('date_fa').annotate(
        amount=models.Sum(models.F('amount'))
    ).order_by('date_fa').reverse()

    daily_payments = {
        'list': daily_payments_list,
        'sum': daily_payments_list.aggregate(sum=models.Sum('amount')),
    }

    context = {
        'agent_data': agent_data,
        'last_n_requests': Requests.actives.order_by('id').reverse()[0:50],
        'hot_products': hot_products,
        'total_qty': total_qty,
        'daily_kw': daily_kw,  # todo: rearrange this similar to proforma daily stats
        'daily_avg': daily_avg,
        'daily_sum': daily_sum,
        'daily_prof': daily_prof,
        'daily_payments': daily_payments,
    }
    return render(request, 'requests/admin_jemco/dashboard.html', context)


@login_required
def dashboard2(request):
    context = {

    }
    return render(request, 'requests/admin_jemco/dashboard/dashboard3.html', context)


@login_required
def sales_expert_dashboard(request):

    profs_to_follow_on = Xpref.objects.filter(req_id__owner=request.user, is_active=True, to_follow=True, on=True)\
        .order_by('date_modified').reverse()
    profs_to_follow_off = Xpref.objects.filter(req_id__owner=request.user, is_active=True, to_follow=True, on=False)\
        .order_by('date_modified').reverse()

    owner = request.user
    orders = Requests.objects.distinct().filter(reqspec__type__title='روتین', is_active=True)
    orders_agent = orders.filter(customer__agent=True)
    orders_customer = orders.filter(customer__agent=False)

    reqsCount = Requests.objects.filter(reqspec__type__title='روتین', is_active=True).count()
    reqsAgentCount = Requests.objects.filter(customer__agent=True, reqspec__type__title='روتین', is_active=True).count()
    reqsCustomerCount = Requests.objects.filter(customer__agent=False, reqspec__type__title='روتین',
                                                is_active=True).count()

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
        'profs_to_follow_on': profs_to_follow_on,
        'profs_to_follow_off': profs_to_follow_off,
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


def find_all_obj():
    reqs = Requests.objects.filter(is_active=True)
    xprefs = Xpref.objects.filter(is_active=True)
    xpayment = Payment.objects.filter(is_active=True)
    return reqs, xprefs, xpayment
