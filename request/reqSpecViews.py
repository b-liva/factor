import json

from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from request.views import allRequests, find_all_obj
from .models import Requests
from .models import ReqSpec
from .models import Prefactor
from .models import PrefactorVerification
from .models import PrefSpec
from .models import Xpref
from .models import Payment
from .models import XprefVerf
from customer.models import Customer
from django.contrib.auth.decorators import login_required


# Create your views here.
def reqspec_form(request, req_pk):
    req_obj = Requests.objects.get(pk=req_pk)
    specs = req_obj.reqspec_set.all()
    return render(request, 'requests/admin_jemco/yreqspec/form.html', {'req_obj': req_obj, 'specs': specs})


def reqspec_insert(request):
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
        return redirect('reqSpec_form', req_pk=related_req.pk)


def reqspec_index(request):
    reqspecs = ReqSpec.objects.all()
    return render(request, 'requests/admin_jemco/yreqspec/index.html', {'reqspecs': reqspecs})


def reqspec_details(request, yreqSpec_pk):
    pass


def reqspec_delete(request, yreqSpec_pk, req_pk):
    reqspec = ReqSpec.objects.get(pk=yreqSpec_pk)
    req = reqspec.req_id
    reqspec.delete()
    return redirect('reqSpec_form', req_pk=req_pk)

def reqspec_edit(request, yreqSpec_pk, req_pk):
    req = Requests.objects.get(pk=req_pk)
    specs = ReqSpec.objects.filter(req_id=req)
    spec = ReqSpec.objects.get(pk=yreqSpec_pk)
    updating = True
    # specs = PrefSpec.objects.all()
    return render(request, 'requests/admin_jemco/yreqspec/form.html', {
        'spec': spec,
        'specs': specs,
        'req_obj': req,
        'updating': updating
    })
