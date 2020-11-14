import jdatetime
from django.db.models import Count, FloatField, Sum, F
from customer.models import Customer
from request.models import PrefSpec, Payment
from .permit import base_prefspec


def customer_by_sale(days):
    prefspecs = base_prefspec(days)

    prefs_distinct = prefspecs.values('xpref_id__req_id__customer').distinct()
    values = prefs_distinct.annotate(
        amount=Sum(1.09 * F('price') * F('qty'), output_field=FloatField()),
        qty=Sum('qty'),
        customer_id=F('xpref_id__req_id__customer'),
        customer_name=F('xpref_id__req_id__customer__name')
    )
    values = values.annotate(
        debt=F('amount') - Payment.objects.filter(xpref_id__req_id__customer=F('xpref_id__req_id__customer')).aggregate(sum=Sum('amount'))['sum']
    )
    values = values.values(
        'customer_id',
        'customer_name',
        'amount',
        'qty',
        'debt'
    ).order_by('amount', 'qty').reverse()

    return values


def customer_debt(days):
    pass
