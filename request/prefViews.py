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


def pref_form(request):
    Reqs = Requests.objects.all()
    return render(request, 'requests/admin_jemco/ypref/form.html', {'reqs': Reqs})


def pref_form2(request):
    req = Requests.objects.get(number=request.POST['req_no'])
    a = req
    reqspec = a.reqspec_set.all()
    print(reqspec.count())
    return render(request, 'requests/admin_jemco/ypref/form2.html', {
        'reqspec': reqspec,
        'req_id': req.pk,
    })


def pref_insert(request):
    reqs = Requests.objects.all()
    req_no = request.POST['req_no']
    xpref_no = request.POST['xpref']
    spec_prices = request.POST.getlist('price')
    spec_ids = request.POST.getlist('spec_id')
    x = 0
    xpref = Xpref.objects.filter(pk=xpref_no)
    xpref = Xpref()
    xpref.number = xpref_no
    xpref.req_id = Requests.objects.get(pk=req_no)
    xpref.save()
    for i in spec_ids:
        j = int(i)
        print(str(i) + ':' + str(spec_prices[x]))
        # r = PrefSpec.objects.filter(pk=spec_ids[x])
        spec = ReqSpec.objects.get(pk=j)

        pref_spec = PrefSpec()
        pref_spec.type = spec.type
        if spec_prices[x] == '':
            pref_spec.price = 0
        else:
            pref_spec.price = spec_prices[x]
        pref_spec.kw = spec.kw
        pref_spec.rpm = spec.rpm
        pref_spec.voltage = spec.voltage
        pref_spec.ip = spec.ip
        pref_spec.ic = spec.ic
        pref_spec.summary = spec.summary
        pref_spec.xpref_id = xpref
        pref_spec.save()
        x += 1

    return redirect('pref_form')


def pref_index(request):
    prefs = Xpref.objects.all()
    print(len(prefs))
    return render(request, 'requests/admin_jemco/ypref/index.html', {'prefs': prefs})

def pref_find(request):
    pref = Xpref.objects.get(number=request.POST['pref_no'])
    return redirect('pref_details', ypref_pk=pref.pk)
def pref_details(request, ypref_pk):
    pref = Xpref.objects.get(pk=ypref_pk)
    return render(request, 'requests/admin_jemco/ypref/details.html', {'pref': pref})


def pref_delete(request, ypref_pk):
    pref = Xpref.objects.get(pk=ypref_pk)
    pref.delete()
    return redirect('pref_index')


def pref_edit(request, ypref_pk):
    pass
