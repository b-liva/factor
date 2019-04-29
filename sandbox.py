from django.db.models import Sum, F, FloatField, Avg, Count, Q
from django import template
from request.models import Requests, Xpref, ReqSpec, PrefSpec, Payment

register = template.Library()


@register.simple_tag()
def active_request():
    active_request = Requests.actives.all()
    # TODO: .filter(reqspec__isnull=False) can be added to the ActiveRequestManager as a part of model manager
    active_request = Requests.actives.filter(reqspec__isnull=False).distinct()

    active_specs = ReqSpec.objects.filter(req_id__is_active=True).aggregate(sum=Sum(F('kw') * F('qty'), output_field=FloatField()))
    context = {
        'active_specs_kw': active_specs['sum'],
        'active_reqs': active_request,
        'active_reqs_count': active_request.count(),
    }
    return context
