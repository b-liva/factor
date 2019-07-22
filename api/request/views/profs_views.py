import json
import jdatetime
from django.http import JsonResponse
from django.urls import reverse

from request.models import (
    Requests, Xpref, ReqSpec,
    IMType, ICType, IEType, IPType,
    ProjectType
)


def profs_index(request):
    profs = Xpref.objects.filter(is_active=True)[:100]
    profs_count = profs.count()
    context = {
        'profs': [{
            'url': request.build_absolute_uri(reverse('pref_details', kwargs={'ypref_pk': prof.pk})),
            'number': prof.number,
            'customer': prof.req_id.customer.name,
            'owner': prof.owner.last_name,
        } for prof in profs],
        'count': profs_count,
    }
    print(context)
    return JsonResponse(context, safe=False)


def prof_specs(request):
    data = json.loads(request.body.decode('utf-8'))
    number = int(data['number'])
    context = {}
    try:
        prof = Xpref.objects.get(number=number)
        specs = prof.prefspec_set.all()
        context = {
            'specs': [{
                'qty': spec.qty,
                'kw': spec.kw,
                'voltage': spec.voltage,
                'rpm': spec.rpm,
            } for spec in specs]
        }
        print('req', context)
    except:
        msg = 'موردی یافت نشد.'
        context.update({
            'msg': msg
        })
    print('all', context)
    return JsonResponse(context, safe=False)

