from django.db.models import Sum, F, FloatField, Avg, Count, Q
from django_jalali.db import models as jmodels
import base64

from django import template
from request.models import Requests, Xpref, ReqSpec, PrefSpec, Payment

register = template.Library()


@register.simple_tag()
def reqeust_of_type(project_type):
    count = {
        'count': None
    }
    if project_type != 'all':
        reqspecs = ReqSpec.objects.filter(req_id__is_active=True, type__title=project_type)
    else:
        # TODO: handle 'سایر' later
        reqspecs = ReqSpec.objects.filter(req_id__is_active=True).exclude(type__title__contains='سایر')

        # These two lines are identical
        Requests.actives.filter(reqspec__isnull=False).distinct()
        count = reqspecs.values('req_id').distinct().aggregate(count=Count('req_id'))
    kw = reqspecs.aggregate(sum=Sum(F('qty') * F('kw'), output_field=FloatField()))
    qty = reqspecs.distinct().aggregate(sum=Sum('qty'))

    context = {
        'sum_kw': kw['sum'],
        'sum_qty': qty['sum'],
        'count': count['count'],
    }
    return context


@register.simple_tag()
def total_received():
    received_amount = Payment.objects.aggregate(sum=Sum('amount'))
    return received_amount['sum']


@register.filter(name='is_sent')
def is_sent(reqspec):
    sent = False
    pref_set = reqspec.prefspec_set.filter(xpref_id__is_active=True)
    # print(f"pref specs: {pref_set}")
    for p in pref_set:
        print(f"pref: {p}")
        if p.sent:
            sent = True
    return sent


@register.filter(name='has_price')
def has_price(reqspec):
    price = False
    pref_set = reqspec.prefspec_set.filter(xpref_id__is_active=True).order_by('xpref_id__date_fa', 'pk').reverse()

    if len(pref_set):
        for p in pref_set:
            if p.price > 0:
                price = True


    # if len(pref_set):
    #     if len(pref_set) > 1:
    #         """
    #             here we should find the valid price
    #             """
    #         for p in pref_set:
    #             if p.price > 0:
    #                 price = True
    #     else:
    #         if pref_set[0].price > 0:
    #             price = True

    # if len(pref_set) > 1:
    #     pass
    # elif len(pref_set) == 0:
    #     if pref_set[0].price > 0:
    #         price = True
    # else:
    #     pass
    return price


@register.filter(name='is_cancelled')
def is_cancelled(reqspec):
    cancelled = False
    pref_set = reqspec.prefspec_set.all()
    return cancelled


@register.filter(name='has_permission')
def has_permission(reqspec):
    perm = False
    pref_set = reqspec.prefspec_set.filter(xpref_id__is_active=True).order_by('xpref_id__date_fa', 'pk').reverse()
    if len(pref_set):
        for p in pref_set:
            if p.xpref_id.perm:
                perm = True
    return perm


@register.filter(name='enc')
def enc(reqspec_pk):
    v = str(reqspec_pk)
    value = base64.b64encode(v.encode("utf-8"))
    return value


@register.filter(name='perm_warning_class')
def perm_warning_class(perm):
    today_fa = jmodels.jdatetime.date.today()
    diff = perm.due_date - today_fa
    warning_class = ""

    if diff.days <= 0:
        warning_class = 'btn-danger'

    if diff.days > 0:
        warning_class = 'btn-warning'

    if diff.days > 31:
        warning_class = 'btn-success'

    return warning_class


@register.filter(name='days')
def days(perm):
    today_fa = jmodels.jdatetime.date.today()
    diff = perm['perm'].due_date - today_fa

    return diff.days


@register.filter(name='perm_total')
def perm_total(permission):
    payments = permission.payment_set.all()
    proforma_total = pref_total_price(permission)
    return proforma_total


@register.filter(name='perm_days')
def perm_days(permission):
    today_fa = jmodels.jdatetime.date.today()
    diff = permission.due_date - today_fa
    return diff.days


@register.filter(name='date_diff')
def date_diff(date):
    today_fa = jmodels.jdatetime.date.today()
    diff = date - today_fa
    # return diff.days
    return diff.days


@register.filter(name='perm_receivable')
def perm_receivable(permission):
    payments = permission.payment_set.all()
    total_paid = payments.aggregate(Sum('amount'))
    proforma_total = pref_total_price(permission)
    print(proforma_total)
    if not total_paid['amount__sum']:
        total_paid['amount__sum'] = 0
    receivable = proforma_total - total_paid['amount__sum']
    return receivable


@register.filter(name='receivable_percent')
def perm_receivable_percent(permission):
    payments = permission.payment_set.all()
    total_paid = payments.aggregate(Sum('amount'))
    proforma_total = pref_total_price(permission)
    print(proforma_total)
    if not total_paid['amount__sum']:
        total_paid['amount__sum'] = 0
    receivable = proforma_total - total_paid['amount__sum']
    value = "Error" if proforma_total == 0 else f"{100 * receivable / proforma_total}"
    print(value)
    return value


@register.filter(name='prof_expiry')
def prof_expiry(prof):
    prof_valid = 'prof_valid'
    today_fa = jmodels.jdatetime.date.today()
    if prof.exp_date_fa < today_fa and prof.perm is False:
        prof_valid = 'prof_expired'
    return prof_valid


@register.filter(name='proformas')
def proformas(req):
    all_proformas = req.xpref_set.filter(is_active=True)
    return all_proformas


@register.filter(name='payments')
def payments(proforma):
    all_payments = proforma.payment_set.filter(is_active=True)
    return all_payments


@register.filter(name='total_kw')
def total_kw(req):
    kw = ReqSpec.objects.filter(req_id=req, is_active=True).aggregate(total=Sum(F('qty') * F('kw'), output_field=FloatField()))
    return kw['total']


@register.filter(name='total_received')
def total_received(req):
    sum = Payment.objects.filter(xpref_id__req_id=req).aggregate(Sum('amount'))
    if sum['amount__sum'] is None:
        sum['amount__sum'] = ''
    return sum['amount__sum']


@register.filter(name='total_receiveable')
def total_receiveable(req):
    total = PrefSpec.objects.filter(xpref_id__req_id=req, xpref_id__perm=True).aggregate(total_sum=Sum(F('qty') * F('price'), output_field=FloatField()))
    sum = Payment.objects.filter(xpref_id__req_id=req).aggregate(Sum('amount'))
    print(type(total['total_sum']))
    print(type(sum['amount__sum']))
    if sum['amount__sum'] is None:
        sum['amount__sum'] = 0
    if total['total_sum'] is None:
        total['total_sum'] = 0
    receiveable = 1.09 * total['total_sum'] - sum['amount__sum']
    return receiveable


@register.filter(name='qty_remaining')
def qty_remaining(permspec):
    if permspec.qty_sent is None:
        permspec.qty_sent = 0
    qty = permspec.qty - permspec.qty_sent
    return qty


@register.filter(name='perm_number')
def perm_number(perm):
    p_number = perm.perm_number if perm.perm_number is not None else ''
    return p_number


def pref_total_price(permission):
    prefs = permission.prefspec_set.all()
    proforma_total_before_tax = prefs.aggregate(total=Sum(F('qty') * F('price'), output_field=FloatField()))
    if not proforma_total_before_tax['total']:
        proforma_total_before_tax['total'] = 0
    proforma_total_after_tax = 1.09 * proforma_total_before_tax['total']
    return proforma_total_after_tax


@register.filter
def daily_kilowatt(t):
    daily_kwatt = ReqSpec.objects.exclude(type__title='تعمیرات').filter(is_active=True).values(
        'req_id__date_fa').annotate(
        request_sum=Sum(F('kw') * F('qty'), output_field=FloatField())).order_by(
        'req_id__date_fa').reverse()
    print(f"avg: {daily_kwatt.count()}")
    daily_avg = daily_kwatt.distinct().aggregate(
        request_avg=Avg(F('kw') * F('qty'), output_field=FloatField()))
    # print(f"daily_kilowatt: {daily_kwatt['request_sum']}")
    return daily_avg['request_avg']


@register.filter(name='flag')
def flag(payment):
    flag_value = 'red_flag' if payment.red_flag else ''
    return flag_value


@register.filter(name='highlight_class')
def highlight_class(proforma):
    flag_value = ''
    if proforma.is_entered:
        flag_value = 'green_flag'
    elif proforma.red_flag:
        flag_value = 'red_flag'
    return flag_value
