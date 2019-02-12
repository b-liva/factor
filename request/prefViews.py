from django.contrib import messages
from django.shortcuts import render, redirect

import request.templatetags.functions as funcs
# from request.functions import has_perm_or_is_owner
# from fund.views import has_perm_or_is_owner

from .models import Requests
from .models import ReqSpec
from .models import PrefSpec
from .models import Xpref

from request.forms import forms
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def pref_form(request):
    Reqs = Requests.objects.filter(is_active=True)
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_xpref')
    if not can_add:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')
    return render(request, 'requests/admin_jemco/ypref/form.html', {'reqs': Reqs})


@login_required
def pref_form2(request):
    req = Requests.objects.filter(is_active=True).get(number=request.POST['req_no'])
    a = req
    reqspec = a.reqspec_set.filter(is_active=True)
    print(reqspec.count())
    return render(request, 'requests/admin_jemco/ypref/form2.html', {
        'reqspec': reqspec,
        'req_id': req.pk,
    })


@login_required
def pref_insert(request):
    # can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_xpref')
    reqs = Requests.objects.filter(is_active=True)
    req_no = request.POST['req_no']
    print(req_no)
    xpref_no = request.POST['xpref']
    spec_prices = request.POST.getlist('price')
    spec_ids = request.POST.getlist('spec_id')
    x = 0
    xpref = Xpref.objects.filter(is_active=True).filter(pk=xpref_no)
    xpref = Xpref()
    xpref.number = xpref_no
    xpref.req_id = Requests.objects.filter(is_active=True).get(pk=req_no)
    xpref.date_fa = request.POST['date_fa']
    xpref.exp_date_fa = request.POST['exp_date_fa']
    xpref.owner = request.user
    xpref.save()
    for i in spec_ids:
        j = int(i)
        print(str(i) + ':' + str(spec_prices[x]))
        # r = PrefSpec.objects.filter(pk=spec_ids[x])
        spec = ReqSpec.objects.filter(is_active=True).get(pk=j)

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


@login_required
def pref_edit_form(request, ypref_pk):
    if not Xpref.objects.filter(is_active=True).filter(pk=ypref_pk):
        messages.error(request, 'no Proforma')
        return redirect('errorpage')
    proforma = Xpref.objects.filter(is_active=True).get(pk=ypref_pk)
    can_edit = funcs.has_perm_or_is_owner(request.user, 'request.edit_xpref', proforma)
    if not can_edit:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')
    prof_specs = proforma.prefspec_set.all()
    return render(request, 'requests/admin_jemco/ypref/edit_form.html', {
    # return render(request, 'requests/admin_jemco/ypref/index.html', {
        'proforma': proforma,
        'prof_specs': prof_specs
    })


@login_required
def xpref_link(request, xpref_id):
    xpref = Xpref.objects.filter(is_active=True).get(pk=xpref_id)
    xpref_specs = xpref.prefspec_set.all()
    return render(request, 'requests/admin_jemco/report/xpref_details.html', {
        'xpref': xpref,
        'xpref_specs': xpref_specs
    })


@login_required
def prof_spec_form(request, ypref_pk):
    if not Xpref.objects.filter(is_active=True).filter(pk=ypref_pk):
        messages.error(request, 'no Proforma')
        return redirect('errorpage')
    proforma = Xpref.objects.filter(is_active=True).get(pk=ypref_pk)
    req = proforma.req_id
    reqspecs = req.reqspec_set.all()
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_xpref')
    if not can_add:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

    if request.method == 'POST':
        # form = forms.ProfSpecForm(request.POST, request.user)
        form = forms.ProfSpecForm(request.POST)
        if form.is_valid():
            print('form is valid')
            spec = form.save(commit=False)
            spec.xpref_id = proforma
            spec.save()
            print('saved')
            # return redirect('prof_spec_form', ypref_pk=proforma.pk)
            return redirect('pref_insert_spec_form', ypref_pk=proforma.pk)
        else:
            print('form is not valid')
    else:
        form = forms.ProfSpecForm(request.POST)

    context = {
        'form': form,
        'proforma': proforma,
        'req_obj': req,
        'reqspec': reqspecs
    }
    return render(request, 'requests/admin_jemco/ypref/proforma_specs.html', context)
