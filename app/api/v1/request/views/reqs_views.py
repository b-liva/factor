import json
import jdatetime
from django.http import JsonResponse
from django.urls import reverse

from request.models import (
    Requests, Xpref, ReqSpec,
    IMType, ICType, IEType, IPType,
    ProjectType
)


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
    except:
        msg = 'موردی یافت نشد.'
        context.update({
            'msg': msg
        })
    return JsonResponse(context, safe=False)


def im_types(request):
    im_types = IMType.objects.all()
    ic_types = ICType.objects.all()
    ip_types = IPType.objects.all()
    ie_types = IEType.objects.all()
    project_type = ProjectType.objects.all()

    context = {
        'im_types': [{
            'title': item.title,
            'id': item.pk
        } for item in im_types],
        'ic_types': [{
            'title': item.title,
            'id': item.pk
        } for item in ic_types],
        'ip_types': [{
            'title': item.title,
            'id': item.pk
        } for item in ip_types],
        'ie_types': [{
            'title': item.title,
            'id': item.pk
        } for item in ie_types],
        'project_type': [{
            'title': item.title,
            'id': item.pk,
        } for item in project_type],
    }
    return JsonResponse(context, safe=False)
