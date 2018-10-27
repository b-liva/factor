import json

from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

import request.functions as funcs
# from request.functions import has_perm_or_is_owner
# from fund.views import has_perm_or_is_owner

from request.views import allRequests, find_all_obj
from .models import Requests
from .models import ReqSpec
from .models import Prefactor
from .models import PrefactorVerification
from .models import PrefSpec
from .models import Xpref
from pricedb.models import PriceDb
from pricedb.models import MotorDB


from .models import Payment
from .models import XprefVerf
from customer.models import Customer
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def pref_form(request):
    Reqs = Requests.objects.all()
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_xpref')
    if not can_add:
        messages.error(request, 'You have not enough access')
        return redirect('errorpage')
    return render(request, 'requests/admin_jemco/ypref/form.html', {'reqs': Reqs})


@login_required
def pref_form2(request):
    req = Requests.objects.get(number=request.POST['req_no'])
    a = req
    reqspec = a.reqspec_set.all()
    print(reqspec.count())
    return render(request, 'requests/admin_jemco/ypref/form2.html', {
        'reqspec': reqspec,
        'req_id': req.pk,
    })


@login_required
def pref_insert(request):
    # can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_xpref')
    reqs = Requests.objects.all()
    req_no = request.POST['req_no']
    print(req_no)
    xpref_no = request.POST['xpref']
    spec_prices = request.POST.getlist('price')
    spec_ids = request.POST.getlist('spec_id')
    x = 0
    xpref = Xpref.objects.filter(pk=xpref_no)
    xpref = Xpref()
    xpref.number = xpref_no
    xpref.req_id = Requests.objects.get(pk=req_no)
    xpref.date_fa = request.POST['date_fa']
    xpref.exp_date_fa = request.POST['exp_date_fa']
    xpref.owner = request.user
    xpref.save()
    for i in spec_ids:
        j = int(i)
        print(str(i) + ':' + str(spec_prices[x]))
        # r = PrefSpec.objects.filter(pk=spec_ids[x])
        spec = ReqSpec.objects.get(pk=j)

        pref_spec = PrefSpec()
        pref_spec.type = spec.type
        pref_spec.price = 0
        pref_spec.price = spec_prices[x]

        # if spec_prices[x] == '':
        # else:
        pref_spec.kw = spec.kw
        pref_spec.qty = spec.qty
        pref_spec.rpm = spec.rpm
        pref_spec.voltage = spec.voltage
        pref_spec.ip = spec.ip
        pref_spec.ic = spec.ic
        pref_spec.summary = spec.summary
        pref_spec.xpref_id = xpref
        pref_spec.owner = request.user
        pref_spec.save()
        x += 1

    return redirect('pref_form')


# @login_required
def pref_index(request):
    prefs = Xpref.objects.filter(req_id__owner=request.user).order_by('pub_date')
    prefs = Xpref.objects.all()
    print(len(prefs))
    return render(request, 'requests/admin_jemco/ypref/index.html', {
        'prefs': prefs
    })


@login_required
def pref_find(request):
    pref = Xpref.objects.get(number=request.POST['pref_no'])
    return redirect('pref_details', ypref_pk=pref.pk)


@login_required
def pref_details(request, ypref_pk):
    spec_total = 0
    proforma_total = 0
    sales_total = 0
    percentage = 0
    total_percentage = 0
    pref = Xpref.objects.get(pk=ypref_pk)
    prefspecs = pref.prefspec_set.all()

    nestes_dict = {}
    i = 0
    for prefspec in prefspecs:

        print("**" + str(prefspec.qty) + "**")
        kw = prefspec.kw
        speed = prefspec.rpm
        price = MotorDB.objects.filter(kw=kw).filter(speed=speed).last()
        print(price.sale_price)
        proforma_total += prefspec.qty * prefspec.price
        if price.prime_cost:
            sales_total += prefspec.qty * price.prime_cost
            percentage = (prefspec.price/(price.prime_cost))
        if percentage >= 1:
            percentage_class = 'good-conditions'
        else:
            percentage_class = 'bad-conditions'
        nestes_dict[i] = {
            'obj': prefspec,
            'sale_price': price.prime_cost,
            'percentage': percentage,
            'percentage_class': percentage_class,
            'spec_total': prefspec.qty * prefspec.price
        }
        i += 1
        if price.prime_cost:
            total_percentage = proforma_total/sales_total
    if total_percentage >= 1:
        total_percentage_class = 'good-conditions'
    else:
        total_percentage_class = 'bad-conditions'
    return render(request, 'requests/admin_jemco/ypref/details.html', {
        'pref': pref,
        'prefspecs': prefspecs,
        'nested': nestes_dict,
        'proforma_total': proforma_total,
        'sales_total': sales_total,
        'total_percentage': total_percentage,
        'total_percentage_class': total_percentage_class,
    })


@login_required
def pref_delete(request, ypref_pk):
    pref = Xpref.objects.get(pk=ypref_pk)
    can_del = funcs.has_perm_or_is_owner(request.user, 'request.delete_xpref', pref.req_id)

    if not can_del:
        messages.error(request, 'You have not enough access')
        return redirect('errorpage')
    pref.delete()
    return redirect('pref_index')



@login_required
def pref_edit_form(request, ypref_pk):
    proforma = Xpref.objects.get(pk=ypref_pk)
    can_edit = funcs.has_perm_or_is_owner(request.user, 'request.change_xpref', proforma.req_id)
    print(can_edit)
    if not can_edit:
        messages.error(request, 'You have not enough access')
        return redirect('errorpage')
    prof_specs = proforma.prefspec_set.all()
    return render(request, 'requests/admin_jemco/ypref/edit_form.html', {
        'proforma': proforma,
        'prof_specs': prof_specs
    })


@login_required
def pref_edit(request, ypref_pk):
    xpref = Xpref.objects.get(pk=ypref_pk)
    spec_prices = request.POST.getlist('price')
    xspec = xpref.prefspec_set.all()
    x = 0
    for item in xspec:
        item.price = spec_prices[x]
        item.save()
        x += 1
    prefspecs = xpref.prefspec_set.all()
    nestes_dict = {}
    i = 0
    for prefspec in prefspecs:
        kw = prefspec.kw
        speed = prefspec.rpm
        price = MotorDB.objects.filter(kw=kw).filter(speed=speed).last()
        percentage = (prefspec.price / (price.prime_cost))
        if percentage >= 1:
            percentage_class = 'good-conditions'
        else:
            percentage_class = 'bad-conditions'
        nestes_dict[i] = {
            'obj': prefspec,
            'sale_price': price.prime_cost,
            'percentage': percentage,
            'percentage_class': percentage_class
        }
        i += 1

    msg = 'Proforma was updated'

    return render(request, 'requests/admin_jemco/ypref/details.html', {
        'pref': xpref,
        'prefspecs': prefspecs,
        'nested': nestes_dict,
        'msg': msg
    })






    # return render(request, 'requests/admin_jemco/ypref/details.html', {
    #     'pref': xpref,
    #     'prefspecs': xspec,
    #     'msg': msg,
    # })


@login_required
def xpref_link(request, xpref_id):
    xpref = Xpref.objects.get(pk=xpref_id)
    xpref_specs = xpref.prefspec_set.all()
    return render(request, 'requests/admin_jemco/report/xpref_details.html', {
        'xpref': xpref,
        'xpref_specs': xpref_specs
    })


