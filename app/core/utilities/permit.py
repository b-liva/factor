import jdatetime
from django.db.models import Sum, F, FloatField
from request.models import PrefSpec, Payment


def base_prefspec(days):
    prefspecs = PrefSpec.objects.filter(xpref_id__is_active=True, xpref_id__perm=True)
    if days:
        today = jdatetime.date.today()
        start_date = today - jdatetime.timedelta(days)
        print(start_date)
        prefspecs = prefspecs.filter(xpref_id__date_fa__gte=start_date)
        print(prefspecs.count())
    return prefspecs


def sales_total(days):
    prefspecs = base_prefspec(days)

    total_value = prefspecs.aggregate(total=Sum(F('qty') * F('price'), output_field=FloatField()))['total']
    total_value = 0 if not total_value else total_value
    total_value = total_value * 1.09
    return total_value


def income_total(days):
    payments = Payment.objects.filter(is_active=True)

    if days:
        today = jdatetime.date.today()
        start_date = today - jdatetime.timedelta(days)
        print(start_date)
        payments = payments.filter(date_fa__gte=start_date)

    payment_amount = payments.aggregate(total=Sum('amount'))
    payment_amount = payment_amount['total']
    payment_amount = 0 if not payment_amount else payment_amount
    return payment_amount


def specs_sold_by_qty(days):
    prefspecs = base_prefspec(days)

    prefspecs = prefspecs.values('kw', 'rpm').distinct().order_by('kw', 'rpm').annotate(
        count=Sum('qty')
    ).order_by('count').reverse()
    return prefspecs
