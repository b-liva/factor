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


# Create your views here.
@login_required
def reqspec_form(request, req_pk):
    if not Requests.objects.filter(is_active=True).filter(pk=req_pk):
        messages.error(request, 'No such Request')
        return redirect('errorpage')
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_reqspec')
    if not can_add:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')
    req_obj = Requests.objects.filter(is_active=True).get(pk=req_pk)
    specs = req_obj.reqspec_set.filter(is_active=True)
    return render(request, 'requests/admin_jemco/yreqspec/form.html', {'req_obj': req_obj, 'specs': specs})


@login_required
def reqspec_index(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.index_reqspecs')
    if not can_add:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

    reqspecs = ReqSpec.objects.filter(is_active=True).all()
    return render(request, 'requests/admin_jemco/yreqspec/index.html', {'reqspecs': reqspecs})


@login_required
def reqspec_index_no_summary(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.index_reqspecs')
    if not can_add:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

    reqspecs = ReqSpec.objects.filter(is_active=True, req_id__owner=User.objects.get(pk=4), summary='', type__title='روتین')
    reqspecs = ReqSpec.objects.filter(is_active=True, req_id__owner=User.objects.get(pk=4), summary='').exclude(code=99009900)

    context = {
        'motors': reqspecs
    }
    return render(request, 'requests/admin_jemco/yreqspec/index_motor_code.html', context)


@login_required
def reqspec_index_no_summary_no_routine(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.index_reqspecs')
    if not can_add:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

    reqspecs = ReqSpec.objects.filter(is_active=True, req_id__owner=User.objects.get(pk=4), summary='', type__title='روتین')
    reqspecs = ReqSpec.objects.filter(is_active=True, req_id__owner=User.objects.get(pk=4), code=99009900, summary='')

    context = {
        'motors': reqspecs
    }
    return render(request, 'requests/admin_jemco/yreqspec/index_motor_code.html', context)


@login_required
def reqspec_index_with_summary(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.index_reqspecs')
    if not can_add:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

    reqspecs = ReqSpec.objects.filter(is_active=True, req_id__owner=User.objects.get(pk=4), summary='', type__title='روتین')
    reqspecs = ReqSpec.objects.filter(is_active=True, req_id__owner=User.objects.get(pk=4), code=99009900).exclude(summary='')
    # reqspecs = ReqSpec.objects.filter(is_active=True, req_id__owner=User.objects.get(pk=4), summary='فلنجدارعمودنصب روبه پایین')
    # reqspecs = ReqSpec.objects.filter(is_active=True, req_id__owner=User.objects.get(pk=4), summary='فلنجی')
    # reqspecs = ReqSpec.objects.filter(is_active=True, req_id__owner=User.objects.get(pk=4), summary='فلنج دار')
    # reqspecs = ReqSpec.objects.filter(is_active=True, req_id__owner=User.objects.get(pk=4), summary='با پایه وفلنج')
    # reqspecs = ReqSpec.objects.filter(is_active=True, req_id__owner=User.objects.get(pk=4)).filter(Q(summary='فلنجی') | Q(summary='فلنج دار') | Q(summary='با پایه وفلنج'))
    print(reqspecs.count())

    context = {
        'motors': reqspecs
    }
    return render(request, 'requests/admin_jemco/yreqspec/index_motor_code.html', context)


@login_required
def reqspec_index_IE(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.index_reqspecs')
    if not can_add:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

    reqspecs = ReqSpec.objects.filter(is_active=True, req_id__owner=User.objects.get(pk=4), summary='', type__title='روتین')
    reqspecs = ReqSpec.objects.filter(is_active=True, req_id__owner=User.objects.get(pk=4), summary__contains='IE')

    context = {
        'motors': reqspecs
    }
    return render(request, 'requests/admin_jemco/yreqspec/index_motor_code.html', context)


@login_required
def assign_code_to_motor(request):
    print('hhhhhhh')
    imb3 = IMType.objects.get(title='IMB3')
    imb35 = IMType.objects.get(title='IMB35')
    ip55 = IPType.objects.get(title="IP55")
    ic411 = ICType.objects.get(title='IC411')
    ie1 = IEType.objects.get(title='IE1')
    reqspecs = ReqSpec.objects.filter(is_active=True, code=99009900, req_id__owner=User.objects.get(pk=4), summary='',
                                      type__title='روتین')
    print(reqspecs.count())
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

    reqspecs = ReqSpec.objects.filter(is_active=True, code=99009900, req_id__owner=User.objects.get(pk=4))\
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
def reqspec_delete(request, yreqSpec_pk, req_pk):
    if not ReqSpec.objects.filter(is_active=True).filter(pk=yreqSpec_pk):
        messages.error(request, 'No such Spec.')
        return redirect('errorpage')

    reqspec = ReqSpec.objects.filter(is_active=True).get(pk=yreqSpec_pk)
    can_del = funcs.has_perm_or_is_owner(request.user, 'request.delete_reqspecs', reqspec)
    if not can_del:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

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
    return redirect('spec_form', req_pk=req_pk)


@login_required
def reqspec_edit(request, yreqSpec_pk, req_pk):
    if not Requests.objects.filter(is_active=True).filter(pk=req_pk) or not ReqSpec.objects.filter(is_active=True).filter(pk=yreqSpec_pk):
        messages.error(request, 'no request or specs')
        return redirect('errorpage')
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
def spec_form(request, req_pk):
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_reqspec')
    if not can_add:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

    form = forms.SpecForm()
    req = Requests.objects.filter(is_active=True).get(pk=req_pk)

    if request.method == 'POST':
        form = forms.SpecForm(request.POST)
        if form.is_valid():
            spec = form.save(commit=False)
            spec.req_id = req
            spec.owner = request.user
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
            return redirect('spec_form', req_pk=req_pk)
    else:
        form = forms.SpecAddForm()

    specs = req.reqspec_set.all()
    list = ['kw', 'qty']

    return render(request, 'requests/admin_jemco/yreqspec/spec_form.html', {
        'form': form,
        'req_obj': req,
        'specs': specs,
        'list': list,
    })


@login_required
def reqspec_edit_form(request, yreqSpec_pk, req_pk):

    if not Requests.objects.filter(is_active=True).filter(pk=req_pk) or not ReqSpec.objects.filter(is_active=True).filter(pk=yreqSpec_pk):
        messages.error(request, 'no request or specs')
        return redirect('errorpage')

    reqspec = ReqSpec.objects.filter(is_active=True).get(pk=yreqSpec_pk)
    colleagues = reqspec.req_id.colleagues.all()
    colleague = False
    if request.user in colleagues:
        colleague = True
    can_edit = funcs.has_perm_or_is_owner(request.user, 'request.edit_reqspec', reqspec, colleague)
    if not can_edit:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

    req = Requests.objects.get(pk=req_pk)
    specs = req.reqspec_set.all()
    spec = ReqSpec.objects.filter(is_active=True).get(pk=yreqSpec_pk)
    form = forms.SpecForm(request.POST or None, instance=spec)
    if request.method == 'POST':
        if form.is_valid():
            spec = form.save(commit=False)
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
            spec.save()
            # form = forms.SpecForm()
            messages.add_message(request, level=20,  message='جزئیات درخواست اصلاح شد')
            return redirect('spec_form', req_pk=req.pk)

    context = {
        'req_obj': req,
        'specs': specs,
        'form': form
    }
    return render(request, 'requests/admin_jemco/yreqspec/spec_form.html', context)


@login_required
def reqspec_copy(request, yreqSpec_pk, req_pk):
    spec = ReqSpec.objects.get(pk=yreqSpec_pk)
    spec.pk = None
    spec.save()
    messages.error(request, 'ردیف با موفقیت کپی شد.')
    return redirect('reqspec_edit_form', yreqSpec_pk=spec.pk, req_pk=spec.req_id.pk)
