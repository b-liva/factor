from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages


from request.views import allRequests, find_all_obj
from request.models import Requests
from request.models import Xpref
from request.models import Payment
from request import models
from customer.models import Customer
from django.contrib.auth.decorators import login_required
import request.templatetags.functions as funcs
from request.forms import forms


# Create your views here.

@login_required
def project_type_form(request):

    if request.method == 'POST':
        form = forms.ProjectTypeForm(request.POST)
        project_type = form.save(commit=False)
        project_type.save()
        return redirect('projects_type_index')
    else:
        form = forms.ProjectTypeForm()
    return render(request, 'requests/admin_jemco/project_type/form.html', {
        'form': form,
    })

@login_required
def projects_type_index(request):
    all_project_types = models.ProjectType.objects.all()
    return render(request, 'requests/admin_jemco/project_type/index.html', {
        'projects': all_project_types,
    })


@login_required
# add a new request to the system
def request_form(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_requests')
    if not can_add:
        messages.error(request, 'Sorry, You need some priviliges to do this.')
        return redirect('errorpage')
    req = Requests()
    customers = Customer.objects.all()
    return render(request, 'requests/admin_jemco/yrequest/form.html', {
        'req': req,
        'customers': customers,
    })


@login_required
def req_form(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_requests')
    if not can_add:
        messages.error(request, 'Sorry, You need some priviliges to do this.')
        return redirect('errorpage')
    file_instance = forms.RequestFileForm()

    if request.method == 'POST':
        form = forms.RequestFrom(request.POST or None, request.FILES or None)
        img_form = forms.RequestFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        if form.is_valid() and img_form.is_valid():
            req_item = form.save(commit=False)
            req_item.owner = request.user
            req_item.save()
            for f in files:
                file_instance = models.RequestFiles(image=f, req=req_item)
                file_instance.save()
            return redirect('spec_form', req_pk=req_item.pk)
    else:
        print('request is GET')
        form = forms.RequestFrom()
        file_instance = forms.RequestFileForm()
    return render(request, 'requests/admin_jemco/yrequest/req_form.html', {
        'form': form,
        'req_img': file_instance
    })


@login_required
def request_insert(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_requests')
    if not can_add:
        messages.error(request, 'No Priviliges')
        return redirect('errorpage')
    if request.method == 'POST':
        if request.POST['req_no']:
            req = Requests()
            req.number = request.POST['req_no']
            req.summary = request.POST['req_summary']
            req.date_fa = request.POST['date_fa']
            req.customer = Customer.objects.get(pk=request.POST['customer_id'])
            req.image = request.FILES['req_file']
            req.owner = request.user
            req.pub_date = timezone.datetime.now()
            req.save()
            return redirect('reqSpec_form', req_pk=req.pk)
        else:
            return render(request, 'requests/admin_jemco/yrequest/form.html', {'error': 'some field is empty'})
    return render(request, 'requests/admin_jemco/yrequest/form.html')


@login_required
def request_index(request):
    # requests = Requests.objects.all()
    can_index = funcs.has_perm_or_is_owner(request.user, 'request.index_requests')
    if not can_index:
        messages.error(request, 'Sorry No access...')
        return redirect('errorpage')
    requests = Requests.objects.filter(is_active=True).filter(owner=request.user)
    return render(request, 'requests/admin_jemco/yrequest/index.html', {'all_requests': requests})


@login_required
def request_find(request):
    if not Requests.objects.filter(is_active=True, number=request.POST['req_no']):
        messages.error(request, 'درخواست مورد نظر یافت نشد')
        return redirect('errorpage')
    req = Requests.objects.filter(is_active=True).get(number=request.POST['req_no'])
    return redirect('request_details', request_pk=req.pk)


@login_required
def request_read(request, request_pk):
    if not Requests.objects.filter(is_active=True).filter(pk=request_pk):
        messages.error(request, 'Nothin found')
        return redirect('errorpage')

    req = Requests.objects.filter(is_active=True).get(pk=request_pk)
    can_read = funcs.has_perm_or_is_owner(request.user, 'request.read_requests', req)
    if not can_read:
        messages.error(request, 'No access!!!')
        return redirect('errorpage')

    reqspecs = req.reqspec_set.all()
    req_images = req.requestfiles_set.all()
    kw = total_kw(request_pk)

    return render(request, 'requests/admin_jemco/yrequest/details.html', {
        'request': req,
        'reqspecs': reqspecs,
        'req_images': req_images,
        'total_kw': kw
    })


@login_required
def request_delete(request, request_pk):
    if not Requests.objects.filter(is_active=True, pk=request_pk):
        messages.error(request, 'Nothing found')
        return redirect('errorpage')
    req = Requests.objects.filter(is_active=True).get(pk=request_pk)
    can_delete = funcs.has_perm_or_is_owner(request.user, 'request.delete_requests', req)
    # can_delete = True
    if not can_delete:
        messages.error(request, 'No access')
        return redirect('errorpage')
    req.delete()
    # return redirect('request_index')
    return redirect('req_search')


@login_required
def request_edit(request, request_pk):
    if not Requests.objects.filter(is_active=True).filter(pk=request_pk):
        messages.error(request, 'Nothing found')
        return redirect('errorpage')
    return HttpResponse('request Edit' + str(request_pk))


@login_required
def pref_add(request):
    return render(request, 'test.html', {'is_add': True})


@login_required
def pref_insert(request):
    print('added to the db...')
    return render(request, 'test.html', {'is_add': True})


# add payment to the prefactor
@login_required
def payment_form(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_payment')
    if not can_add:
        messages.error(request, 'Sorry, No way to access')
        return redirect('errorpage')
    reqs, xprefs, xpayments = find_all_obj()
    return render(request, 'requests/admin_jemco/ypayment/form.html', {
        'reqs': reqs,
        'xprefs': xprefs,
        'xpayments': xpayments
    })


@login_required
def payment_insert(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_payment')
    if not can_add:
        messages.error(request, 'Sorry, No way to access')
        return redirect('errorpage')

    xpref = Xpref.objects.filter(is_active=True).get(number=request.POST['xpref_no'])
    payment = Payment()
    payment.xpref_id = xpref
    payment.amount = request.POST['amount']
    payment.number = request.POST['number']
    payment.date_fa = request.POST['date_fa']
    payment.summary = request.POST['summary']
    payment.owner = request.user
    payment.customer = xpref.req_id.customer
    payment.save()
    msg = 'payment added successfully'

    reqs, xprefs, xpayments = find_all_obj()

    payments = Payment.objects.filter(is_active=True)
    return render(request, 'requests/admin_jemco/ypayment/index.html', {
        'msg': msg,
        'reqs': reqs,
        'xprefs': xprefs,
        'xpayments': xpayments,
        'payments': payments
    })


@login_required
def payment_index(request):
    payments = Payment.objects.all()
    pref_sum = 0
    sum = 0

    for payment in payments:
        for spec in payment.xpref_id.prefspec_set.all():
            pref_sum += spec.price
        sum += payment.amount
    debt = sum - pref_sum
    debt_percent = debt / pref_sum
    return render(request, 'requests/admin_jemco/ypayment/index.html', {
        'payments': payments,
        'amount_sum': sum,
        'pref_sum': pref_sum,
        'debt': debt,
        'debt_percent': debt_percent,
    })


@login_required
def payment_find(request):
    payment = Payment.objects.filter(is_active=True).get(number=request.POST['payment_no'])
    return redirect('payment_details', ypayment_pk=payment.pk)


@login_required
def payment_details(request, ypayment_pk):
    payment = Payment.objects.filter(is_active=True).get(pk=ypayment_pk)
    return render(request, 'requests/admin_jemco/ypayment/payment_details.html', {'payment': payment})


@login_required
def payment_delete(request, ypayment_pk):
    payment = Payment.objects.filter(is_active=True).get(pk=ypayment_pk)
    can_delete = funcs.has_perm_or_is_owner(request.user, 'request.delete_payment', payment)
    if not can_delete:
        messages.error(request, 'No access!')
        return redirect('errorpage')
    payment.delete()
    payments = Payment.objects.filter(is_active=True)
    msg = 'payment deleted successfully...'
    # return render(request, 'requests/admin_jemco/ypayment/index.html', {'payments': payments, 'msg':msg})
    return redirect('payment_index')


@login_required
def payment_edit(request, ypayment_pk):
    payment = Payment.objects.filter(is_active=True).get(pk=ypayment_pk)
    can_edit = funcs.has_perm_or_is_owner(request.user, 'request.edit_payment', payment)
    if not can_edit:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')
    return HttpResponse('payment payment_edit')


# add spec to the prefactor
@login_required
def pref_spec_add(request):
    return HttpResponse('prefactor spec add')


@login_required
def pref_spec_details(request, ypref_spec_pk):
    return HttpResponse('prefactor spec details')


@login_required
def pref_spec_del(request, ypref_spec_pk):
    return HttpResponse('prefactor spec delete')


@login_required
def pref_spec_edit(request, ypref_spec_pk):
    return HttpResponse('prefactor spec edit')


@login_required
def pref(request, ypref_pk):
    if request.method == 'POST':
        if '_METHOD' not in request.POST:
            # Do post request
            return HttpResponse('this is a post request')
        else:
            if request.POST['_METHOD'] == 'PUT':
                # Do put request
                return HttpResponse('this is a put request')
            elif request.POST['_METHOD'] == 'DELETE':
                return HttpResponse('this is a delete request')

    elif request.method == 'GET':
        list = allRequests()
        return render(request, 'test.html', {
            'ypref_pk': ypref_pk,
            'is_add': False,
        })
        # return render(request, 'requests/admin_jemco/prefactor/create2.html', {
        #     'list': list,
        #     'ypref_pk': ypref_pk
        # })
        # return render(request, 'test.html', {'ypref_pk': ypref_pk})


    # return HttpResponse('this is from a single line of code for: ' + str(ypref_ipk))



def total_kw(req_id):
    req = Requests.objects.filter(is_active=True).get(pk=req_id)
    reqspecs = req.reqspec_set.all()
    total_kw = 0
    for reqspec in reqspecs:
        total_kw += reqspec.kw * reqspec.qty
    return total_kw


@login_required
def pay_form(request):
    if request.method == 'POST':
        form = forms.PaymentFrom(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.owner = request.user
            payment.customer = payment.xpref_id.req_id.customer
            payment.save()

            return redirect('payment_index')
    else:
        form = forms.PaymentFrom()

    payments = Payment.objects.filter(is_active=True)
    return render(request, 'requests/admin_jemco/ypayment/payment_form.html', {
        'form': form,
        'xpayments': payments
    })


@login_required
def request_edit_form(request, request_pk):

    # 1- check for permissions
    # 2 - find request and related images
    # 3 - make request image form
    # 4 - prepare image name to use in template
    # 5 - get the list of files from request
    # 6 - if form is valid the save request and its related images
    # 7 - render the template file

    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_requests')
    if not can_add:
        messages.error(request, 'Sorry, You need some priviliges to do this.')
        return redirect('errorpage')

    req = Requests.objects.filter(is_active=True).get(pk=request_pk)
    req_images = req.requestfiles_set.all()
    img_names = {}
    for r in req_images:
        name = r.image.name
        newname = name.split('/')
        las = newname[-1]
        img_names[r.pk] = las
    form = forms.RequestFrom(request.POST or None, request.FILES or None, instance=req)
    img_form = forms.RequestFileForm(request.POST, request.FILES)
    files = request.FILES.getlist('image')
    if form.is_valid() and img_form.is_valid():
        req_item = form.save(commit=False)
        req_item.owner = request.user
        req_item.save()
        for f in files:
            file_instance = models.RequestFiles(image=f, req=req_item)
            file_instance.save()
        # return redirect('request_index')
        return redirect('req_search')

    return render(request, 'requests/admin_jemco/yrequest/req_form.html', {
        'form': form,
        'req_img': img_form,
        'req_images': req_images,
        'img_names': img_names
    })


@login_required
def image_delete(request, img_pk):

    img = models.RequestFiles.objects.get(pk=img_pk)
    req = img.req
    imgForm = forms.RequestFileForm(instance=img)
    imgForm.delete()
    return True

@login_required
def img_del(request, img_pk):
    print(request)
    # with ajax
    # image = models.RequestFiles.objects.get(pk=request.POST['id'])

    # withour ajax
    image = models.RequestFiles.objects.get(pk=img_pk)
    req = image.req

    # auto_delete_file_on_delete(sender=,instance=image)


    image.delete()

    return redirect('request_edit_form', request_pk=req.pk)


@login_required
def prof_img_del(request, img_pk):
    # withour ajax
    image = models.ProfFiles.objects.get(pk=img_pk)
    prof = image.prof

    image.delete()

    return redirect('pref_edit2', ypref_pk=prof.pk)

