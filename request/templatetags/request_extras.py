import jdatetime
from django.db.models import Sum, F, FloatField, Avg, Count, Q
from django_jalali.db import models as jmodels
import base64

from django import template

from django.contrib.auth import get_user_model
User = get_user_model()
from req_track.models import ReqEntered
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
    received_amount = Payment.objects.filter(is_active=True).aggregate(sum=Sum('amount'))
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


@register.filter(name='prof_expiry')
def prof_expiry(prof):
    prof_valid = 'prof_valid'
    today_fa = jmodels.jdatetime.date.today()
    if prof.exp_date_fa < today_fa and prof.perm is False:
        prof_valid = 'prof_expired'
    return prof_valid


@register.filter(name='payments')
def payments(proforma):
    all_payments = proforma.payment_set.filter(is_active=True)
    return all_payments


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


@register.filter(name='expert_remaining_reqs_not_entered')
def expert_remaining_reqs_not_entered(account):
    reqs = ReqEntered.objects.filter(owner_text__contains=account.last_name, is_request=True, is_entered=False)
    if account.last_name=='فروغی':
        reqs = reqs.exclude(owner_text__contains='ظریف')

    return reqs.count()


@register.simple_tag()
def expert_remaining_reqs_not_entered_new(pk):
    account = User.objects.get(pk=pk)
    print(account)
    reqs = ReqEntered.objects.filter(owner_text__contains=account.last_name, is_request=True, is_entered=False)
    if account.last_name=='فروغی':
        reqs = reqs.exclude(owner_text__contains='ظریف')

    return reqs.count()


@register.filter(name='expert_reqs_entered')
def expert_reqs_entered(account):
    reqs = ReqEntered.objects.filter(owner_text__contains=account.last_name, is_request=True, is_entered=True)
    return reqs.count()


@register.filter(name='all_expert_reqs')
def all_expert_reqs(account):
    reqs = Requests.objects.filter(is_active=True, owner=account)
    return reqs.count()


@register.simple_tag()
def all_expert_reqs_new(account):
    reqs = Requests.objects.filter(is_active=True, owner=account)
    return reqs.count()


@register.filter(name='expert_reqs_percent')
def expert_reqs_percent(account):
    reqs = Requests.objects.filter(is_active=True, owner=account)
    all_reqs = Requests.objects.filter(is_active=True)
    return 100 * reqs.count() / all_reqs.count()


@register.simple_tag()
def expert_reqs_percent_new(account):
    reqs = Requests.objects.filter(is_active=True, owner=account)
    all_reqs = Requests.objects.filter(is_active=True)
    return 100 * reqs.count() / all_reqs.count()


@register.simple_tag()
def expert_reqs_noxp(account):
    date = jdatetime.date(month=10, day=1, year=1397)
    reqs = Requests.objects.filter(
        is_active=True,
        finished=False,
        date_fa__gte=date,
        owner=account,
        xpref__isnull=True
    )
    return reqs.count()


@register.simple_tag()
def total_orders_not_remaining():
    reqs = ReqEntered.objects.filter(is_request=True, is_entered=False)
    return reqs.count()


@register.simple_tag()
def total_orders_entered():
    reqs = Requests.objects.filter(is_active=True)
    return reqs.count()


@register.filter(name='proforma_details')
def proforma_details(prof_follow):
    try:
        prof = Xpref.objects.get(number=prof_follow.number)
        return prof.proforma_details()
    except:
        return 'پیش فاکتور وارد نشده'


@register.filter(name='proforma_customer')
def proforma_customer(prof_follow):
    try:
        prof = Xpref.objects.get(number=prof_follow.number)
        return prof.req_id.customer.name
    except:
        return ''


@register.simple_tag()
def invout_qty_sent(perm):
    qty = 0
    if perm is not None and perm.inv_out_perm.all().exists():
        qty = perm.inv_out_perm.all().aggregate(qty=Sum('inventoryoutspec__qty'))['qty']
    return qty


@register.simple_tag()
def invout_qty_not_sent(perm):
    qty = 0
    total = 0
    if perm:
        total = perm.qy_total()
    if perm is not None and perm.inv_out_perm.all().exists():
        qty = perm.inv_out_perm.all().aggregate(qty=Sum('inventoryoutspec__qty'))['qty']
    return total - qty


@register.simple_tag()
def perm_days_new(proforma):
    perm = proforma.perm_prof.first()
    today_fa = jmodels.jdatetime.date.today()
    date = today_fa
    qty = 0
    total = 0
    if perm:
        total = perm.qy_total()
    if perm is not None and perm.inv_out_perm.all().exists():
        qty = perm.inv_out_perm.all().aggregate(qty=Sum('inventoryoutspec__qty'))['qty']
        remaining = total - qty
        if remaining == 0 and perm.inv_out_perm.exists():
            last_invout = perm.inv_out_perm.last()
            date_values = last_invout.date.split('/')
            date = jdatetime.date(year=int(date_values[0]), month=int(date_values[1]), day=int(date_values[2]))

    diff = (proforma.due_date - date)
    warning_class = ""

    if diff.days < 0:
        warning_class = 'btn-danger'

    if 0 <= diff.days <= 31:
            warning_class = 'btn-warning'
    if diff.days > 31:
        warning_class = 'btn-success'
    context = {
        'warning_class': warning_class,
        'delay': diff.days,
    }
    print(context)
    return context
