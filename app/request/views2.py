import xlwt
import json
import jdatetime
from datetime import datetime

from django.db.models import Q, Sum, F, FloatField, Count
from django.core.cache import cache
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from req_track.models import ReqEntered
from request.filters.filters import RequestFilter
from request.forms.forms import RequestCopyForm, CommentForm
from request.forms.search import ReqSearchForm
from .models import Requests, ReqSpec, PrefSpec
from .models import Xpref, Payment
from . import models
from customer.models import Customer
import request.templatetags.functions as funcs
from request.forms import forms, search
from core.access_control.permission_check import OrderProxy, AccessControl, ProformaProxy, SpecProxy
from core.access_control.decorator import check_perm
import nested_dict as nd
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from request.models import Requests, ReqSpec, Xpref, PrefSpec
from django.db import models
from django.db.models import Sum, FloatField, ExpressionWrapper, F, Value, Count, Avg, Max, Min
from django.db.models.functions import Concat, TruncMonth
from accounts.models import User
from request.models import Requests
from accounts.models import User
from req_track.models import ReqEntered

User = get_user_model()


# Create your views here.
@login_required
@check_perm('request.add_requests', OrderProxy)
def request_form(request):
    acl_obj = ProformaProxy(request.user, 'request.add_requests')
    is_allowed = AccessControl(acl_obj).allow()
    # is_allowed = funcs.has_perm_or_is_owner(request.user, 'request.add_requests')
    if not is_allowed:
        messages.error(request, 'Sorry, You need some priviliges to do this.')
        return redirect('errorpage')

    req = Requests()
    customers = Customer.objects.all()
    return render(request, 'requests/admin_jemco/yrequest/form.html', {
        'req': req,
        'customers': customers,
    })


@login_required
@check_perm('request.add_requests', OrderProxy)
def req_form_copy(request):
    # acl_obj = OrderProxy(request.user, 'request.add_requests')
    # is_allowed = AccessControl(acl_obj).allow()
    # is_allowed = funcs.has_perm_or_is_owner(request.user, 'request.add_requests', )
    # if not is_allowed:
    #     messages.error(request, 'عدم دسترسی کافی')
    #     return redirect('errorpage')

    if request.method == 'POST':
        form = RequestCopyForm(request.POST or None)
        if form.is_valid():
            req_no = form.cleaned_data['number']
            if form.cleaned_data['new_number']:
                has_parent = False
                new_numebr = form.cleaned_data['new_number']
            else:
                has_parent = True
            if not Requests.objects.filter(is_active=True).filter(number=req_no):
                messages.error(request, 'درخواست مورد نظر یافت نشد.')
                return redirect('errorpage')

            master_req = Requests.objects.filter(is_active=True).get(number=req_no)
            can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_requests', instance=master_req)
            if not can_add:
                messages.error(request, 'عدم دسترسی کافی')
                return redirect('errorpage')

            reqspec_sets = master_req.reqspec_set.all()
            temp_number = master_req.number
            master_req.pk = None
            if has_parent:
                master_req.parent_number = temp_number
                # last_request = Requests.objects.filter(is_active=True).filter(parent_number__isnull=False).order_by('number').last()
                master_req.number = Requests.objects.order_by('number').last().number + 1
            else:
                if not Requests.objects.filter(number=new_numebr):
                    master_req.number = new_numebr
                else:
                    messages.error(request, 'درخواست با این شماره موجود است.')
                    return redirect('errorpage')

            master_req.save()

            for s in reqspec_sets:
                s.pk = None
                s.req_id = master_req
                s.save()
            messages.error(request, f"درخواست شماره {master_req.number} از درخواست شماره {temp_number} کپی گردید.")
            return redirect('spec_form', request_pk=master_req.pk)

    if request.method == 'GET':
        form = RequestCopyForm()

    context = {
        'form': form,
    }
    return render(request, 'requests/admin_jemco/yrequest/req_form_copy.html', context)


@login_required
@check_perm('request.add_requests', OrderProxy)
def req_form(request):
    file_instance = forms.RequestFileForm()
    if request.method == 'POST':
        form = forms.RequestFrom(request.POST or None, request.FILES or None)
        img_form = forms.RequestFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        customer_id = form.data.get('cu_value')
        customer = Customer.objects.get(pk=customer_id)
        if form.is_valid() and img_form.is_valid():
            req_item = form.save(commit=False)
            req_item.owner = request.user
            req_item.customer = customer
            # year = jdatetime.date.today().year
            year = req_item.date_fa.year
            req_item.number = str(int(str(year)[2:4]) * 10000 + int(request.POST['number']))
            req_item.save()
            form.save_m2m()
            for f in files:
                file_instance = models.RequestFiles(image=f, req=req_item)
                file_instance.save()
            return redirect('spec_form', request_pk=req_item.pk)
    else:
        form = forms.RequestFrom()
        file_instance = forms.RequestFileForm()

    context = {
        'form': form,
        'req_img': file_instance,
        'add_new': True,
    }
    return render(request, 'requests/admin_jemco/yrequest/req_form.html', context)


@login_required
def wrong_data(request):
    probably_wrong = ReqSpec.objects.filter(is_active=True).all()
    if not request.user.is_superuser:
        probably_wrong = probably_wrong.filter(req_id__owner=request.user)
    probably_wrong = probably_wrong.filter(
        Q(rpm__lt=700) |
        Q(rpm__gt=750, rpm__lte=940) |
        Q(rpm__gt=1000, rpm__lte=1450) |
        Q(rpm__gt=1500, rpm__lt=2940) |
        Q(kw__gt=10000) |
        Q(kw__lt=1)
    )

    context = {
        'reqspecs': probably_wrong,
    }
    return render(request, 'requests/admin_jemco/yreqspec/wrong_data.html', context)


@login_required
def wrong_data2(request):
    probably_wrong = ReqSpec.objects.filter(is_active=True).all()
    if not request.user.is_superuser:
        probably_wrong = probably_wrong.filter(req_id__owner=request.user)
    probably_wrong = probably_wrong.filter(
        Q(rpm__lt=700) |
        Q(rpm__gt=750, rpm__lt=1000) |
        Q(rpm__gt=1000, rpm__lt=1500) |
        Q(rpm__gt=1500, rpm__lt=3000)
    ).exclude(type__title='تعمیرات')

    context = {
        'reqspecs': probably_wrong,
    }
    return render(request, 'requests/admin_jemco/yreqspec/wrong_data.html', context)


def function_define(request, specs):
    form_data = {}
    if request['date_min']:
        form_data['date_min'] = (request['date_min'])
        specs = specs.filter(req_id__date_fa__gte=form_data['date_min'])
    if request['date_max']:
        form_data['date_max'] = (request['date_max'])
        specs = specs.filter(req_id__date_fa__lte=form_data['date_max'])
    if request['kw_min']:
        form_data['kw_min'] = (request['kw_min'])
        specs = specs.filter(kw__gte=form_data['kw_min'])
    if request['kw_max']:
        form_data['kw_max'] = (request['kw_max'])
        specs = specs.filter(kw__lte=form_data['kw_max'])
    if request['owner'] and request['owner'] != '0':
        form_data['owner'] = (request['owner'])
        owner = User.objects.get(pk=form_data['owner'])
        specs = specs.filter(Q(req_id__owner=owner))
    form_data['price'] = request.get('price')
    form_data['tech'] = request.get('tech')
    form_data['type'] = request.get('type')
    form_data['permission'] = request.get('permission')
    form_data['sent'] = request.get('sent')
    form_data['item_per_page'] = request.get('item_per_page')
    if form_data['price'] != '0':
        specs = specs.filter(price=form_data['price'])
    if form_data['tech'] != '0':
        specs = specs.filter(tech=form_data['tech'])
    if form_data['type'] != '0':
        specs = specs.filter(type__title=form_data['type'])
    if form_data['permission'] != '0':
        specs = specs.filter(permission=form_data['permission'])
    if form_data['sent'] != '0':
        specs = specs.filter(sent=form_data['sent'])

    if request['rpm']:
        rpm = form_data['rpm'] = int(request['rpm'])

        specs = specs.filter(rpm=rpm)
    if request['customer_name']:
        form_data['customer_name'] = request['customer_name']
        specs = specs.filter(req_id__customer__name__icontains=form_data['customer_name'])
    if request['sort_by']:
        form_data['sort_by'] = request['sort_by']
        if form_data['sort_by'] == '1':
            specs = specs.order_by('kw')
        # if form_data['sort_by'] == '2':
        #     specs = specs.order_by('req_id__customer__name')
        if form_data['sort_by'] == '3':
            specs = specs.order_by('req_id__date_fa')
        if form_data['sort_by'] == '4':
            specs = specs.order_by('qty')
    if request['dsc_asc'] == '2':
        form_data['dsc_asc'] = request['dsc_asc']
        specs = specs.reverse()
    return form_data, specs


@login_required
@check_perm('request.index_reqspecs', SpecProxy)
def reqspec_search(request):
    form_data = {}

    if not request.method == 'POST':
        if 'reqspec-search-post' in request.session:
            request.POST = request.session['reqspec-search-post']
            request.method = 'POST'

    specs = ReqSpec.objects.filter(req_id__is_active=True).prefetch_related('req_id', 'req_id__owner', 'req_id__customer', 'req_id__colleagues', 'type', 'req_id__xpref_set', 'req_id__xpref_set__payment_set')
    if request.method == 'POST':
        # specs = ReqSpec.objects
        request.session['reqspec-search-post'] = request.POST

        (form_data, specs,) = function_define(request.POST, specs)
        search_form = search.SpecSearchForm(form_data)
        item_per_page = form_data['item_per_page']

    else:
        form_data['price'] = 'False'
        form_data['tech'] = 'False'
        item_per_page = 50
        specs = ReqSpec.objects.filter(req_id__is_active=True, price=form_data['price'], tech=form_data['tech'])\
            .prefetch_related('req_id', 'req_id__owner', 'req_id__customer', 'req_id__colleagues', 'type', 'req_id__xpref_set', 'req_id__xpref_set__payment_set')
        search_form = search.SpecSearchForm(form_data)

    today = jdatetime.date.today()

    date_format = "%m/%d/%Y"
    if not request.user.is_superuser:
        specs = specs.filter(req_id__owner=request.user) | specs.filter(req_id__colleagues=request.user)

    paginator = Paginator(specs, item_per_page)
    page = request.GET.get('page')
    specs_to_render = paginator.get_page(page)

    qty = specs.aggregate(sum=Sum('qty'))
    kw = specs.aggregate(sum=Sum(F('kw') * F('qty'), output_field=FloatField()))

    context = {
        'reqspecs': specs_to_render,
        'total_kw': kw['sum'],
        'total_qty': qty['sum'],
    }

    cache.set('spec_in_sessions', context, 300)

    context.update({
        'search_form': search_form,
    })
    return render(request, 'requests/admin_jemco/yreqspec/index_opt.html', context)


@login_required
def reqspec_clear_cache(request):
    if 'reqspec-search-post' in request.session:
        request.session.pop('reqspec-search-post')
    return redirect('reqspec_search')


@login_required
def spec_export(request):
    try:
        # specs = request.session['spec_in_sessions']
        context = cache.get('spec_in_sessions')
        specs = context['reqspecs']
        total_kw = context['total_kw']
        total_qty = context['total_qty']
    except:
        specs = ReqSpec.objects.filter(is_active=True)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="specs.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('الکتروموتور')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = (
        'ردیف',
        'شماره درخواست',
        'مشتری',
        'کیلووات',
        'سرعت',
        'ولتاژ',
        'تعداد',
        'نوع پروژه',
        'کارشناس',
        'پیش فاکتور',
        'پرداخت',
        'زمان',
    )

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    temp_request = {}
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    # if request.user.is_superuser:
    #     pass
    for spec in specs:
        row_num += 1

        exportables = []
        exportables.append(row_num)
        exportables.append(spec.req_id.number)
        exportables.append(spec.req_id.customer.name)
        exportables.append(spec.kw)
        exportables.append(spec.rpm)
        exportables.append(spec.voltage)
        exportables.append(spec.qty)
        exportables.append(spec.type.title)
        exportables.append(spec.req_id.owner.last_name)

        prof_str = ''
        pay_str = ''
        profs = spec.req_id.xpref_set.all()
        for x in profs:
            prof_str += f"{str(x.number)} - "
            payments = x.payment_set.all()
            if payments.count() > 0:
                for y in payments:
                    pay_str += f"{str(y.amount)} - "
        exportables.append(prof_str)
        exportables.append(pay_str)
        for col_num in range(len(exportables)):
            ws.write(row_num, col_num, exportables[col_num], font_style)

    row_num += 2

    ws.write(row_num, 0, 'مجموع ', font_style)
    ws.write(row_num, 1, 'کیلووات ', font_style)
    ws.write(row_num, 2, 'توان ', font_style)

    row_num += 1
    ws.write(row_num, 0, '', font_style)
    ws.write(row_num, 1, total_qty, font_style)
    ws.write(row_num, 2, total_kw, font_style)

    ws.cols_right_to_left = True
    wb.save(response)
    return response


def proforma_total(spset):
    sum = 0
    for s in spset:
        sum += s.qty * s.price
    return sum


def fsearch3(request):
    acl_obj = OrderProxy(request.user, 'request.index_requests')
    is_allowed = AccessControl(acl_obj).allow()
    # is_allowed = funcs.has_perm_or_is_owner(request.user, 'request.index_requests')
    if not is_allowed:
        messages.error(request, 'عدم دسترسی کافی!')
        return redirect('errorpage')
    context = {
        'search_form': search.SpecSearchForm()
    }
    return render(request, 'requests/admin_jemco/yreqspec/index-vue.html', context)


@login_required
def request_insert(request):
    acl_obj = OrderProxy(request.user, 'request.add_requests')
    is_allowed = AccessControl(acl_obj).allow()
    # is_allowed = funcs.has_perm_or_is_owner(request.user, 'request.add_requests')
    if not is_allowed:
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
            return redirect('reqSpec_form', request_pk=req.pk)
        else:
            return render(request, 'requests/admin_jemco/yrequest/form.html', {'error': 'some field is empty'})
    return render(request, 'requests/admin_jemco/yrequest/form.html')


@login_required
def req_to_follow(request, request_pk):
    acl_obj = OrderProxy(request.user, 'request.index_requests')
    is_allowed = AccessControl(acl_obj).allow()
    # is_allowed = funcs.has_perm_or_is_owner(request.user, 'request.index_requests')
    if not is_allowed:
        messages.error(request, 'عدم دسترسی کافی!')
        return redirect('errorpage')

    req = Requests.objects.get(pk=request_pk)
    req.to_follow = not req.to_follow
    req.on = req.to_follow
    req.save()

    if req.to_follow:
        comment = req.comments.create(author=request.user, body='وضعیت درخواست؟')
        comment.is_read = False
        comment.save()

    return redirect('req_report')


@login_required
def request_index_vue_deleted(request):
    acl_obj = OrderProxy(request.user, 'request.index_deleted_requests')
    is_allowed = AccessControl(acl_obj).allow()
    # is_allowed = funcs.has_perm_or_is_owner(request.user, 'request.index_deleted_requests')
    if not is_allowed:
        messages.error(request, 'عدم دسترسی کافی!')
        return redirect('errorpage')
    # requests = Requests.objects.filter(owner=request.user).order_by('date_fa').reverse()
    # requests = Requests.objects.all().order_by('date_fa').reverse()
    today = jdatetime.date.today()
    requests = Requests.objects.filter(is_active=False).order_by('date_fa').reverse()
    # if not request.user.is_superuser:
    #     requests = requests.filter(owner=request.user)
    response = {}
    date_format = "%m/%d/%Y"
    for req in requests:
        diff = today - req.date_fa
        response[req.pk] = {
            'req': req,
            'delay': diff.days,
            'colleagues': req.colleagues.all(),
        }
    # if request.user.is_superuser:
    #     requests = Requests.objects.filter(is_active=False).order_by('date_fa').reverse()
    context = {
        'all_requests': requests,
        'response': response,
        'showHide': False,
        'message': 'درخواست های حذف شده',
    }
    return render(request, 'requests/admin_jemco/yrequest/vue/index.html', context)


@login_required
def request_find(request):
    req_no = str(int(request.POST['year']) * 10000 + int(request.POST['req_no']))
    if not Requests.objects.filter(number=req_no):
        messages.error(request, 'درخواست مورد نظر یافت نشد.')
        return redirect('req_report')
    req = Requests.objects.filter(is_active=True).get(number=req_no)
    return redirect('request_details', request_pk=req.pk)


@login_required
@check_perm('request.read_requests', OrderProxy)
def request_read(request, request_pk):
    req = Requests.objects.get(pk=request_pk)
    if not request.user.is_superuser:
        req.edited_by_customer = False
        req.save()

    reqspecs = req.reqspec_set.filter(is_active=True)
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
        if str(f.image).lower().endswith('.jpg') or str(f.image).lower().endswith('.jpeg') or str(
                f.image).lower().endswith('.png'):
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

    parent_request = Requests.objects.filter(is_active=True).filter(number=req.parent_number)
    sub_requests = Requests.objects.filter(is_active=True).filter(parent_number=req.number)

    if request.method == 'POST':
        comment = req.comments.create(author=request.user, body=request.POST['body'])
        req.comments.all().update(is_read=True)
        comment.is_read = False
        comment.save()

    context = {
        'request': req,
        'sub_requests': sub_requests,
        'parent_request': parent_request,
        'reqspecs': reqspecs,
        'req_images': req_files,
        'files': files,
        'nested_files': nested_files,
        'xfiles': xfiles,
        'comment_form': CommentForm(),
    }
    return render(request, 'requests/admin_jemco/yrequest/details.html', context)


@login_required
@check_perm('request.delete_requests', OrderProxy)
def request_delete(request, request_pk):
    req = Requests.objects.filter(is_active=True).get(pk=request_pk)
    if request.method == 'GET':
        context = {
            'id': req.pk,
            'fn': 'req_del',
        }
        return render(request, 'general/confirmation_page.html', context)
    elif request.method == 'POST':
        # req.delete()
        req.is_active = False
        req.temp_number = req.number
        rand_num = random.randint(100000, 200000)
        while Requests.objects.filter(number=rand_num):
            rand_num = random.randint(100000, 200000)
        req.number = rand_num
        req.save()
        req.reqspec_set.update(is_active=False)

    return redirect('req_report')


@login_required
@check_perm('request.change_requests', OrderProxy)
def request_edit_form(request, request_pk):
    # 1- check for permissions
    # 2 - find request and related images
    # 3 - make request image form
    # 4 - prepare image name to use in template
    # 5 - get the list of files from request
    # 6 - if form is valid the save request and its related images
    # 7 - render the template file

    req = Requests.objects.filter(is_active=True).get(pk=request_pk)

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
        if form.data.get('cu_value'):
            customer_id = form.data.get('cu_value')
            customer = Customer.objects.get(pk=customer_id)
            req_item.customer = customer
        req_item.save()
        form.save_m2m()
        for f in files:
            file_instance = models.RequestFiles(image=f, req=req_item)
            file_instance.save()
        # return redirect('request_index')
        return redirect('req_report')

    context = {
        'customer': req.customer.name,
        'form': form,
        'req_img': img_form,
        'req_images': req_images,
        'img_names': img_names,
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


@login_required
def payment_form2(request):
    return HttpResponse('hello world')


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, jdatetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj)
        return super().default(obj)


@login_required
@check_perm('request.index_requests', OrderProxy)
def req_report(request):
    req_list = Requests.objects.filter(is_active=True).order_by('date_fa').reverse()
    acl_obj = OrderProxy(user=request.user)
    req_list = req_list.filter(acl_obj.show())

    req_filter = RequestFilter(request.GET, queryset=req_list)
    if not request.method == 'POST':
        if 'search-persons-post' in request.session:
            request.POST = request.session['search-persons-post']
            request.method = 'POST'

    if request.method == 'POST':
        form = ReqSearchForm(request.POST or None)
        request.session['search-persons-post'] = request.POST
        if request.POST['customer_name']:
            if Customer.objects.filter(name=request.POST['customer_name']):
                customer = Customer.objects.get(name=request.POST['customer_name'])
                req_list = req_list.filter(customer=customer)
            else:
                req_list = req_list.filter(customer__name__contains=request.POST['customer_name'])
        if request.POST['owner'] and request.POST['owner'] != '0':
            owner = User.objects.get(pk=request.POST['owner'])
            req_list = req_list.distinct().filter(Q(owner=owner) | Q(colleagues=owner))
        if request.POST['date_min']:
            req_list = req_list.filter(date_fa__gte=request.POST['date_min'])
        if request.POST['date_max']:
            req_list = req_list.filter(date_fa__lte=request.POST['date_max'])
        if request.POST['status'] and request.POST['status'] != '0':
            status = request.POST['status']
            if status == 'no_prof':
                req_list = req_list.filter(xpref__isnull=True)
            elif status == 'close':
                req_list = req_list.filter(finished=True)
            elif status == 'open':
                req_list = req_list.filter(finished=False)
            elif status == 'to_follow':
                req_list = req_list.filter(to_follow=True)

        if request.POST['sort_by']:
            req_list = req_list.order_by(f"{request.POST['sort_by']}")
        if request.POST['dsc_asc'] == '1':
            req_list = req_list.reverse()
    if request.method == 'GET':
        form = ReqSearchForm()

    req_list = req_list.annotate(qty=Sum('reqspec__qty'))
    qty = req_list.aggregate(sum=Sum('qty'))
    req_list = req_list.annotate(kw=Sum(F('reqspec__qty') * F('reqspec__kw'), output_field=FloatField()))
    kw = req_list.aggregate(sum=Sum('kw'))

    page = request.GET.get('page', 1)
    orders_list = req_list
    paginator = Paginator(orders_list, 30)
    try:
        req_page = paginator.page(page)
    except PageNotAnInteger:
        req_page = paginator.page(1)
    except EmptyPage:
        req_page = paginator.page(paginator.num_pages)
    context = {
        'fil': req_filter,
        'req_page': req_page,
        'form': form,
        'qty': qty,
        'kw': kw,
    }
    return render(request, 'requests/admin_jemco/yrequest/search_index2.html', context)


@login_required
def request_report_cc(request):
    if 'search-persons-post' in request.session:
        request.session.pop('search-persons-post')
    return redirect('req_report')


@login_required
def finish(request, request_pk):
    req = Requests.objects.get(pk=request_pk)
    req.finished = not req.finished
    req.save()
    return redirect('req_report')


def change_date_string(date):
    b = date.split('-')
    d = [int(i) for i in b]
    d[0] = str(d[0])
    for i in [1, 2]:
        d[i] = str(d[i]) if d[i] > 9 else '0' + str(d[i])
    date = '-'.join(d)
    return date


@login_required
def fetch_sales_data(request):
    data = json.loads(request.body.decode('utf-8'))
    by_date = data['by_date']

    today = jdatetime.date.today()
    if by_date:
        date_min = data['date_min']
        date_max = data['date_max']
        date_min = change_date_string(date_min)
        date_max = change_date_string(date_max)
        date_min = jdatetime.datetime.strptime(date_min, "%Y-%m-%d").date()
        date_max = jdatetime.datetime.strptime(date_max, "%Y-%m-%d").date()
        diff = date_max - date_min
        days = diff.days
    else:
        days = int(data['days'])
        date_min = today + jdatetime.timedelta(-days)
        date_max = today

    # if request.user.is_superuser:
    #     date_min = data['date_min']
    #     date_max = data['date_max']
    # else:
    #     days = 30
    #     today = jdatetime.date.today()
    #     startDate = today + jdatetime.timedelta(-days)
    #     date_min = startDate
    #     date_max = today

    res = []
    sales_queryset = User.objects.filter(sales_exp=True)
    for exp in sales_queryset:
        id = exp.pk
        name = exp.last_name
        perms_queryset = exp.perms(date_min=date_min, date_max=date_max)
        ps_qty = exp.perms(date_min=date_min, date_max=date_max)['ps_qty']['sum']
        ps_count = exp.perms(date_min=date_min, date_max=date_max)['ps_count']['count']
        count = perms_queryset['count']
        perms = perms_queryset['perms']
        price = exp.perms_price_total(date_min=date_min, date_max=date_max)['price']['sum']
        kw = exp.perms_price_total(date_min=date_min, date_max=date_max)['kw']['sum']
        perms_total_received = exp.perms_total_received(date_min=date_min, date_max=date_max)
        res.append({
            'id': id,
            'show_details': False,
            'name': name,
            'perms': [{
                'proforma_total': a.total_proforma_price_vat()['price_vat'],
                'perm_number': a.perm_number,
                'number_td': a.number_td,
                'total_received': f"{a.total_proforma_received()['received']}",
                'total_received_percentage': a.total_proforma_received()['received_percent'],
                'perm_receivable': a.total_proforma_received()['remaining'],
                'perm_receivable_percentage': a.total_proforma_received()['remaining_percent'],
                'proforma_number': a.number,
                'total_kw': a.total_kw(),
                'url': request.build_absolute_uri(reverse('pref_details', kwargs={'ypref_pk': a.pk})),
                'customer': a.req_id.customer.name,
                'customer_url': request.build_absolute_uri(reverse('customer_read', kwargs={'customer_pk': a.req_id.customer.pk})),
            } for a in perms],
            'count': count,
            'price': price,
            'kw': kw,
            'ps_qty': ps_qty,
            'ps_count': ps_count,
            'perms_total_received': perms_total_received,
        })

    # prefs = PrefSpec.objects.filter(xpref_id__perm_date__gte=date_min, xpref_id__perm_date__lte=date_max)
    prefs = PrefSpec.objects.filter(is_active=True, xpref_id__is_active=True,
                                    xpref_id__perm=True, price__gt=0, qty__gt=0,
                                    xpref_id__perm_date__gte=date_min, xpref_id__perm_date__lte=date_max)

    # if not by_date:
    #     prefs = prefs.filter(xpref_id__perm_date__gte=date_min, xpref_id__perm_date__lte=date_max)
    # elif by_date:
    #     prefs = prefs.filter(xpref_id__perm_date__gte=date_min)

    prefs = prefs.values('xpref_id', 'qty', 'price', 'kw', 'reqspec_eq__type__title', 'id')
    p = prefs.values('reqspec_eq__type__title').distinct()
    p2 = prefs.values('reqspec_eq__type__title').distinct().values('xpref_id', 'xpref_id__number')
    q = p.annotate(count=Sum('qty'))\
        .annotate(kw=Sum(F('qty') * F('kw'), output_field=FloatField()))\
        .annotate(price=Sum(1.09 * F('qty') * F('price'), output_field=FloatField()))
    ReqSpec.objects.filter(rpm_new__isnull=True)

    perms_count = prefs.values('xpref_id').distinct().aggregate(count=Count('xpref_id'))
    project_base = [{
        'type': a['reqspec_eq__type__title'],
        'kw': a['kw'],
        'count': a['count'],
        'price': a['price'],
        'pr_perms': [{
            'number': i['xpref_id__number'],
            'url': request.build_absolute_uri(reverse('pref_details', kwargs={'ypref_pk': i['xpref_id']})),
        } for i in p2.filter(reqspec_eq__type__title=a['reqspec_eq__type__title'])],
    } for a in q]

    context = {
        'response': res,
        'project_base': project_base,
        'perms_count': perms_count,
        'date_min': str(date_min),
        'date_max': str(date_max),
        'diff_days': days,
        # 'date_max': str(date_max),
    }
    return JsonResponse(context, safe=False)


@login_required
def find_by_number(request):
    data = json.loads(request.body.decode('utf-8'))
    number = data['number']
    proforma = Xpref.objects.filter(number=number).last()
    perm = Xpref.objects.filter(perm_number=number).last()
    context = dict()
    if proforma:
        context['proforma'] = {
                'type_slug': 'پیش فاکتور',
                'number': proforma.number,
                'id': proforma.pk,
                'customer': {
                    'id': proforma.req_id.customer.id,
                    'name': proforma.req_id.customer.name,
                }
            }
    if perm:
        context['perm'] = {
            'type_slug': 'مجوز',
            'number': perm.perm_number,
            'id': perm.pk,
            'customer': {
                'id': perm.req_id.customer.id,
                'name': perm.req_id.customer.name,
            }
        }

    return JsonResponse(context, safe=False)


@login_required
def index_by_month_exp(request):

    month = [
        {'start': '1397-10-01', 'end': '1397-10-30', 'name': 'دی'},
        {'start': '1397-11-01', 'end': '1397-11-30', 'name': 'بهمن'},
        {'start': '1397-12-01', 'end': '1397-11-29', 'name': 'اسفند'},
        {'start': '1398-01-01', 'end': '1398-01-31', 'name': 'فروردین'},
        {'start': '1398-02-01', 'end': '1398-02-31', 'name': 'اردیبهشت'},
        {'start': '1398-03-01', 'end': '1398-03-31', 'name': 'خرداد'},
        {'start': '1398-04-01', 'end': '1398-04-31', 'name': 'تیر'},
        {'start': '1398-05-01', 'end': '1398-05-31', 'name': 'مرداد'},
        {'start': '1398-05-01', 'end': '1398-05-31', 'name': 'مرداد'},
        {'start': '1398-06-01', 'end': '1398-06-31', 'name': 'شهریور'},
        {'start': '1398-07-01', 'end': '1398-07-30', 'name': 'مهر'},
        {'start': '1398-08-01', 'end': '1398-08-30', 'name': 'آبان'},
        {'start': '1398-09-01', 'end': '1398-09-30', 'name': 'آذر'},
        {'start': '1398-10-01', 'end': '1398-10-30', 'name': 'دی'},
        {'start': '1398-11-01', 'end': '1398-11-30', 'name': 'بهمن'},
        {'start': '1398-12-01', 'end': '1398-12-29', 'name': 'اسفند'},
        {'start': '1399-01-01', 'end': '1399-01-31', 'name': 'فروردین'},
        {'start': '1399-02-01', 'end': '1399-02-31', 'name': 'اردیبهشت'},
        {'start': '1399-03-01', 'end': '1399-03-31', 'name': 'خرداد'},
        {'start': '1399-04-01', 'end': '1399-04-31', 'name': 'تیر'},
        {'start': '1399-05-01', 'end': '1399-05-31', 'name': 'مرداد'},
    ]
    users = User.objects.filter(sales_exp=True)
    users_summary = list()
    reqs_per_month = list()
    for m in month:
        inner_data = list()
        index = f"{m['name']} - {m['start'].split('-')[0]}"
        # reqs = Requests.objects.filter(date_fa__gte=m['start'], date_fa__lte=m['end'], is_active=True)
        reqs = Requests.objects.filter(date_fa__gte=m['start'], date_fa__lte=m['end'])
        reqs_input = ReqEntered.objects.filter(date_fa__gte=m['start'], date_fa__lte=m['end'], is_request=True)
        inner_data.append(index)
        inner_data.append(reqs_input.count())
        for user in users:
            user_reqs = reqs.filter(owner=user)
            user_input = reqs_input.filter(owner_text__contains=user.last_name)
            inner_data.append(user_input.count())
            inner_data.append(user_reqs.count())

        inner_data.append(reqs.count())
        reqs_per_month.append(inner_data)
    context = {
        'users': users,
        'reqs_per_month': reqs_per_month
    }
    return render(request, 'requests/admin_jemco/yrequest/index_by_month_exp.html', context)


def order_valid(request, request_pk):
    from automation.helpers import helpers
    order = Requests.objects.get(pk=request_pk)
    if helpers.order_is_routine(order):
        proforma = helpers.create_proforma_from_order(order)
        helpers.create_proforma_specs(proforma)
        return redirect('pref_details', ypref_pk=proforma.pk)
    else:
        return redirect('request_details', request_pk=request_pk)
