from django.shortcuts import render, redirect

from .models import Requests
from .models import ReqSpec
from django.contrib.auth.decorators import login_required
import request.templatetags.functions as funcs
from django.contrib import messages
from request.forms import forms


# Create your views here.
@login_required
def reqspec_form(request, req_pk):
    if not Requests.objects.filter(pk=req_pk):
        messages.error(request, 'No such Request')
        return redirect('errorpage')
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_reqspec')
    if not can_add:
        messages.error(request, 'You have not enough access to add request specs')
        return redirect('errorpage')
    req_obj = Requests.objects.get(pk=req_pk)
    specs = req_obj.reqspec_set.all()
    return render(request, 'requests/admin_jemco/yreqspec/form.html', {'req_obj': req_obj, 'specs': specs})


@login_required
def reqspec_insert(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_reqspec')
    if not can_add:
        messages.error(request, 'You have not enough access')
        return redirect('errorpage')
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
        spec.owner = request.user
        # if request.POST['price']:
        #     spec.price = request.POST['price']
        spec.save()
        return redirect('reqSpec_form', req_pk=related_req.pk)


@login_required
def reqspec_index(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.index_reqspecs')
    if not can_add:
        messages.error(request, 'You have not enough access')
        return redirect('errorpage')

    reqspecs = ReqSpec.objects.all()
    return render(request, 'requests/admin_jemco/yreqspec/index.html', {'reqspecs': reqspecs})


@login_required
def reqspec_details(request, yreqSpec_pk):
    if not ReqSpec.objects.filter(pk=yreqSpec_pk):
        messages.error(request, 'No such Spec')
        return redirect('errorpage')
    reqspec = ReqSpec.objects.get(pk=yreqSpec_pk)
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.read_reqspecs', reqspec)
    if not can_add:
        messages.error(request, 'You have not enough access')
        return redirect('errorpage')
    pass


@login_required
def reqspec_delete(request, yreqSpec_pk, req_pk):

    if not ReqSpec.objects.filter(pk=yreqSpec_pk):
        messages.error(request, 'No such Spec.')
        return redirect('errorpage')

    reqspec = ReqSpec.objects.get(pk=yreqSpec_pk)
    can_del = funcs.has_perm_or_is_owner(request.user, 'request.delete_reqspecs', reqspec)
    if not can_del:
        messages.error(request, 'You have not enough access')
        return redirect('errorpage')

    req = reqspec.req_id
    reqspec.delete()
    messages.add_message(request, level=20, message='spec deleted successfully')
    return redirect('spec_form', req_pk=req_pk)
    # return redirect('reqSpec_form', req_pk=req_pk)


@login_required
def reqspec_edit(request, yreqSpec_pk, req_pk):
    if not Requests.objects.filter(pk=req_pk) or not ReqSpec.objects.filter(pk=yreqSpec_pk):
        messages.error(request, 'no request or specs')
        return redirect('errorpage')
    req = Requests.objects.get(pk=req_pk)
    specs = ReqSpec.objects.filter(req_id=req)
    spec = ReqSpec.objects.get(pk=yreqSpec_pk)
    # checks the mismach for request and specs
    if spec not in specs:
        messages.error(request, 'mismatch')
        return redirect('errorpage')
    updating = True
    # specs = PrefSpec.objects.all()
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
        messages.error(request, 'You have not enough access to add request specs')
        return redirect('errorpage')

    form = forms.SpecForm()
    req = Requests.objects.get(pk=req_pk)

    if request.method == 'POST':
        form = forms.SpecForm(request.POST)
        if form.is_valid():
            spec = form.save(commit=False)
            spec.req_id = req
            spec.owner = request.user
            spec.save()
            messages.add_message(request, level=20, message=f'specs added successfully to request no.{req.number}')
            return redirect('spec_form', req_pk=req_pk)
    else:
        form = forms.SpecForm()

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

    if not Requests.objects.filter(pk=req_pk) or not ReqSpec.objects.filter(pk=yreqSpec_pk):
        messages.error(request, 'no request or specs')
        return redirect('errorpage')

    reqspec = ReqSpec.objects.get(pk=yreqSpec_pk)
    can_edit = funcs.has_perm_or_is_owner(request.user, 'request.add_reqspec', reqspec)
    if not can_edit:
        messages.error(request, 'You have not enough access to edit request specs')
        return redirect('errorpage')

    req = Requests.objects.get(pk=req_pk)
    specs = req.reqspec_set.all()
    spec = ReqSpec.objects.get(pk=yreqSpec_pk)
    form = forms.SpecForm(request.POST or None, instance=spec)
    print(f'request is: {request.method}')
    if request.method == 'POST':
        if form.is_valid():
            print('form is valid')
            form.save()
            # form = forms.SpecForm()
            messages.add_message(request, level=20,  message='specs updated successfully')
            return redirect('spec_form', req_pk=req.pk)

    return render(request, 'requests/admin_jemco/yreqspec/spec_form.html', {
        'req_obj': req,
        'specs': specs,
        'form': form
    })