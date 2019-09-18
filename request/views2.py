from django.core.cache import cache
import xlwt
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Q, Sum, F, FloatField, Count
from datetime import datetime
import json
import json_tricks
import jdatetime
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.defaultfilters import floatformat
from django.urls import reverse
from django.utils import timezone
# from django.utils.datetime_safe import strftime
from django.contrib.auth import get_user_model
User = get_user_model()

from request.filters.filters import RequestFilter
from request.forms.forms import RequestCopyForm, CommentForm
from request.forms.search import ReqSearchForm
from request.views import find_all_obj
from .models import Requests, ReqSpec, PrefSpec, IMType
from .models import Xpref, Payment
from . import models
from customer.models import Customer
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import request.templatetags.functions as funcs
from request.forms import forms, search
import nested_dict as nd
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
def req_form_copy(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_requests', )
    if not can_add:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

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
            can_add = funcs.has_perm_or_is_owner(request.user, 'request.copy_requests', instance=master_req)
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
            return redirect('spec_form', req_pk=master_req.pk)

    if request.method == 'GET':
        form = RequestCopyForm()

    context = {
        'form': form,
    }
    return render(request, 'requests/admin_jemco/yrequest/req_form_copy.html', context)


@login_required
def req_form(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_requests')
    if not can_add:
        messages.error(request, 'عدم دستری کافی!')
        return redirect('errorpage')

    file_instance = forms.RequestFileForm()
    if request.method == 'POST':
        c_cookie = request.COOKIES.get('customer')
        # print('this is reqeust cookies: ', request.COOKIES)
        # print('this is cookie: ', c_cookie)
        form = forms.RequestFrom(request.POST or None, request.FILES or None)
        img_form = forms.RequestFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        # customer = Customer.objects.get(name=request.POST['cu'])
        customer = Customer.objects.get(pk=c_cookie)
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
            return redirect('spec_form', req_pk=req_item.pk)
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
    return render(request, 'requests/admin_jemco/yreqspec/wrong_data.html', context)\


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
def reqspec_search(request):
    can_index = funcs.has_perm_or_is_owner(request.user, 'request.index_requests')
    if not can_index:
        messages.error(request, 'عدم دسترسی کافی!')
        return redirect('errorpage')
    form_data = {}
    # specs = ReqSpec.objects.filter(is_active=True)

    if not request.method == 'POST':
        if 'reqspec-search-post' in request.session:
            request.POST = request.session['reqspec-search-post']
            request.method = 'POST'

    # request.session['temp_request_in_session'] = request.POST

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


def fsearch2(request):
    can_index = funcs.has_perm_or_is_owner(request.user, 'request.index_requests')
    if not can_index:
        messages.error(request, 'عدم دسترسی کافی!')
        return redirect('errorpage')

    data = json.loads(request.body.decode('utf-8'))
    specs = ReqSpec.objects.filter(is_active=True)
    pmnt_total = Payment.objects.filter(is_active=True)

    if request.method == 'POST':
        form_data = {}
        form_data['price'] = data['price']
        form_data['tech'] = data['tech']
        form_data['permission'] = data['permission']
        form_data['sent'] = data['sent']
        form_data['customer_name'] = data['customer_name']
        form_data['kw_min'] = data['kw_min']
        form_data['kw_max'] = data['kw_max']
        form_data['rpm'] = data['rpm']
        form_data['date_min'] = data['date_min']
        form_data['date_max'] = data['date_max']
        # if request.POST['kw_min']:
        #     form_data['kw_min'] = (request.POST['kw_min'])
        #     specs = specs.filter(kw__gte=form_data['kw_min'])
        # if request.POST['kw_max']:
        #     form_data['kw_max'] = (request.POST['kw_max'])
        #     specs = specs.filter(kw__lte=form_data['kw_max'])
        if form_data['price']:
            specs = specs.filter(price=form_data['price'])
            # payments = payments.filter(xpref_id__req_id__price=form_data['price'])
        if form_data['permission']:
            specs = specs.filter(permission=form_data['permission'])
            # payments = payments.filter(xpref_id__req_id__price=form_data['permission'])
        if form_data['sent']:
            specs = specs.filter(sent=form_data['sent'])
            # payments = payments.filter(xpref_id__req_id__price=form_data['sent'])
        if form_data['tech']:
            specs = specs.filter(tech=form_data['tech'])
            # payments = payments.filter(xpref_id__req_id__price=form_data['tech'])
        if form_data['customer_name']:
            specs = specs.filter(req_id__customer__name__icontains=form_data['customer_name'])
            # payments = payments.filter(xpref_id__req_id__price=form_data['customer_name'])
        if form_data['kw_min']:
            specs = specs.filter(kw__gte=form_data['kw_min'])
            # payments = payments.filter(xpref_id__req_id__price=form_data['kw_min'])
        if form_data['kw_max']:
            specs = specs.filter(kw__lte=form_data['kw_max'])
            # payments = payments.filter(xpref_id__req_id__price=form_data['kw_max'])
        if form_data['date_min']:
            specs = specs.filter(req_id__date_fa__gte=form_data['date_min'])
            pmnt_total = pmnt_total.filter(date_fa__gte=form_data['date_min'])
            # payments = payments.filter(xpref_id__req_id__price=form_data['date_min'])
        if form_data['date_max']:
            specs = specs.filter(req_id__date_fa__lte=form_data['date_max'])
            pmnt_total = pmnt_total.filter(date_fa__lte=form_data['date_max'])
            # payments = payments.filter(xpref_id__req_id__price=form_data['date_max'])
        if form_data['rpm']:

            # specs = specs.filter(rpm=form_data['rpm'])
            rng = [750, 1000, 1500, 3000]
            i = 0
            if int(form_data['rpm']) <= rng[0]:
                form_data['rpm'] = rng[0]
            for r in rng:
                if r < int(form_data['rpm']) <= rng[i] and i > 0:
                    form_data['rpm'] = rng[i]
                i += 1
            if int(form_data['rpm']) > max(rng):
                form_data['rpm'] = 3000

            # specs = specs.filter(rpm=form_data['rpm'])
            specs = specs.filter(rpm=form_data['rpm'])
            # payments = payments.filter(xpref_id__req_id__price=form_data['rpm'])

        # if request.POST.get('sent') == 'true':
        #     form_data['sent'] = True
        #     specs = specs.filter(sent=form_data['sent'])

        # if request.POST.get('permission') == 'true':
        #     form_data['permission'] = True
        #     specs = specs.filter(permission=form_data['permission'])

        # if request.POST['rpm']:
        #     form_data['rpm'] = request.POST['rpm']
        #     specs = specs.filter(rpm=form_data['rpm'])
        # if request.POST['customer_name']:
        #     form_data['customer_name'] = request.POST['customer_name']
        #     specs = specs.filter(req_id__customer__name__icontains=form_data['customer_name'])
        # specs = ReqSpec.objects.filter(req_id__customer__name__icontains=customer_name).filter(kw=kw).filter(rpm=rpm)
        # print(f"items: {form_data['kw']} + {form_data['rpm']} + {form_data['customer_name']}")
        search_form = search.SpecSearchForm(form_data)
        # search_form = search.SpecSearchForm()
    # elif request.method == 'GET':
    else:
        specs = ReqSpec.objects.filter(is_active=True)
        search_form = search.SpecSearchForm()

    today = jdatetime.date.today()

    response = []

    date_format = "%m/%d/%Y"
    total_kw = 0
    total_qty = 0
    payment_sum = 0

    if not request.user.is_superuser:
        specs = specs.filter(req_id__owner=request.user) | specs.filter(req_id__colleagues=request.user)

    payments_all_total = 0
    for p in pmnt_total:
        payments_all_total += p.amount

    unverified_profs_total = 0
    verified_profs_total = 0

    for spec in specs:
        diff = today - spec.req_id.date_fa
        # url = url(request_read, request_pk=spec.req_id.pk)
        url = reverse('request_details', kwargs={'request_pk': spec.req_id.pk})
        customer_url = reverse('customer_read', kwargs={'customer_pk': spec.req_id.customer.pk})

        owner_colleagues = []
        total_kw += spec.qty * spec.kw
        total_qty += spec.qty
        diff = today - spec.req_id.date_fa
        proformas = spec.req_id.xpref_set.filter(is_active=True)
        unverified_profs = []
        verified_profs = []
        payments = []
        for prof in proformas:
            prof_amount = 0
            for item in prof.prefspec_set.filter(is_active=True):
                prof_amount += item.qty * item.price
            prof_amount = 1.09 * prof_amount
            temp_prof = {
                'number': prof.number,
                'prof_amount': prof_amount,
                'prof_url': reverse('pref_details', kwargs={'ypref_pk': prof.pk}),
            }
            if prof.verified:
                verified_profs_total += prof_amount
                verified_profs.append(temp_prof)
            else:

                unverified_profs_total += prof_amount
                unverified_profs.append(temp_prof)
            pmnts = prof.payment_set.filter(is_active=True)
            for pay in pmnts:
                payment_sum += pay.amount
                amount = int(pay.amount)
                payments.append({
                    'number': pay.number,
                    'amount': amount,
                    'pmnt_url': reverse('payment_details', kwargs={'ypayment_pk': pay.pk}),
                })
        owner_colleagues.append({
            'last_name': spec.req_id.owner.last_name,
        })
        for colleage in spec.req_id.colleagues.all():
            owner_colleagues.append({
                'last_name': colleage.last_name,
            })

        response.append(
            {
                # 'spec': spec,
                # 'date_fa': str(spec.req_id.date_fa),
                'delay': diff.days,
                'customer_name': spec.req_id.customer.name,
                'customer_url': customer_url,
                'qty': spec.qty,
                'rpm': spec.rpm,
                'kw': spec.kw,
                'voltage': spec.voltage,
                'reqNo': spec.req_id.number,
                'price': spec.price,
                'tech': spec.tech,
                'permission': spec.permission,
                'sent': spec.sent,
                'url': url,
                'owner_colleagues': owner_colleagues,
                # 'profs': profs,
                'unverified_profs': unverified_profs,
                'verified_profs': verified_profs,
                'payments': payments,
                'date_fa': spec.req_id.date_fa.strftime("%Y-%m-%d"),
                # 'date_fa': jdatetime.date.fromgregorian(date=spec.req_id.pub_date),
                # 'date_fa': json_tricks.dumps(spec.req_id.date_fa),
                # 'date_fa': serialize('json', spec.req_id.date_fa, cls=DateTimeEncoder),
                # 'colleagues': req.colleagues.all(),
            })
    context = {
        # 'reqspecs': specs,
        'response': response,
        # 'search_form': search_form,
        'total_kw': total_kw,
        'total_qty': total_qty,
        'verified_profs_total': verified_profs_total,
        'unverified_profs_total': unverified_profs_total,
        'unv_perc': 100 * verified_profs_total / (verified_profs_total + unverified_profs_total),
        'payment_sum': payment_sum,
        'payment_percentage': 100 * (payment_sum / payments_all_total),
        'rpm': form_data['rpm'],
    }
    # return render(request, 'requests/admin_jemco/yreqspec/index.html', context)
    return JsonResponse(context, safe=False)


def fsearch3(request):

    can_index = funcs.has_perm_or_is_owner(request.user, 'request.index_requests')
    if not can_index:
        messages.error(request, 'عدم دسترسی کافی!')
        return redirect('errorpage')
    context = {
        'search_form': search.SpecSearchForm()
    }
    return render(request, 'requests/admin_jemco/yreqspec/index-vue.html', context)


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
    # todo: should be removed.
    # requests =request_form Requests.objects.all()
    can_index = funcs.has_perm_or_is_owner(request.user, 'request.index_requests')
    if not can_index:
        messages.error(request, 'عدم دسترسی کافی!')
        return redirect('errorpage')
    # requests = Requests.objects.filter(owner=request.user).order_by('date_fa').reverse()
    # requests = Requests.objects.all().order_by('date_fa').reverse()
    today = jdatetime.date.today()

    requests = Requests.objects.filter(is_active=True).order_by('date_fa').reverse()
    if not request.user.is_superuser:
        requests = requests.filter(owner=request.user)
    response = {}

    date_format = "%m/%d/%Y"
    for req in requests:
        diff = today - req.date_fa
        time_entered = jdatetime.date.fromgregorian(date=req.pub_date, locale='fa_IR')
        delay_entered = time_entered - req.date_fa
        response[req.pk] = {
            'req': req,
            'pub_date': time_entered,
            'delay_entered': delay_entered,
            'delay': diff.days,
            'colleagues': req.colleagues.all(),
        }
    if request.user.is_superuser:
        requests = Requests.objects.filter(is_active=True).order_by('date_fa').reverse()

    page = request.GET.get('page', 1)
    req_list = requests
    paginator = Paginator(req_list, 30)
    try:
        req_page = paginator.page(page)
    except PageNotAnInteger:
        req_page = paginator.page(1)
    except EmptyPage:
        req_page = paginator.page(paginator.num_pages)
    context = {
        'req_page': req_page,
        'all_requests': requests,
        'response': response
    }
    return render(request, 'requests/admin_jemco/yrequest/index.html', context)


@login_required
def request_index_paginate(request):
    can_index = funcs.has_perm_or_is_owner(request.user, 'request.index_requests')
    if not can_index:
        messages.error(request, 'عدم دسترسی کافی!')
        return redirect('errorpage')
    today = jdatetime.date.today()

    requests = Requests.objects.filter(is_active=True).order_by('date_fa').reverse()
    if not request.user.is_superuser:
        requests = requests.filter(Q(owner=request.user) | Q(colleagues=request.user))

    response = {}
    if request.user.is_superuser:
        requests = Requests.objects.filter(is_active=True).order_by('date_fa').reverse()

    page = request.GET.get('page', 1)
    req_list = requests
    paginator = Paginator(req_list, 30)
    try:
        req_page = paginator.page(page)
    except PageNotAnInteger:
        req_page = paginator.page(1)
    except EmptyPage:
        req_page = paginator.page(paginator.num_pages)

    for req in req_page.object_list:
        diff = today - req.date_fa
        time_entered = jdatetime.date.fromgregorian(date=req.pub_date, locale='fa_IR')
        delay_entered = time_entered - req.date_fa
        response[req.pk] = {
            'req': req,
            'pub_date': time_entered,
            'delay_entered': delay_entered,
            'delay': diff.days,
            'colleagues': req.colleagues.all(),
        }
    context = {
        'req_page': req_page,
        'all_requests': requests,
        'response': response
    }
    return render(request, 'requests/admin_jemco/yrequest/index2.html', context)


@login_required
def req_to_follow(request, request_pk):
    can_index = funcs.has_perm_or_is_owner(request.user, 'request.index_requests')
    if not can_index:
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
def request_index_vue(request):
    # requests =request_form Requests.objects.all()
    can_index = funcs.has_perm_or_is_owner(request.user, 'request.index_requests')
    if not can_index:
        messages.error(request, 'عدم دسترسی کافی!')
        return redirect('errorpage')
    # requests = Requests.objects.filter(owner=request.user).order_by('date_fa').reverse()
    # requests = Requests.objects.all().order_by('date_fa').reverse()
    today = jdatetime.date.today()

    requests = Requests.objects.filter(is_active=True).order_by('date_fa').reverse()
    if not request.user.is_superuser:
        requests = requests.filter(owner=request.user)
    response = {}

    date_format = "%m/%d/%Y"
    for req in requests:
        diff = today - req.date_fa
        response[req.pk] = {
            'req': req,
            'delay': diff.days,
            'colleagues': req.colleagues.all(),
        }
    if request.user.is_superuser:
        requests = Requests.objects.filter(is_active=True).order_by('date_fa').reverse()
    context = {
        'all_requests': requests,
        'response': response,
        'showHide': True,
        'message': 'درخواست ها',
    }
    return render(request, 'requests/admin_jemco/yrequest/vue/index.html', context)


@login_required
def request_index_vue_deleted(request):
    # requests =request_form Requests.objects.all()
    can_index = funcs.has_perm_or_is_owner(request.user, 'request.index_deleted_requests')
    if not can_index:
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
        return redirect('request_index_paginate')
    req = Requests.objects.filter(is_active=True).get(number=req_no)
    return redirect('request_details', request_pk=req.pk)


@login_required
def request_read(request, request_pk):
    if not Requests.objects.filter(is_active=True).filter(pk=request_pk) and not request.user.is_superuser:
        messages.error(request, 'صفحه مورد نظر یافت نشد')
        return redirect('errorpage')

    req = Requests.objects.get(pk=request_pk)

    colleagues = req.colleagues.all()
    colleague = False
    if request.user in colleagues:
        colleague = True

    can_read = funcs.has_perm_or_is_owner(request.user, 'request.read_requests', req, colleague)
    if not can_read:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

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
def read_vue(request, request_pk):
    if not Requests.objects.filter(pk=request_pk) and not request.user.is_superuser:
        messages.error(request, 'صفحه مورد نظر یافت نشد')
        return redirect('errorpage')

    req = Requests.objects.get(pk=request_pk)
    colleagues = req.colleagues.all()
    colleague = False
    if request.user in colleagues:
        colleague = True

    can_read = funcs.has_perm_or_is_owner(request.user, 'request.read_requests', req, colleague)
    if not can_read:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

    if not request.user.is_superuser:
        req.edited_by_customer = False
        req.save()

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
    return render(request, 'requests/admin_jemco/yrequest/vue/details.html', context)
    # return JsonResponse(context, safe=False)


@login_required
def request_delete(request, request_pk):
    if not Requests.objects.filter(is_active=True).filter(pk=request_pk):
        messages.error(request, 'Nothing found')
        return redirect('errorpage')
    req = Requests.objects.filter(is_active=True).get(pk=request_pk)
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
        # req.delete()
        req.is_active = False
        req.temp_number = req.number
        rand_num = random.randint(100000, 200000)
        while Requests.objects.filter(number=rand_num):
            rand_num = random.randint(100000, 200000)
        req.number = rand_num
        req.save()
        req.reqspec_set.update(is_active=False)

    return redirect('request_index')


@login_required
def request_edit(request, request_pk):
    if not Requests.objects.filter(pk=request_pk):
        messages.error(request, 'Nothing found')
        return redirect('errorpage')
    return HttpResponse('request Edit' + str(request_pk))


@login_required
def request_edit_form(request, request_pk):
    # 1- check for permissions
    # 2 - find request and related images
    # 3 - make request image form
    # 4 - prepare image name to use in template
    # 5 - get the list of files from request
    # 6 - if form is valid the save request and its related images
    # 7 - render the template file
    if not Requests.objects.filter(is_active=True).filter(pk=request_pk):
        messages.error(request, 'Nothin found')
        return redirect('errorpage')
    if 'customer' in request.COOKIES:
        c_cookie = request.COOKIES.get('customer')
        customer = Customer.objects.get(pk=c_cookie)

    req = Requests.objects.filter(is_active=True).get(pk=request_pk)
    colleagues = req.colleagues.all()
    colleague = False
    if request.user in colleagues:
        colleague = True
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.edit_requests', req, colleague=colleague)
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
        req_item.customer = customer
        req_item.save()
        form.save_m2m()
        for f in files:
            file_instance = models.RequestFiles(image=f, req=req_item)
            file_instance.save()
        # return redirect('request_index')
        return redirect('request_index_paginate')

    context = {
        'customer': req.customer.name,
        'form': form,
        'req_img': img_form,
        'req_images': req_images,
        'img_names': img_names,
        'add_new': False,
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
def req_report(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.index_requests')
    if not can_add:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')
    filters = {}
    req_list = Requests.objects.filter(is_active=True).order_by('date_fa').reverse()
    if not request.user.is_superuser:
        # req_list = req_list.filter(owner=request.user)
        req_list = req_list.filter(Q(owner=request.user) | Q(colleagues=request.user))
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
                'total_received': f"{a.total_proforma_received()['received']}",
                'total_received_percentage': a.total_proforma_received()['received_percent'],
                'perm_receivable': a.total_proforma_received()['remaining'],
                'perm_receivable_percentage': a.total_proforma_received()['remaining_percent'],
                'perm_number': a.number,
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
