import json
import jdatetime
from django.http import JsonResponse
from django.urls import reverse

from request.models import Requests


def request_index(request):
    reqs = Requests.objects.filter(is_active=True)[:100]
    reqs_count = reqs.count()
    context = {
        'reqs': [{
            'url': request.build_absolute_uri(reverse('request_details', kwargs={'request_pk': req.pk})),
            'number': req.number,
            'customer': req.customer.name,
            'details': req.request_details(),
            'total_kw': req.total_kw(),
            'owner': req.owner.last_name,
        } for req in reqs],
        'count': reqs_count,
    }
    return JsonResponse(context, safe=False)


def request_specs(request):
    data = json.loads(request.body.decode('utf-8'))
    number = int(data['number'])
    context = {}
    try:
        req = Requests.objects.get(number=number)
        specs = req.reqspec_set.all()
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
