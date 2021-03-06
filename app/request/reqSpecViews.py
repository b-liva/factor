from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

User = get_user_model()

from .models import Requests, ReqSpec, IMType, IPType, ICType, IEType
from motordb.models import MotorsCode
from django.contrib.auth.decorators import login_required
import request.templatetags.functions as funcs
from django.contrib import messages
from request.forms import forms
from core.access_control.decorator import check_perm
from core.access_control.permission_check import OrderProxy, SpecProxy


# Create your views here.
@login_required
@check_perm('request.add_reqspec', OrderProxy)
def reqspec_form(request, request_pk):
    req_pk = request_pk

    req_obj = Requests.objects.filter(is_active=True).get(pk=req_pk)
    specs = req_obj.reqspec_set.filter(is_active=True)
    return render(request, 'requests/admin_jemco/yreqspec/form.html', {'req_obj': req_obj, 'specs': specs})


@login_required
@check_perm('request.index_reqspecs', SpecProxy)
def reqspec_index(request):
    reqspecs = ReqSpec.objects.filter(is_active=True).all()
    return render(request, 'requests/admin_jemco/yreqspec/index.html', {'reqspecs': reqspecs})


@login_required
@check_perm('request.index_reqspecs', SpecProxy)
def reqspec_index_no_summary(request):

    reqspecs = ReqSpec.objects.filter(is_active=True, req_id__owner=User.objects.get(pk=4), summary='',
                                      type__title='روتین')
    reqspecs = ReqSpec.objects.filter(is_active=True, req_id__owner=User.objects.get(pk=4), summary='').exclude(
        code=99009900)

    context = {
        'motors': reqspecs
    }
    return render(request, 'requests/admin_jemco/yreqspec/index_motor_code.html', context)


@login_required
@check_perm('request.index_reqspecs', SpecProxy)
def reqspec_index_no_summary_no_routine(request):
    reqspecs = ReqSpec.objects.filter(is_active=True, req_id__owner=User.objects.get(pk=4), summary='',
                                      type__title='روتین')
    reqspecs = ReqSpec.objects.filter(is_active=True, req_id__owner=User.objects.get(pk=4), code=99009900, summary='')

    context = {
        'motors': reqspecs
    }
    return render(request, 'requests/admin_jemco/yreqspec/index_motor_code.html', context)


@login_required
@check_perm('request.index_reqspecs', SpecProxy)
def reqspec_index_with_summary(request):
    reqspecs = ReqSpec.objects.filter(is_active=True, req_id__owner=User.objects.get(pk=4), summary='',
                                      type__title='روتین')
    reqspecs = ReqSpec.objects.filter(is_active=True, req_id__owner=User.objects.get(pk=4), code=99009900).exclude(
        summary='')
    context = {
        'motors': reqspecs
    }
    return render(request, 'requests/admin_jemco/yreqspec/index_motor_code.html', context)


@login_required
@check_perm('request.index_reqspecs', SpecProxy)
def reqspec_index_IE(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.index_reqspecs')
    if not can_add:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

    reqspecs = ReqSpec.objects.filter(is_active=True, req_id__owner=User.objects.get(pk=4), summary='',
                                      type__title='روتین')
    reqspecs = ReqSpec.objects.filter(is_active=True, req_id__owner=User.objects.get(pk=4), summary__contains='IE')

    context = {
        'motors': reqspecs
    }
    return render(request, 'requests/admin_jemco/yreqspec/index_motor_code.html', context)


@login_required
def assign_code_to_motor(request):
    imb3 = IMType.objects.get(title='IMB3')
    imb35 = IMType.objects.get(title='IMB35')
    ip55 = IPType.objects.get(title="IP55")
    ic411 = ICType.objects.get(title='IC411')
    ie1 = IEType.objects.get(title='IE1')
    reqspecs = ReqSpec.objects.filter(is_active=True, code=99009900, req_id__owner=User.objects.get(pk=4), summary='',
                                      type__title='روتین')
    for req in reqspecs:
        try:
            code = MotorsCode.objects.get(kw=req.kw, speed=req.rpm, im='B3', ip='IP55')
            req.code = code.code
            req.im = imb3
            req.ic = ic411
            req.ip = ip55
            req.ie = ie1
            req.save()
        except:
            print('Nothing Found')

    reqspecs = ReqSpec.objects.filter(is_active=True, code=99009900, req_id__owner=User.objects.get(pk=4)) \
        .filter(Q(summary='فلنجی') | Q(summary='فلنج دار') | Q(summary='با پایه وفلنج'))

    for req in reqspecs:
        try:
            code = MotorsCode.objects.get(kw=req.kw, speed=req.rpm, im='B35', ip='IP55')
            req.code = code.code
            req.im = imb35
            req.ic = ic411
            req.ip = ip55
            req.ie = ie1
            req.save()
        except:
            print('Nothing Found')

    return redirect('reqspec_index_no_summary')


@login_required
@check_perm('request.delete_reqspec', SpecProxy)
def reqspec_delete(request, yreqSpec_pk, request_pk):
    req_pk = request_pk
    reqspec = ReqSpec.objects.filter(is_active=True).get(pk=yreqSpec_pk)
    req = reqspec.req_id

    if request.method == 'GET':
        context = {
            'req_id': reqspec.req_id.pk,
            'reqspec_id': reqspec.pk,
            'fn': 'reqspec_del',
        }
        return render(request, 'general/confirmation_page.html', context)
    elif request.method == 'POST':
        msg = f'ردیف مربوط به {reqspec.qty} دستگاه {reqspec.kw} کیلوات  - {reqspec.rpm} دور حذف گردید'
        messages.add_message(request, level=20, message=msg)

        reqspec.delete()
    return redirect('spec_form', request_pk=request_pk)


@login_required
@check_perm('request.edit_reqspec', SpecProxy)
def reqspec_edit(request, yreqSpec_pk, request_pk):
    req_pk = request_pk

    req = Requests.objects.filter(is_active=True).get(pk=req_pk)
    specs = ReqSpec.objects.filter(is_active=True).filter(req_id=req)
    spec = ReqSpec.objects.filter(is_active=True).get(pk=yreqSpec_pk)
    # checks the mismach for request and specs
    if spec not in specs:
        messages.error(request, 'mismatch')
        return redirect('errorpage')
    updating = True
    return render(request, 'requests/admin_jemco/yreqspec/form.html', {
        'spec': spec,
        'specs': specs,
        'req_obj': req,
        'updating': updating
    })


@login_required
@check_perm('request.add_reqspec', OrderProxy)
def spec_form(request, request_pk):
    req_pk = request_pk

    form = forms.SpecForm()
    req = Requests.objects.filter(is_active=True).get(pk=req_pk)

    if request.method == 'POST':
        form = forms.SpecForm(request.POST)
        if form.is_valid():
            spec = form.save(commit=False)
            spec.req_id = req
            spec.rpm = spec.rpm_new.rpm
            spec.owner = request.user
            if hasattr(spec.im, 'title') and hasattr(spec.ic, 'title') and hasattr(spec.ip, 'title'):
                code = MotorsCode.objects.filter(
                    kw=spec.kw,
                    speed=spec.rpm_new.rpm,
                    voltage=spec.voltage,
                    im=spec.im.title,
                    ic=spec.ic.title,
                    ip=spec.ip.title,
                )
                if code.count() == 1:
                    spec.code = code.first().code

            spec.save()
            messages.add_message(request, level=20, message=f'یک ردیف به درخواست شماره {req.number} اضافه شد.')
            return redirect('spec_form', request_pk=request_pk)
    else:
        form = forms.SpecAddForm()

    specs = req.reqspec_set.all()
    parts = req.reqpart_set.all()
    list = ['kw', 'qty']

    return render(request, 'requests/admin_jemco/yreqspec/spec_form.html', {
        'form': form,
        'req_obj': req,
        'specs': specs,
        'parts': parts,
        'list': list,
        'show_part_form': False,
    })


@login_required
@check_perm('request.add_reqpart', OrderProxy)
def part_form(request, request_pk):
    req_pk = request_pk
    req = Requests.objects.get(pk=req_pk, is_active=True)

    if request.method == 'POST':
        form = forms.PartForm(request.POST)
        if form.is_valid():
            part = form.save(commit=False)
            part.req = req
            part.owner = request.user
            part.save()
            messages.add_message(request, level=20, message=f'یک ردیف به درخواست شماره {req.number} اضافه شد.')
            return redirect('part_form', request_pk=request_pk)
        else:
            print('form not valid(part)')
    else:
        form = forms.PartForm()

    specs = req.reqspec_set.all()
    parts = req.reqpart_set.all()

    return render(request, 'requests/admin_jemco/yreqspec/spec_form.html', {
        'form': form,
        'req_obj': req,
        'specs': specs,
        'parts': parts,
        'show_part_form': True
    })


@login_required
@check_perm('request.change_reqspec', SpecProxy)
def reqspec_edit_form(request, yreqSpec_pk, request_pk):
    req_pk = request_pk

    req = Requests.objects.get(pk=req_pk)
    specs = req.reqspec_set.all()
    parts = req.reqpart_set.all()
    spec = ReqSpec.objects.filter(is_active=True).get(pk=yreqSpec_pk)
    form = forms.SpecForm(request.POST or None, instance=spec)
    if request.method == 'POST':
        if form.is_valid():
            spec = form.save(commit=False)
            spec.rpm = spec.rpm_new.rpm
            if hasattr(spec.im, 'title') and hasattr(spec.ic, 'title') and hasattr(spec.ip, 'title'):
                code = MotorsCode.objects.filter(
                    kw=spec.kw,
                    speed=spec.rpm_new.rpm,
                    voltage=spec.voltage,
                    im=spec.im.title,
                    ic=spec.ic.title,
                    ip=spec.ip.title,
                )
                if code.count() == 1:
                    spec.code = code.first().code
                else:
                    spec.code = 99009900
            else:
                spec.code = 99009900
            spec.save()
            # form = forms.SpecForm()
            messages.add_message(request, level=20, message='جزئیات درخواست اصلاح شد')
            return redirect('spec_form', request_pk=req.pk)

    context = {
        'req_obj': req,
        'parts': parts,
        'specs': specs,
        'form': form
    }
    return render(request, 'requests/admin_jemco/yreqspec/spec_form.html', context)


@login_required
def reqspec_copy(request, yreqSpec_pk, request_pk):
    spec = ReqSpec.objects.get(pk=yreqSpec_pk)
    spec.pk = None
    spec.save()
    messages.error(request, 'ردیف با موفقیت کپی شد.')
    return redirect('reqspec_edit_form', yreqSpec_pk=spec.pk, request_pk=spec.req_id.pk)
