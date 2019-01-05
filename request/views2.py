from datetime import datetime
import jdatetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages

from request.views import allRequests, find_all_obj
from .models import Requests
from .models import Xpref, Payment
from . import models
from customer.models import Customer
from django.contrib.auth.decorators import login_required
import request.templatetags.functions as funcs
from request.forms import forms
import nested_dict as nd
from collections import defaultdict as dd


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
        messages.error(request, 'عدم دستری کافی!')
        return redirect('errorpage')

    file_instance = forms.RequestFileForm()
    if request.method == 'POST':
        c_cookie = request.COOKIES.get('customer')
        print(f"coockie: {c_cookie}")
        form = forms.RequestFrom(request.POST or None, request.FILES or None)
        img_form = forms.RequestFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        # customer = Customer.objects.get(name=request.POST['cu'])
        customer = Customer.objects.get(pk=c_cookie)
        if form.is_valid() and img_form.is_valid():
            req_item = form.save(commit=False)
            req_item.owner = request.user
            print(f"autocomplete user is: {customer}")
            req_item.customer = customer
            req_item.save()
            for f in files:
                file_instance = models.RequestFiles(image=f, req=req_item)
                file_instance.save()
            return redirect('spec_form', req_pk=req_item.pk)
    else:
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
    # requests =request_form Requests.objects.all()
    can_index = funcs.has_perm_or_is_owner(request.user, 'request.index_requests')
    if not can_index:
        messages.error(request, 'عدم دسترسی کافی!')
        return redirect('errorpage')
    # requests = Requests.objects.filter(owner=request.user).order_by('date_fa').reverse()
    # requests = Requests.objects.all().order_by('date_fa').reverse()
    today = jdatetime.date.today()

    requests = Requests.objects.all().order_by('date_fa').reverse()
    print(f'super user: {request.user.is_superuser}')
    if not request.user.is_superuser:
        requests = requests.filter(owner=request.user)
    response = {}

    date_format = "%m/%d/%Y"
    for req in requests:
        diff = today - req.date_fa
        print(f'diff is: {diff.days}')
        response[req.pk] = {
            'req': req,
            'delay': diff.days,
            'colleagues': req.colleagues.all(),
        }
    print(response)
    if request.user.is_superuser:
        requests = Requests.objects.all().order_by('date_fa').reverse()
    context = {
        'all_requests': requests,
        'response': response
    }
    return render(request, 'requests/admin_jemco/yrequest/index.html', context)


@login_required
def request_find(request):
    req = Requests.objects.get(number=request.POST['req_no'])
    return redirect('request_details', request_pk=req.pk)


@login_required
def request_read(request, request_pk):
    if not Requests.objects.filter(pk=request_pk):
        messages.error(request, 'درخواست مورد نظر یافت نشد')
        return redirect('errorpage')

    req = Requests.objects.get(pk=request_pk)
    colleagues = req.colleagues.all()
    print(f'colleagues: {colleagues}')
    colleague = False
    if request.user in colleagues:
        colleague = True

    can_read = funcs.has_perm_or_is_owner(request.user, 'request.read_requests', req, colleague)
    if not can_read:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

    reqspecs = req.reqspec_set.all()
    req_files = req.requestfiles_set.all()
    req_imgs = []
    req_pdfs = []
    req_words = []
    req_other_files = []
    files = {}
    nested_files = nd.nested_dict()
    # default_nested_files = dd.default_factory()

    xfiles = {
        'img': {},
        'pdf': {},
        'doc': {},
        'other': {},
    }

    for f in req_files:
        if str(f.image).lower().endswith('.jpg') or str(f.image).lower().endswith('.jpeg') or str(f.image).lower().endswith('.png'):
            req_imgs.append(f)
            nested_files['ximg'][f.pk]['url'] = f.image.url
            nested_files['ximg'][f.pk]['name'] = f.image.name.split('/')[-1]
            # nested_files['img']['name'] = f.image.name.split('/')
            xfiles['img'][f.pk] = {}
            xfiles['img'][f.pk]['url'] = f.image.url
            xfiles['img'][f.pk]['name'] = f.image.name.split('/')[-1]
        elif str(f.image).lower().endswith('.pdf'):
            req_pdfs.append(f)
            nested_files['pdf']['url'] = f.image.url
            nested_files['pdf']['name'] = f.image.name.split('/')[-1]
            xfiles['pdf'][f.pk] = {}
            xfiles['pdf'][f.pk]['url'] = f.image.url
            xfiles['pdf'][f.pk]['name'] = f.image.name.split('/')[-1]

        elif str(f.image).lower().endswith('.doc'):
            req_words.append(f)
            xfiles['doc'][f.pk] = {}
            xfiles['doc'][f.pk]['url'] = f.image.url
            xfiles['doc'][f.pk]['name'] = f.image.name.split('/')[-1]
        else:
            req_other_files.append(f)
            xfiles['other'][f.pk] = {}
            xfiles['other'][f.pk]['url'] = f.image.url
            xfiles['other'][f.pk]['name'] = f.image.name.split('/')[-1]

    files['req_imgs'] = req_imgs
    files['req_pdfs'] = req_pdfs
    files['req_words'] = req_words
    files['req_other_files'] = req_other_files

    img_names = {}
    for r in req_files:
        name = r.image.name
        newname = name.split('/')
        las = newname[-1]
        img_names[r.pk] = las

    for x, y in nested_files['ximg'].items():
        print(f"last is: {y['name']}")

    print(f'file names: {nested_files}')

    kw = total_kw(request_pk)
    context = {
        'request': req,
        'reqspecs': reqspecs,
        'req_images': req_files,
        'total_kw': kw,
        'files': files,
        'nested_files': nested_files,
        'xfiles': xfiles
    }
    return render(request, 'requests/admin_jemco/yrequest/details.html', context)


@login_required
def request_delete(request, request_pk):
    if not Requests.objects.filter(pk=request_pk):
        messages.error(request, 'Nothing found')
        return redirect('errorpage')
    req = Requests.objects.get(pk=request_pk)
    can_delete = funcs.has_perm_or_is_owner(request.user, 'request.delete_requests', req)
    if not can_delete:
        messages.error(request, 'No access')
        return redirect('errorpage')
    if request.method == 'GET':
        context = {
            'id': req.pk,
            'fn': 'req_del',
        }
        return render(request, 'general/confirmation_page.html', context)
    elif request.method == 'POST':
        req.delete()
    return redirect('request_index')


@login_required
def request_edit(request, request_pk):
    if not Requests.objects.filter(pk=request_pk):
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
    req = Requests.objects.get(pk=req_id)
    reqspecs = req.reqspec_set.all()
    total_kw = 0
    for reqspec in reqspecs:
        total_kw += reqspec.kw * reqspec.qty
    return total_kw




@login_required
def request_edit_form(request, request_pk):

    # 1- check for permissions
    # 2 - find request and related images
    # 3 - make request image form
    # 4 - prepare image name to use in template
    # 5 - get the list of files from request
    # 6 - if form is valid the save request and its related images
    # 7 - render the template file
    if not Requests.objects.filter(pk=request_pk):
        messages.error(request, 'Nothin found')
        return redirect('errorpage')
    req = Requests.objects.get(pk=request_pk)
    colleagues = req.colleagues.all()
    colleague = False
    if request.user in colleagues:
        colleague = True
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.edit_requests', colleague=colleague)
    if not can_add:
        messages.error(request, 'عدم دسترسی کافی')
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
    form = forms.RequestFrom(request.POST or None, request.FILES or None, instance=req)
    img_form = forms.RequestFileForm(request.POST, request.FILES)
    files = request.FILES.getlist('image')
    if form.is_valid() and img_form.is_valid():
        req_item = form.save(commit=False)
        # req_item.owner = request.user
        req_item.save()
        for f in files:
            file_instance = models.RequestFiles(image=f, req=req_item)
            file_instance.save()
        return redirect('request_index')

    context = {
        'form': form,
        'req_img': img_form,
        'req_images': req_images,
        'img_names': img_names
    }
    return render(request, 'requests/admin_jemco/yrequest/req_form.html', context)


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


def payment_form2(request):
    return HttpResponse('hello world')