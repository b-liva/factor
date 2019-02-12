import random

from django.contrib import messages
from django.shortcuts import render, redirect

import request.templatetags.functions as funcs
from request import models
from request.models import Requests
from request.models import Xpref
from pricedb.models import MotorDB

from request.forms import proforma_forms, forms
from django.contrib.auth.decorators import login_required


@login_required
def pref_index(request):
    can_index = funcs.has_perm_or_is_owner(request.user, 'request.index_proforma')
    if not can_index:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')
    # prefs = Xpref.objects.filter(req_id__owner=request.user).order_by('pub_date').reverse()
    # prefs = Xpref.objects.all().order_by('date_fa').reverse()
    prefs = Xpref.objects.filter(is_active=True, owner=request.user).order_by('date_fa').reverse()
    if request.user.is_superuser:
        prefs = Xpref.objects.filter(is_active=True).order_by('date_fa').reverse()
    context = {
        'prefs': prefs,
        'title': 'پیش فاکتور',
        'showDelete': True,
    }
    return render(request, 'requests/admin_jemco/ypref/index.html', context)


@login_required
def pref_index_deleted(request):
    can_index = funcs.has_perm_or_is_owner(request.user, 'request.index_deleted_proforma')
    if not can_index:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')
    # prefs = Xpref.objects.filter(req_id__owner=request.user).order_by('pub_date').reverse()
    # prefs = Xpref.objects.all().order_by('date_fa').reverse()
    prefs = Xpref.objects.filter(is_active=False, owner=request.user).order_by('date_fa').reverse()
    if request.user.is_superuser:
        prefs = Xpref.objects.filter(is_active=False).order_by('date_fa').reverse()
    context = {
        'prefs': prefs,
        'title': 'پیش فاکتور های حذف شده',
        'showDelete': False,
    }
    return render(request, 'requests/admin_jemco/ypref/index.html', context)


@login_required
def pref_find(request):
    # term = request.POST['text']
    if not request.POST['pref_no']:
        return redirect('pref_index')
    prof_no = request.POST['pref_no']
    if not Xpref.objects.filter(number=prof_no):
        messages.error(request, 'پیش فاکتور مورد نظر یافت نشد')
        return redirect('pref_index')
    prefs = Xpref.objects.filter(is_active=True).filter(number=prof_no).filter(summary__contains=term).all()
    search_items = {
        # 'term': term,
        'proforma_no': prof_no,
    }
    if prefs is None:
        messages.error(request, 'no match found')
        return redirect('errorpage')
    return render(request, 'requests/admin_jemco/ypref/search_index.html', {
        'prefs': prefs,
        'search_items': search_items
    })


@login_required
def pref_details(request, ypref_pk):
    if not Xpref.objects.filter(pk=ypref_pk):
        messages.error(request, 'Nothin found')
        return redirect('errorpage')

    pref = Xpref.objects.get(pk=ypref_pk)

    can_read = funcs.has_perm_or_is_owner(request.user, 'request.read_proforma', pref)
    if not can_read:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')
    nestes_dict = {}
    proforma_total = 0
    kw_total = 0

    prof_images = pref.proffiles_set.all()
    prefspecs = pref.prefspec_set.all()
    i = 0
    for prefspec in prefspecs:
        kw = prefspec.kw
        speed = prefspec.rpm
        proforma_total += prefspec.qty * prefspec.price
        kw_total += prefspec.qty * prefspec.kw
        nestes_dict[i] = {
            'obj': prefspec,
            'spec_total': prefspec.qty * prefspec.price
        }
        i += 1

    context = {
        'pref': pref,
        'prefspecs': prefspecs,
        'nested': nestes_dict,
        'vat': proforma_total * 0.09,
        'proforma_total': proforma_total * 1.09,
        'kw_total': kw_total,
        'prof_images': prof_images,
    }
    return render(request, 'requests/admin_jemco/ypref/details.html', context)


@login_required
def pref_details_backup(request, ypref_pk):
    if not Xpref.objects.filter(is_active=True).filter(pk=ypref_pk):
        messages.error(request, 'Nothin found')
        return redirect('errorpage')

    pref = Xpref.objects.filter(is_active=True).get(pk=ypref_pk)

    can_read = funcs.has_perm_or_is_owner(request.user, 'request.read_proforma', pref)
    if not can_read:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')
    nestes_dict = {}

    spec_total = 0
    proforma_total = 0
    sales_total = 0
    percentage = 0
    total_percentage = 0
    # pref = Xpref.objects.get(pk=ypref_pk)

    prof_images = pref.proffiles_set.all()
    prefspecs = pref.prefspec_set.all()
    print('pref and specs found')
    print(f'pk={pref.pk} - number={pref.number}')
    print(f'specs: {prefspecs}')
    i = 0
    for prefspec in prefspecs:
        kw = prefspec.kw
        speed = prefspec.rpm
        price = MotorDB.objects.filter(kw=kw).filter(speed=speed).last()
        print(f'price is exactly: {price} with type: {type(price)}')
        proforma_total += prefspec.qty * prefspec.price
        if hasattr(price, 'prime_cost'):
            sales_total += prefspec.qty * price.prime_cost
            percentage = (prefspec.price/(price.prime_cost))
            prime = price.prime_cost
        else:
            prime = 'N/A'
            sales_total = "N/A"
            percentage = False
        if percentage >= 1:
            percentage_class = 'good-conditions'
        elif percentage < 1:
            percentage_class = 'bad-conditions'
        else:
            percentage_class = 'no-value'
        nestes_dict[i] = {
            'obj': prefspec,
            'sale_price': prime,
            'percentage': percentage,
            'percentage_class': percentage_class,
            'spec_total': prefspec.qty * prefspec.price
        }
        i += 1
        if hasattr(price, 'prime_cost'):
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
        'prof_images': prof_images,
    })


@login_required
def pref_delete(request, ypref_pk):

    if not Xpref.objects.filter(is_active=True).filter(pk=ypref_pk):
        messages.error(request, 'Nothin found')
        return redirect('errorpage')
    pref = Xpref.objects.filter(is_active=True).get(pk=ypref_pk)
    can_del = funcs.has_perm_or_is_owner(request.user, 'request.delete_xpref', pref)

    if not can_del:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')
    if request.method == 'GET':
        context = {
            'id': pref.pk,
            'fn': 'prof_del',
        }
        return render(request, 'general/confirmation_page.html', context)
    elif request.method == 'POST':
        # pref.delete()
        pref.is_active = False
        pref.temp_number = pref.number
        rand_num = random.randint(100000, 200000)
        while Xpref.objects.filter(number=rand_num):
            rand_num = random.randint(100000, 200000)
        pref.number = rand_num
        pref.save()
    return redirect('pref_index')


@login_required
def pro_form(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_xpref')
    if not can_add:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

    reqs = Requests.objects.filter(is_active=True)
    owners_reqs = Requests.objects.filter(is_active=True).filter(owner=request.user)
    imgform = proforma_forms.ProfFileForm()

    if request.method == 'POST':
        form = forms.ProformaForm(request.user.pk, request.POST)
        img_form = proforma_forms.ProfFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        if form.is_valid():
            # Save Proforma
            proforma = form.save(commit=False)
            proforma.owner = request.user
            proforma.save()

            # Save files
            for f in files:
                file_instance = models.ProfFiles(image=f, prof=proforma)
                file_instance.save()

            # make a list of specs for this proforma
            req = proforma.req_id
            specs_set = req.reqspec_set.all()
            print(f'request is: {req}')
            print(f'specs: {specs_set}')

            for spec in specs_set:

                form = forms.ProfSpecForm()
                specItem = form.save(commit=False)

                specItem.type = spec.type
                specItem.price = 0
                specItem.kw = spec.kw
                specItem.qty = spec.qty
                specItem.rpm = spec.rpm
                specItem.voltage = spec.voltage
                specItem.ip = spec.ip
                specItem.ic = spec.ic
                specItem.summary = spec.summary
                specItem.owner = request.user

                specItem.xpref_id = proforma
                specItem.save()

            return redirect('prof_spec_form', ypref_pk=proforma.pk)
        else:
            print('form is not Valid')
    else:
        form = forms.ProformaForm(request.user.pk)

    context = {
        'form': form,
        'reqs': reqs,
        'prof_file': imgform,
        'owner_reqs': owners_reqs,
        'message': 'ثبت پیش فاکتور',
    }
    return render(request, 'requests/admin_jemco/ypref/proforma_form.html', context)


@login_required
def pref_insert_spec_form(request, ypref_pk):
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_xpref')
    if not can_add:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')
    pref = Xpref.objects.filter(is_active=True).get(pk=ypref_pk)
    req = Requests.objects.filter(is_active=True).get(pk=pref.req_id.pk)
    specs = req.reqspec_set.filter(is_active=True)
    prefspecs = pref.prefspec_set.filter(is_active=True)

    prices = request.POST.getlist('price')
    qty = request.POST.getlist('qty')
    considerations = request.POST.getlist('considerations')
    i = 0
    for s in prefspecs:
        s.qty = qty[i]
        s.price = prices[i]
        s.considerations = considerations[i]
        s.save()
        i += 1

    return redirect('pref_index')


@login_required
def pref_edit(request, ypref_pk):
    if not Xpref.objects.filter(is_active=True).filter(pk=ypref_pk):
        messages.error(request, 'no Proforma')
        return redirect('errorpage')

    can_edit = funcs.has_perm_or_is_owner(request.user, 'request.edit_xpref')
    if not can_edit:
        messages.error(request, 'no access ')
        return redirect('errorpage')

    xpref = Xpref.objects.filter(is_active=True).get(pk=ypref_pk)
    spec_prices = request.POST.getlist('price')
    prof_images = xpref.proffiles_set.all()

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
        if hasattr(price, 'prime_cost'):
            prime = price.prime_cost
            percentage = (prefspec.price / (prime))
        else:
            percentage = False
            prime = 'N/A'
        if percentage >= 1:
            percentage_class = 'good-conditions'
        elif percentage < 1:
            percentage_class = 'bad-conditions'
        else:
            percentage_class = 'No class'
        nestes_dict[i] = {
            'obj': prefspec,
            'sale_price': prime,
            'percentage': percentage,
            'percentage_class': percentage_class
        }
        i += 1

    messages.add_message(request, level=20, message='Proforma updated successfulley.')

    return redirect('pref_index')

    # return render(request, 'requests/admin_jemco/ypref/index.html', {
    #     'pref': xpref,
    #     'prefspecs': prefspecs,
    #     'nested': nestes_dict,
    #     'prof_images': prof_images,
    # })


    # return render(request, 'requests/admin_jemco/ypref/details.html', {
    #     'pref': xpref,
    #     'prefspecs': xspec,
    #     'msg': msg,
    # })

@login_required
def pref_edit2(request, ypref_pk):
    # 1- check for permissions
    # 2 - find proforma and related images and specs
    # 3 - make request image form
    # 4 - prepare image names to use in template
    # 5 - get the list of files from request
    # 6 - if form is valid the save request and its related images
    # 7 - render the template file

    if not Xpref.objects.filter(is_active=True).filter(pk=ypref_pk):
        messages.error(request, 'Nothin found')
        return redirect('errorpage')

    prof = Xpref.objects.filter(is_active=True).get(pk=ypref_pk)

    can_read = funcs.has_perm_or_is_owner(request.user, 'request.edit_xpref', prof)
    if not can_read:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

    # prof = models.Xpref.objects.get(pk=ypref_pk)
    prof_images = prof.proffiles_set.all()
    img_names = {}
    for p in prof_images:
        name = p.image.name
        newname = name.split('/')
        las = newname[-1]
        img_names[p.pk] = las
    # form = proforma_forms.ProfEditForm(request.POST or None, request.FILES or None, instance=prof)
    if prof.date_fa:
        prof.date_fa = prof.date_fa.togregorian()
    if prof.exp_date_fa:
        prof.exp_date_fa = prof.exp_date_fa.togregorian()
    # form = forms.ProformaForm(request.user.pk, request.POST or None, request.FILES or None, instance=prof)
    form = forms.ProformaEditForm(request.user.pk, request.POST or None, request.FILES or None, instance=prof)
    form.req_id = prof.req_id
    # form = forms.ProformaForm(request.POST or None, request.FILES or None)
    img_form = proforma_forms.ProfFileForm(request.POST, request.FILES)
    files = request.FILES.getlist('image')
    # fv = form.is_valid()
    # fvi = img_form.is_valid()
    # print(f'fv is: {fv}')
    # print(f'fvi is: {fvi}')
    if form.is_valid() and img_form.is_valid():
        prof_item = form.save(commit=False)
        # prof_item.owner = request.user
        # prof_item.req_id = prof.req_id
        prof_item.number = prof.number
        prof_item.save()
        for f in files:
            file_instance = models.ProfFiles(image=f, prof=prof_item)
            file_instance.save()
        return redirect('pref_index')

    context = {
        'form': form,
        'prof_file': img_form,
        'prof_images': prof_images,
        'img_names': img_names,
        'message': 'ویرایش پیش فاکتور',
    }
    return render(request, 'requests/admin_jemco/ypref/proforma_form.html', context)
