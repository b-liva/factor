import os
import shutil
import datetime
import jdatetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.models import User
from request.forms.forms import RequestFrom, RequestFileForm
from customer.forms import CustomerCreateRequestForm, CustomerCreateSpecForm
from request.models import Requests, RequestFiles, ReqSpec, ProjectType
import request.templatetags.functions as funcs


@login_required
def custome_create_request(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_requests')
    if not can_add:
        messages.error(request, 'مجاز نیستید.')
        return redirect('errorpage')

    no_spec_reqs = Requests.objects.filter(number__gte=100000)
    for r in no_spec_reqs:
        specs = r.reqspec_set.all()
        if len(specs) == 0:
            files_tobe_removed = r.requestfiles_set.all()
            for f in files_tobe_removed:
                f.delete()
            file_name = f"id{r.pk}_No{r.number}"
            dir_path = os.path.join(settings.MEDIA_ROOT, 'requestfiles', file_name)
            shutil.rmtree(dir_path, ignore_errors=True)
            r.delete()

    user = request.user
    customer = user.customer
    if request.method == 'POST':
        form = CustomerCreateRequestForm(request.POST or None)
        file_form = RequestFileForm(request.FILES or None)
        files = request.FILES.getlist('image')
        if form.is_valid():
            req_item = form.save(commit=False)

            last_req = Requests.objects.filter(number__gte=100000).order_by('number').last()
            if last_req is None:
                req_item.number = 100000
            else:
                req_item.number = last_req.number + 1
            req_item.customer = customer
            req_item.pub_date = datetime.datetime.now()
            req_item.date_fa = jdatetime.datetime.now()
            owner = User.objects.get(pk=1)
            req_item.owner = owner
            req_item.added_by_customer = True
            req_item.edited_by_customer = True
            # do stuff here
            req_item.save()
            for file in files:
                file_instance = RequestFiles(image=file, req=req_item)
                file_instance.save()
            return redirect('fbv_customer_spec_create', req_pk=req_item.pk)
    if request.method == 'GET':
        form = CustomerCreateRequestForm()
        file_form = RequestFileForm()

    context = {
        'user_p': user,
        'customer': customer,
        'form': form,
        'file_form': file_form,
    }

    return render(request, 'requests/fbv/req_form.html', context)


@login_required
def custome_create_request2(request):
    no_spec_reqs = Requests.objects.filter(number__gte=100000)
    for r in no_spec_reqs:
        specs = r.reqspec_set.all()
        if len(specs) == 0:
            r.delete()
    user = request.user
    customer = user.customer
    req = Requests()
    last_req = Requests.objects.filter(number__gte=100000).order_by('number').last()
    if last_req is None:
        req.number = 100000
    else:
        req.number = last_req.number + 1
    req.customer = customer
    req.pub_date = datetime.datetime.now()
    req.date_fa = jdatetime.datetime.now()
    owner = User.objects.get(pk=1)
    req.owner = owner
    req.added_by_customer = True
    req.save()
    return redirect('fbv_customer_spec_create', req_pk=req.pk)


@login_required
def customer_create_specs(request, req_pk):

    user = request.user
    # if user.is_customer:
    #     customer = user.customer
    req = Requests.objects.get(pk=req_pk)
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_reqspec', req)
    if not can_add:
        messages.error(request, 'مجاز نیستید.')
        return redirect('errorpage')

    specs = req.reqspec_set.all()
    if request.method == 'POST':
        form = CustomerCreateSpecForm(request.POST or None)
        if form.is_valid():
            spec_item = form.save(commit=False)
            spec_item.req_id = req
            spec_item.owner = req.owner
            spec_item.type = ProjectType.objects.first()
            spec_item.save()
            req.edited_by_customer = True
            req.save()
            msg = f"{spec_item.qty} دستگاه الکتروموتور {spec_item.kw} کیلووات {spec_item.rpm} دور اضافه گردید."
            messages.add_message(request, level=20, message=msg)
            return redirect('fbv_customer_spec_create', req_pk=req.pk)
        else:
            messages.error(request, 'something went wrong')
            return redirect('fbv_customer_spec_create')
    if request.method == 'GET':
        form = CustomerCreateSpecForm()
    context = {
        'form': form,
        'specs': specs,
        'req': req,
    }
    return render(request, 'requests/fbv/spec_form.html', context)


@login_required
def customer_req_details(request, req_pk):
    req = Requests.objects.get(pk=req_pk)
    context = {
        'request': req
    }
    return render(request, 'requests/fbv/details.html', context)


@login_required
def customer_spec_edit_form(request, req_pk, spec_pk):
    # if not Requests.objects.filter(pk=req_pk):
    #     error = True
    #     messages.error(request, 'درخواست مورد نظر یافت نشد')
    #     return redirect('errorpage')
    user = request.user
    req = Requests.objects.filter(is_active=True).get(pk=req_pk)
    spec = ReqSpec.objects.filter(is_active=True).get(pk=spec_pk)

    can_edit = funcs.has_perm_or_is_owner(request.user, 'request.edit_reqspec', req)
    if not can_edit:
        messages.error(request, 'مجاز نیستید.')
        return redirect('errorpage')

    # can_edit = funcs.has_perm_or_is_owner(request.user, 'request.delete_requests', req)
    # if not can_edit:
    #     messages.error(request, 'No access')
    #     return redirect('errorpage')

    specs = req.reqspec_set.all()
    if request.method == "POST":
        form = CustomerCreateSpecForm(request.POST or None, instance=spec)
        if form.is_valid():
            spec_item = form.save(commit=False)
            req.edited_by_customer = True
            spec_item.save()
            req.save()
            # messages.add_message(request, level=20, messages="ردیف با اصلاح گردید.")
            return redirect('customer_request_details', pk=req.pk)
    if request.method == "GET":
        form = CustomerCreateSpecForm(instance=spec)

    context = {
        'user': user,
        'req': req,
        'spec': spec,
        'specs': specs,
        'form': form,
    }
    return render(request, 'requests/fbv/spec_form.html', context)


@login_required
def customer_spec_delete(request, spec_pk, req_pk):
    if not ReqSpec.objects.filter(is_active=True).filter(pk=spec_pk):
        messages.error(request, 'No such Spec.')
        return redirect('errorpage')
    reqspec = ReqSpec.objects.filter(is_active=True).get(pk=spec_pk)
    req = reqspec.req_id

    can_delete = funcs.has_perm_or_is_owner(request.user, 'request.delete_reqspec', req)
    if not can_delete:
        messages.error(request, 'مجاز نیستید.')
        return redirect('errorpage')

    if request.method == 'GET':
        context = {
            'req_id': reqspec.req_id.pk,
            'reqspec_id': reqspec.pk,
            'fn': 'reqspec_del',
        }
        return render(request, 'requests/fbv/confirmation_page.html', context)
    elif request.method == 'POST':
        msg = f'ردیف مربوط به {reqspec.qty} دستگاه {reqspec.kw} کیلوات  - {reqspec.rpm} دور حذف گردید'
        messages.add_message(request, level=20, message=msg)
        reqspec.delete()
        reqspec.req_id.edited_by_customer = True
        reqspec.req_id.save()
    return redirect('fbv_customer_spec_create', req_pk=req_pk)


@login_required
def customer_req_edit(request, req_pk):
    req = Requests.objects.get(pk=req_pk)

    can_edit = funcs.has_perm_or_is_owner(request.user, 'request.edit_requests', req)
    if not can_edit:
        messages.error(request, 'مجاز نیستید.')
        return redirect('errorpage')

    req_images = req.requestfiles_set.all()
    img_names = {}
    for r in req_images:
        name = r.image.name
        newname = name.split('/')
        las = newname[-1]
        img_names[r.pk] = las
    if req.date_fa:
        req.date_fa = req.date_fa.togregorian()

    if request.method == "POST":
        form = CustomerCreateRequestForm(request.POST or None, request.FILES or None, instance=req)
        img_form = RequestFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        if form.is_valid() and img_form.is_valid():
            req_item = form.save(commit=False)
            req_item.edited_by_customer = True
            req_item.save()
            # form.save_m2m()
            for f in files:
                file_instance = RequestFiles(image=f, req=req_item)
                file_instance.save()
            # return redirect('request_index')
            return redirect('customer_request_details', pk=req.pk)

    if request.method == "GET":
        form = CustomerCreateRequestForm(instance=req)
        img_form = RequestFileForm(instance=req)

    context = {
        'form': form,
        'req': req,
        'file_form': img_form,
        'img_names': img_names,
        'req_images': req_images,
    }

    return render(request, 'requests/fbv/req_form.html', context)


@login_required
def customer_img_del(request, img_pk):
    if not RequestFiles.objects.filter(pk=img_pk):
        messages.error(request, 'فایل مورد نظر یافت نشد.')
        return redirect('errorpage')

    image = RequestFiles.objects.get(pk=img_pk)
    req = image.req

    can_delete = funcs.has_perm_or_is_owner(request.user, 'request.edit_requests', req)
    if not can_delete:
        messages.error(request, 'مجاز نیستید.')
        return redirect('errorpage')

    image.delete()
    req = image.req
    req.edited_by_customer = True
    req.save()
    return redirect('fbv_customer_req_edit', req_pk=req.pk)
