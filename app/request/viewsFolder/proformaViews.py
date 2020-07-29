import datetime
import json
import os
from base64 import encode

from django.core.cache import cache
import random

import jdatetime
import xlwt
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template, render_to_string

from django_jalali.db import models as jmodels
from xhtml2pdf import pisa

import request.templatetags.functions as funcs

from django.contrib.auth import get_user_model
from django.templatetags.static import static
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import F, Field, FloatField, ExpressionWrapper, DurationField, Value, DateField, DateTimeField, Q, \
    Sum

import pdfkit
import jdatetime
import xlwt
from django.urls import reverse

from factor import settings
from customer.models import Customer
from request import models
from request.forms.forms import CommentForm, ProfFollowUpForm
from request.forms.search import ProformaSearchForm, PermSearchForm, PrefSpecSearchForm
import request.templatetags.functions as funcs
from request.models import Requests, Xpref, ReqSpec, PrefSpec, ProformaFollowUP, Perm, ProjectType, ProfChangeRequest
from pricedb.models import MotorDB

from request.forms import proforma_forms, forms
from django.contrib.auth.decorators import login_required

from django.db.models import F, Field, FloatField, ExpressionWrapper, DurationField, Value, DateField, DateTimeField, Q, \
    Sum

from request.templatetags import functions, request_extras
from pricedb.models import MotorDB

User = get_user_model()
from django.views.generic import View
from ..utils import render_to_pdf, link_callback

from django.template.loader import get_template
from django.template import Context
import pdfkit


@login_required
def pref_index(request):
    can_index = funcs.has_perm_or_is_owner(request.user, 'request.index_proforma')
    if not can_index:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

    prof_list = Xpref.objects.filter(is_active=True).order_by('date_fa', 'pk').reverse()

    if not request.user.is_superuser:
        prof_list = prof_list.filter(
            Q(owner=request.user) | Q(req_id__colleagues=request.user) | Q(req_id__owner=request.user)
        ).distinct()

    if not request.method == 'POST':
        if 'proforma-search-post' in request.session:
            request.POST = request.session['proforma-search-post']
            request.method = 'POST'

    form = ProformaSearchForm()
    item_per_page = 50
    if request.method == 'POST':
        item_per_page = request.POST['item_per_page']
        form = ProformaSearchForm(request.POST or None)
        request.session['proforma-search-post'] = request.POST
        if request.POST['customer_name']:
            if Customer.objects.filter(name=request.POST['customer_name']):
                customer = Customer.objects.get(name=request.POST['customer_name'])
                prof_list = prof_list.filter(req_id__customer=customer)
            else:
                prof_list = prof_list.filter(req_id__customer__name__contains=request.POST['customer_name'])
        if request.POST['owner'] and request.POST['owner'] != '0':

            owner = User.objects.get(pk=request.POST['owner'])
            prof_list = prof_list.distinct().filter(Q(owner=owner) | Q(req_id__colleagues=owner))
        if request.POST['date_min']:
            prof_list = prof_list.filter(date_fa__gte=request.POST['date_min'])
        if request.POST['date_max']:
            prof_list = prof_list.filter(date_fa__lte=request.POST['date_max'])
        if request.POST['status'] and request.POST['status'] != '0':
            status = request.POST['status']
            today = jdatetime.date.today()

            if status == 'valid':
                # prof_list = prof_list.filter(Q(exp_date_fa__gte=today) | Q(perm=True))
                prof_list = prof_list.filter(exp_date_fa__gte=today)
            elif status == 'perm':
                prof_list = prof_list.filter(perm=True)
            elif status == 'expired':
                prof_list = prof_list.filter(exp_date_fa__lt=today, perm=False)
            elif status == 'to_follow':
                prof_list = prof_list.filter(to_follow=True)

        if request.POST['sort_by']:
            prof_list = prof_list.order_by(f"{request.POST['sort_by']}")
        if request.POST['dsc_asc'] == '2':
            prof_list = prof_list.reverse()
    if request.method == 'GET':
        form = ProformaSearchForm()

    page = request.GET.get('page')
    paginator = Paginator(prof_list, item_per_page)
    try:
        pref_page = paginator.page(page)
    except PageNotAnInteger:
        pref_page = paginator.page(1)
    except EmptyPage:
        pref_page = paginator.page(paginator.num_pages)

    context = {
        'prefs': pref_page,
    }
    cache.set('profs_in_sessions', context, 300)
    context.update({
        'form': form,
        'title': 'پیش فاکتور',
        'showDelete': True,
    })
    return render(request, 'requests/admin_jemco/ypref/index.html', context)


@login_required
def verify(request):
    profs_active = Xpref.objects.filter(is_active=True)
    profs = profs_active.filter(
        verified=False,
        # profchangerequest__change_needed=False
    ).exclude(profchangerequest__change_needed=True)
    profs_need_change = profs_active.filter(
        profchangerequest__change_needed=True
    )
    profs_to_verified = profs_active.filter(verified=True, signed=False)
    profs_signed = profs_active.filter(verified=True, signed=True)
    if profs_signed.count() >= 50:
        profs_signed = profs_signed[profs_signed.count() - 50:]
    context = {
        'proformas': profs,
        'profs_need_change': profs_need_change,
        'profs_to_verified': profs_to_verified,
        'profs_signed': profs_signed,
    }
    return render(request, 'requests/admin_jemco/ypref/to_verify.html', context)


@login_required
def change_done(request, ypref_pk, change_pk):
    pchange = ProfChangeRequest.objects.get(pk=change_pk)
    pchange.change_needed = False
    pchange.save()
    return redirect('pref_details', ypref_pk=ypref_pk)


@login_required
def pref_index_cc(request):
    if 'proforma-search-post' in request.session:
        request.session.pop('proforma-search-post')
    return redirect('pref_index')


@login_required
def perm_clear_session(request):
    if 'perm-search' in request.session:
        request.session.pop('perm-search')
    return redirect('perm_index')


@login_required
def prof_export(request):

    try:
        context = cache.get('profs_in_sessions')
        profs = context['prefs']
    except:
        profs = Xpref.objects.filter(is_active=True)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="proformas.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('پیش فاکتور')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = (
        'ردیف',
        'پیش فاکتور',
        'مجوز',
        'شماره درخواست',
        'مشتری',
        'کارشناس',
        'تاریخ',
        'انقضا',
    )

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    # if request.user.is_superuser:
    #     pass
    for prof in profs:
        row_num += 1

        exportables = []
        exportables.append(row_num)
        exportables.append(prof.number)
        exportables.append(prof.perm_number)
        exportables.append(prof.req_id.number)
        exportables.append(prof.req_id.customer.name)
        exportables.append(prof.req_id.owner.last_name)
        exportables.append(str(prof.date_fa))
        exportables.append(str(prof.exp_date_fa))

        for col_num in range(len(exportables)):
            ws.write(row_num, col_num, exportables[col_num], font_style)

    ws.cols_right_to_left = True
    wb.save(response)
    return response


@login_required
def prefspec_index(request):
    can_index = funcs.has_perm_or_is_owner(request.user, 'request.index_proforma')
    if not can_index:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

    spec_list = PrefSpec.objects.filter(xpref_id__is_active=True, xpref_id__perm=True, price__gt=0) \
        .annotate(qty_remaining=F('qty') - F('qty_sent'))

    if not request.method == 'POST':
        if 'prefspec-search-post' in request.session:
            request.POST = request.session['prefspec-search-post']
            request.method = 'POST'

    form = PrefSpecSearchForm()
    item_per_page = 50

    if request.method == 'POST':
        item_per_page = request.POST['item_per_page']
        form = PrefSpecSearchForm(request.POST or None)
        request.session['prefspec-search-post'] = request.POST
        if request.POST['customer_name']:
            if Customer.objects.filter(name=request.POST['customer_name']):
                customer = Customer.objects.get(name=request.POST['customer_name'])
                spec_list = spec_list.filter(xpref_id__req_id__customer=customer)
            else:
                spec_list = spec_list.filter(xpref_id__req_id__customer__name__contains=request.POST['customer_name'])
        if request.POST['owner'] and request.POST['owner'] != '0':

            owner = User.objects.get(pk=request.POST['owner'])
            spec_list = spec_list.distinct().filter(Q(xpref_id__owner=owner) | Q(xpref_id__req_id__colleagues=owner))
        if request.POST['date_min']:
            spec_list = spec_list.filter(xpref_id__date_fa__gte=request.POST['date_min'])
        if request.POST['date_max']:
            spec_list = spec_list.filter(xpref_id__date_fa__lte=request.POST['date_max'])
        if request.POST['kw_max']:
            spec_list = spec_list.filter(kw__lte=request.POST['kw_max'])
        if request.POST['kw_min']:
            spec_list = spec_list.filter(kw__gte=request.POST['kw_min'])
        if request.POST['rpm']:
            spec_list = spec_list.filter(rpm=request.POST['rpm'])
        if request.POST['project_type'] and request.POST['project_type'] != '0':
            project_type = ProjectType.objects.get(title=request.POST['project_type'])
            spec_list = spec_list.filter(reqspec_eq__type=project_type)
        if request.POST['status'] and request.POST['status'] != '0':
            status = request.POST['status']

            if status == 'not_complete':
                spec_list = spec_list.filter(qty_remaining__gt=0)
            elif status == 'complete':
                spec_list = spec_list.filter(qty_remaining=0)

        if request.POST['sort_by']:
            spec_list = spec_list.order_by(f"{request.POST['sort_by']}")
        if request.POST['dsc_asc'] == '2':
            spec_list = spec_list.reverse()

    page = request.GET.get('page')
    paginator = Paginator(spec_list, item_per_page)
    try:
        prefspec_page = paginator.page(page)
    except PageNotAnInteger:
        prefspec_page = paginator.page(1)
    except EmptyPage:
        prefspec_page = paginator.page(paginator.num_pages)
    context = {
        'pref_specs': prefspec_page,
        'form': form,
    }
    return render(request, 'requests/admin_jemco/ypref/prefspec_index.html', context)


@login_required
def prefspec_clear_cache(request):
    if 'prefspec-search-post' in request.session:
        request.session.pop('prefspec-search-post')
    return redirect('prefspec_index')


@login_required
def perm_index(request):
    can_index = funcs.has_perm_or_is_owner(request.user, 'request.index_proforma')
    if not can_index:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

    prof_list = Xpref.objects.filter(is_active=True, req_id__is_active=True, perm=True) \
        .annotate(total_qty=Sum('prefspec__qty', filter=Q(prefspec__price__gt=0))) \
        .annotate(total_qty_sent=Sum('prefspec__qty_sent', filter=Q(prefspec__price__gt=0))) \
        .annotate(qty_remaining=F('total_qty') - F('total_qty_sent')).order_by('due_date').prefetch_related('owner')

    if not request.user.is_superuser:
        prof_list = prof_list.filter(owner=request.user)
        # prof_list = prof_list.filter(req_id__owner=request.user)

    if not request.method == 'POST':

        if 'perm-search' in request.session:
            request.POST = request.session['perm-search']
            request.method = 'POST'

    form = PermSearchForm()

    if request.method == 'POST':
        form = PermSearchForm(request.POST or None)
        request.session['perm-search'] = request.POST
        if request.POST['customer_name']:
            if Customer.objects.filter(name=request.POST['customer_name']):
                customer = Customer.objects.get(name=request.POST['customer_name'])
                prof_list = prof_list.filter(req_id__customer=customer)
            else:
                prof_list = prof_list.filter(req_id__customer__name__contains=request.POST['customer_name'])
        if request.POST['owner'] and request.POST['owner'] != '0':

            owner = User.objects.get(pk=request.POST['owner'])
            prof_list = prof_list.distinct().filter(
                Q(owner=owner) | Q(req_id__colleagues=owner) | Q(req_id__owner=owner))
        if request.POST['date_min']:
            prof_list = prof_list.filter(perm_date__gte=request.POST['date_min'])
        if request.POST['date_max']:
            prof_list = prof_list.filter(perm_date__lte=request.POST['date_max'])
        if request.POST['status'] and request.POST['status'] != '0':
            status = request.POST['status']

            if status == 'not_complete':
                prof_list = prof_list.filter(qty_remaining__gt=0)
            elif status == 'complete':
                prof_list = prof_list.filter(qty_remaining=0)

        if request.POST['sort_by']:
            sort_by = request.POST['sort_by']
            prof_list = prof_list.order_by(f"{request.POST['sort_by']}")
            if sort_by == 'due_date':
                prof_list = prof_list.reverse()
        if request.POST['dsc_asc'] == '2':
            prof_list = prof_list.reverse()

    res = []
    for p in prof_list:
        res.append(p)
    prof_list_nums = [prof.number for prof in prof_list]
    qty = {
        'total': PrefSpec.objects.filter(xpref_id__number__in=prof_list_nums, price__gt=0).aggregate(total=Sum('qty'))['total'],
        'qty_sent': PrefSpec.objects.filter(xpref_id__number__in=prof_list_nums, price__gt=0).aggregate(qty_sent=Sum('qty_sent'))['qty_sent'],
        # 'total': prof_list.aggregate(total=Sum('qty'))['total'],
        # 'sent': prof_list.aggregate(sent=Sum('sent'))['sent'],
        # 'remain': prof_list.aggregate(remain=F('total')-F('sent'))['remain'],
    }
    qty['remain'] = qty['total'] - qty['qty_sent']
    context = {
        'permission': res,
        'form': form,
        'qty': qty,
        'title': 'مجوز ساخت',
        'showDelete': True,
    }

    return render(request, 'requests/admin_jemco/ypref/index_perms.html', context)


@login_required
def perm_index2(request):
    can_index = funcs.has_perm_or_is_owner(request.user, 'request.index_proforma')
    if not can_index:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')
    # perm_numbers = Perm.objects.values('number').distinct().prefetch_related('permspec_perm__qty', 'inv_out_perm__inventoryoutspec__qty')
    perm_numbers = Perm.objects.all().order_by('date')
    context = {
        'perm_numbers': perm_numbers,
        'title': 'مجوز ساخت',
        'showDelete': True,
    }

    return render(request, 'requests/admin_jemco/ypref/index_perms2.html', context)


@login_required
def user_export(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Username', 'First name', 'Last name', 'Email address', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


@login_required
def request_export(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="requests.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['number', 'customer', 'summary', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Requests.objects.all().values_list('number', 'customer__name', 'summary')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


@login_required
def perms_export(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="perms.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('مجوز')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = (
        'ردیف',
        'شماره مجوز',
        'شماره پیش فاکتور',
        'شماره درخواست',
        'تاریخ مجوز',
        'زمان تحویل',
        'مشتری',
        'زمان باقیمانده(روز)',
        'کل مبلغ',
        'تسویه نشده',
        'درصد تسویه نشده',
        'جزئیات',
        'کارشناس'
    )

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    profs = Xpref.objects.filter(perm=True).order_by('due_date')
    profs = Xpref.objects.filter(is_active=True, owner=request.user, perm=True) \
        .annotate(total_qty=Sum('prefspec__qty', filter=Q(prefspec__price__gt=0))) \
        .annotate(total_qty_sent=Sum('prefspec__qty_sent', filter=Q(prefspec__price__gt=0))) \
        .annotate(qty_remaining=F('total_qty') - F('total_qty_sent')) \
        .filter(qty_remaining__gt=0) \
        .order_by('due_date', 'pk')

    # new = prefs.exclude(prefspec__price=False).distinct().annotate(total=Count('prefspec'))
    if request.user.is_superuser:
        profs = Xpref.objects.filter(is_active=True, perm=True) \
            .annotate(total_qty=Sum('prefspec__qty', filter=Q(prefspec__price__gt=0))) \
            .annotate(total_qty_sent=Sum('prefspec__qty_sent', filter=Q(prefspec__price__gt=0))) \
            .annotate(qty_remaining=F('total_qty') - F('total_qty_sent')) \
            .filter(qty_remaining__gt=0) \
            .order_by('due_date', 'pk')

    profs_values = profs.values()
    final = {}
    for perm in profs:
        row_num += 1
        a = ()
        days = request_extras.perm_days(perm)
        if days < 0:
            cell_style = 'pattern: pattern solid, fore_colour blue;'
        total_receiveable = perm.total_proforma_price_vat()['price_vat']
        perm_receivable = perm.total_proforma_received()['remaining']
        perm_receivable_percent = perm.total_proforma_received()['remaining_percent']
        final['days'] = days

        exportables = []
        exportables.append(row_num)
        exportables.append(perm.perm_number)
        exportables.append(perm.number)
        exportables.append(perm.req_id.number)
        exportables.append(str(perm.perm_date))
        exportables.append(str(perm.due_date))
        exportables.append(perm.req_id.customer.name)
        exportables.append(days)
        exportables.append(total_receiveable)
        exportables.append(perm_receivable)
        exportables.append(perm_receivable_percent)
        exportables.append(perm.req_id.owner.last_name)

        for col_num in range(len(exportables)):
            ws.write(row_num, col_num, exportables[col_num], font_style)

    ws.cols_right_to_left = True
    wb.save(response)
    return response


@login_required
def perm_specs(request):
    print(request)


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
    prof_no = False
    prof_td_no = False
    # term = request.POST['text']
    if not request.POST['pref_no'] and not request.POST['pref_td_no']:
        return redirect('pref_index')
    elif request.POST['pref_no']:
        prof_no = request.POST['pref_no']
        pref = Xpref.objects.filter(number=prof_no)
    elif request.POST['pref_td_no']:
        prof_td_no = request.POST['pref_td_no']
        pref = Xpref.objects.filter(number_td=prof_td_no)
    if pref.exists():
        pref = pref.last()
        return redirect('pref_details', ypref_pk=pref.pk)
    else:
        messages.error(request, 'پیشفاکتور یافت نشد.')
        return redirect('errorpage')

    # if not Xpref.objects.filter(number=prof_no):
    #     messages.error(request, 'پیش فاکتور مورد نظر یافت نشد')
    #     return redirect('pref_index')
    # try:
    #     pref = Xpref.objects.filter(is_active=True).get(number=prof_no)
    #     return redirect('pref_details', ypref_pk=pref.pk)
    # except:
    #     messages.error(request, 'پیشفاکتور یافت نشد.')
    #     return redirect('errorpage')


# @login_required
def find_price_by_id(request):
    data = json.loads(request.body.decode('utf-8'))
    pk = data['rspec']
    spec = PrefSpec.objects.get(pk=pk)

    # Exact specs
    exact = True
    # rspecs = PrefSpec.objects.filter(
    #     code=spec.code,
    #     price__gt=0,
    # )

    # if not rspecs.exists():

    # exact = False
    rspecs = PrefSpec.objects.filter(
        kw=spec.kw,
        rpm=spec.rpm,
        voltage=spec.voltage,
        im=spec.im,
        xpref_id__is_active=True,
        price__gt=0,
    )
    rspecs = rspecs.order_by('xpref_id__date_fa').reverse()

    prices = [{
        'price': rspec.price,
        'url': request.build_absolute_uri(reverse('pref_details', kwargs={'ypref_pk': rspec.xpref_id.pk})),
        'date': str(rspec.xpref_id.date_fa),
        'customer': rspec.xpref_id.req_id.customer.name[:45],
    } for rspec in rspecs]

    # Similar specs

    context = {
        'rs': pk,
        'prices': prices,
        'exact': exact,
    }
    return JsonResponse(context, safe=False)


def find_no_price_by_id(request):
    data = json.loads(request.body.decode('utf-8'))
    pk = data['rspec']
    spec = PrefSpec.objects.get(pk=pk)

    # Exact specs
    exact = True
    # rspecs = PrefSpec.objects.filter(
    #     code=spec.code,
    #     price__gt=0,
    # )

    # if not rspecs.exists():

    # exact = False
    rspecs = ReqSpec.objects.filter(
        kw=spec.kw,
        rpm=spec.rpm,
        voltage=spec.voltage,
        im=spec.im,
        is_active=True,
        req_id__xpref__isnull=True,
    )
    rspecs = rspecs.order_by('req_id__date_fa').reverse()

    requests = [{
        'url': request.build_absolute_uri(reverse('request_details', kwargs={'request_pk': rspec.req_id.pk})),
        'date': str(rspec.req_id.date_fa),
        'number': rspec.req_id.number,
        'customer': rspec.req_id.customer.name[:45],
    } for rspec in rspecs]

    # Similar specs
    print(len(requests))
    context = {
        'rs': pk,
        'requests': requests,
        'exact': exact,
    }
    return JsonResponse(context, safe=False)


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
    changes_needed = pref.profchangerequest_set.all()
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

    if request.method == 'POST':
        # comment = pref.comments.create(author=request.user, body=request.POST['body'])
        # pref.comments.all().update(is_read=True)
        # comment.is_read = False
        # comment.save()
        followup_form = forms.ProfFollowUpForm(request.POST)
        if followup_form.is_valid():
            followup = followup_form.save(commit=False)
            followup.author = request.user
            followup.xpref = pref
            followup.save()

    context = {
        'pref': pref,
        'prefspecs': prefspecs,
        'changes_needed': changes_needed,
        'nested': nestes_dict,
        'vat': proforma_total * 0.09,
        'proforma_total': proforma_total * 1.09,
        'kw_total': kw_total,
        'prof_images': prof_images,
        'comment_form': CommentForm(),
        # 'followup_form': ProfFollowUpForm(initial={'xpref': pref, 'author': request.user}),
        'followup_form': ProfFollowUpForm(),
        'followUps': pref.proformafollowup_set.all(),
    }
    return render(request, 'requests/admin_jemco/ypref/details.html', context)


@login_required
def proforma_copy(request, ypref_pk):

    if not Xpref.objects.filter(pk=ypref_pk):
        messages.error(request, 'Nothin found')
        return redirect('errorpage')
    pref = Xpref.objects.get(pk=ypref_pk)
    can_read = funcs.has_perm_or_is_owner(request.user, 'request.add_xpref', pref)

    if not can_read:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

    proforma = Xpref.objects.get(pk=ypref_pk)
    pref_specs = proforma.prefspec_set.all()
    proforma.pk = None

    last = Xpref.objects.order_by('number').last()
    proforma.number = last.number + 1
    proforma.save()

    for pspec in pref_specs:
        pspec.pk = None
        pspec.xpref_id = proforma
        pspec.save()

    return redirect('pref_edit_form', ypref_pk=proforma.pk)


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
            percentage = (prefspec.price / (price.prime_cost))
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
            total_percentage = proforma_total / sales_total
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
def pref_verify_to_send(request, ypref_pk):
    proforma = Xpref.objects.get(pk=ypref_pk)
    proforma.verified = True
    proforma.save()
    return redirect('verify')


@login_required
def pref_send_verified(request, ypref_pk):
    proforma = Xpref.objects.get(pk=ypref_pk)
    proforma.signed = True
    proforma.save()

    return redirect('verify')


@login_required
def proforma_changed_needed(request, ypref_pk):
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_profchangerequest')
    if not can_add:
        messages.error(request, 'عدم دستری کافی!')
        return redirect('errorpage')
    proforma = Xpref.objects.get(pk=ypref_pk)
    from request.models import ProfChangeRequest

    if request.method == 'POST':
        form = forms.ProfChangeRequestForm(request.POST or None)

        if form.is_valid():
            req_item = form.save(commit=False)
            req_item.owner = request.user
            req_item.proforma = proforma
            req_item.change_needed = True
            req_item.save()
            proforma.verified = False
            proforma.signed = False
            proforma.save()
            return redirect('verify')
    else:
        form = forms.ProfChangeRequestForm()

    context = {
        'form': form,
        'proforma': proforma,
    }
    return render(request, 'requests/admin_jemco/ypref/prof_need_change.html', context)


@login_required
def cancel_pref_send_verified(request, ypref_pk):
    proforma = Xpref.objects.get(pk=ypref_pk)
    proforma.verified = False
    proforma.signed = False
    proforma.save()
    return redirect('verify')


@login_required
def cancel_pref_verify_to_send(request, ypref_pk):
    proforma = Xpref.objects.get(pk=ypref_pk)
    proforma.verified = True
    proforma.signed = False
    proforma.save()

    return redirect('verify')


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
        pref.is_active = False
        pref.temp_number = pref.number
        rand_num = random.randint(100000, 200000)
        while Xpref.objects.filter(number=rand_num).exists():
            rand_num = random.randint(100000, 200000)
        pref.number = rand_num
        pref.save()
        pref.prefspec_set.update(is_active=False)
    return redirect('pref_index')


@login_required
def delete_proforma_no_prefspec(request, ypref_pk):
    try:
        prof = Xpref.objects.get(pk=ypref_pk)
        prefspecs = prof.prefspec_set.filter(price__gt=0)
        if prefspecs.count() == 0:
            prof.delete()
    except:
        print('h03')

        return redirect('pref_index')
    return redirect('pref_index')


@login_required
def pro_form_cookie(request, req_id):
    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_xpref')
    if not can_add:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')
    try:
        req = Requests.objects.get(pk=req_id)
        if req.reqspec_set.count() == 0:
            messages.error(request, 'درخواست باید شامل حداقل یک ردیف باشد.')
            return redirect('request_details', request_pk=req_id)
    except:
        messages.error(request, 'درخواست مورد نظر یافت نشد.')
        return redirect('errorpage')

    # response = HttpResponse()
    # response.set_cookie('request_pk', req_id)
    # request.set_cookie('request_pk', req_id)
    # request.COOKIES['request_pk'] = req_id
    request.session['request_pk'] = req_id
    return redirect(pro_form)


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
            last = Xpref.objects.order_by('number').last()

            proforma.number = last.number + 1
            proforma.save()

            # Save files
            for f in files:
                file_instance = models.ProfFiles(image=f, prof=proforma)
                file_instance.save()

            # make a list of specs for this proforma
            req = proforma.req_id
            specs_set = req.reqspec_set.filter(finished=False, is_active=True)
            # print(f'request is: {req}')
            # print(f'specs: {specs_set}')

            for spec in specs_set:
                form = forms.ProfSpecForm()
                spec_item = form.save(commit=False)
                spec_item.type = spec.type
                spec_item.code = spec.code
                spec_item.price = 0
                spec_item.kw = spec.kw
                spec_item.qty = spec.qty
                # spec_item.rpm = spec.rpm
                try:
                    spec_item.rpm = int(spec.rpm_new.rpm)
                except:
                    proforma.prefspec_set.all().delete()
                    proforma.delete()
                    messages.error(request, 'اطلاعات سرعت صحیح نیست.')
                    return redirect('reqspec_edit_form', req_pk=req.pk, yreqSpec_pk=spec.pk)
                spec_item.voltage = spec.voltage
                spec_item.ip = spec.ip
                spec_item.im = spec.im
                spec_item.ic = spec.ic
                spec_item.summary = spec.summary
                spec_item.owner = request.user
                spec_item.xpref_id = proforma
                spec_item.reqspec_eq = spec
                try:
                    if proforma.req_id.customer.agent:
                        spec_item.price = MotorDB.objects.get(motor__code=spec_item.code).base_price
                    else:
                        spec_item.price = MotorDB.objects.get(motor__code=spec_item.code).sale_price
                except:
                    pass

                spec_item.save()
                spec.price = True
                spec.save()

            return redirect('prof_spec_form', ypref_pk=proforma.pk)
        else:
            pass
    else:
        if 'request_pk' in request.session:
            reqq = Requests.objects.filter(pk=request.session['request_pk'])
            data = {
                'req_id': Requests.objects.get(pk=request.session['request_pk']),
            }
            del request.session['request_pk']
        else:
            data = {}
        form = forms.ProformaForm(request.user.pk, data)

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
    # prices = request.POST.getlist('price')
    z = ['0.0', '0']
    prices = [i if i not in z else '0' for i in request.POST.getlist('price')]
    zeros = ['0' for i in prices]
    price_list = []
    # These checks if there is any string that can't be change to a number.
    for i in prices:
        try:
            price_list.append(float(i))
        except:
            messages.error(request, 'اشکال در اطلاعات قیمت')
            return redirect('prof_spec_form', ypref_pk=pref.pk)
    if prices == zeros:
        messages.error(request, 'پیش فاکتور شامل هیچ قیمتی نیست.')
        return redirect('prof_spec_form', ypref_pk=pref.pk)

    qty = request.POST.getlist('qty')
    if qty == ['0' for i in qty]:
        messages.error(request, 'پیش فاکتور شامل هیچ دستگاهی نیست.')
        return redirect('prof_spec_form', ypref_pk=pref.pk)

    considerations = request.POST.getlist('considerations')
    i = 0
    for s in prefspecs:
        s.qty = qty[i]
        s.price = prices[i] if prices[i] else 0
        s.considerations = considerations[i]
        s.save()
        i += 1

    return redirect('pref_details', ypref_pk=pref.pk)


@login_required
def pref_edit(request, ypref_pk):
    if not Xpref.objects.filter(is_active=True).filter(pk=ypref_pk):
        messages.error(request, 'no Proforma ّFound')
        return redirect('errorpage')
    xpref = Xpref.objects.filter(is_active=True).get(pk=ypref_pk)
    can_edit = funcs.has_perm_or_is_owner(request.user, 'request.change_xpref', xpref)
    if not can_edit:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

    # spec_prices = [float(i.replace(',', '')) for i in request.POST.getlist('price')]
    # spec_prices = request.POST.getlist('price')
    spec_prices = [i if i is not '' else '0' for i in request.POST.getlist('price')]
    zeros = ['0' for i in spec_prices]
    if spec_prices == zeros:
        messages.error(request, 'پیش فاکتور شامل هیچ قیمتی نیست.')
        return redirect('pref_edit_form', ypref_pk=xpref.pk)

    spec_qty = request.POST.getlist('qty')
    if spec_qty == ['0' for i in spec_qty]:
        messages.error(request, 'پیش فاکتور شامل هیچ دستگاهی نیست')
        return redirect('pref_edit_form', ypref_pk=xpref.pk)

    spec_qty_sent = request.POST.getlist('qty_sent')
    for i in range(len(spec_qty)):
        if int(spec_qty_sent[i]) > int(spec_qty[i]):
            messages.error(request, 'تعداد ارسال شده نمیتواند از تعداد سفارش بیشتر باشد.')
            return redirect('pref_edit_form', ypref_pk=xpref.pk)
    spec_sent = request.POST.getlist('sent')
    prof_images = xpref.proffiles_set.all()
    xspec = xpref.prefspec_set.all()
    x = 0
    for item in xspec:
        item.sent = True if str(item.pk) in spec_sent and spec_prices[x] != 0 and item.xpref_id.perm else False
        item.price = spec_prices[x]
        item.qty = spec_qty[x]

        item.qty_sent = spec_qty_sent[x]
        item.save()
        x += 1
    prefspecs = xpref.prefspec_set.all()
    nestes_dict = {}
    i = 0
    for prefspec in prefspecs:
        kw = prefspec.kw
        speed = prefspec.rpm
        price = MotorDB.objects.filter(motor__kw=kw, motor__speed=speed, motor__voltage=prefspec.voltage).last()
        if hasattr(price, 'prime_cost') and price.prime_cost:
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

    # messages.add_message(request, level=20, message=f"پیش فاکتور شماره {xpref.number} برزورسانی شد.")
    messages.add_message(request, messages.SUCCESS, message=f"پیش فاکتور شماره {xpref.number} برزورسانی شد.")

    return redirect('pref_details', ypref_pk=xpref.pk)

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

    can_read = funcs.has_perm_or_is_owner(request.user, 'request.change_xpref', prof)
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
    if prof.due_date:
        prof.due_date = prof.due_date.togregorian()
    if prof.perm_date:
        prof.perm_date = prof.perm_date.togregorian()
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

        perm = True if prof.perm else False
        for prof_spec in prof.prefspec_set.all():
            if not prof.perm and prof_spec.sent:
                prof_spec.sent = False
                prof_spec.save()

            reqSpec = prof_spec.reqspec_eq
            reqSpec.permission = perm
            reqSpec.save()
        return redirect('pref_index')

    context = {
        'form': form,
        'prof_file': img_form,
        'prof_images': prof_images,
        'img_names': img_names,
        'message': 'ویرایش پیش فاکتور',
    }
    return render(request, 'requests/admin_jemco/ypref/proforma_form.html', context)


@login_required
def to_follow(request, ypref_pk):
    prof = Xpref.objects.get(pk=ypref_pk)
    prof.to_follow = not prof.to_follow
    prof.on = prof.to_follow
    prof.save()
    return redirect('pref_index')


@login_required
def pref_insert(request):
    # can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_xpref')
    reqs = Requests.objects.filter(is_active=True)
    req_no = request.POST['req_no']
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
    can_edit = funcs.has_perm_or_is_owner(request.user, 'request.change_xpref', proforma)
    if not can_edit:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')
    show = True
    if proforma.total_proforma_price_vat()['price_vat'] == 0:
        show = False
    prof_specs = proforma.prefspec_set.all()
    context = {
        'proforma': proforma,
        'prof_specs': prof_specs,
        'show': show,
    }

    return render(request, 'requests/admin_jemco/ypref/edit_form.html', context)


@login_required
def prof_spec_form(request, ypref_pk):
    if not Xpref.objects.filter(is_active=True).filter(pk=ypref_pk):
        messages.error(request, 'no Proforma')
        return redirect('errorpage')
    proforma = Xpref.objects.filter(is_active=True).get(pk=ypref_pk)
    req = proforma.req_id
    reqspecs = req.reqspec_set.filter(is_active=True)

    can_add = funcs.has_perm_or_is_owner(request.user, 'request.add_xpref', instance=proforma)

    if not can_add:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

    if request.method == 'POST':
        print(request.POST)
        print('this is not ran at all')
        # form = forms.ProfSpecForm(request.POST, request.user)
        form = forms.ProfSpecForm(request.POST)
        if form.is_valid():
            spec = form.save(commit=False)
            spec.xpref_id = proforma
            spec.save()
            # return redirect('prof_spec_form', ypref_pk=proforma.pk)
            return redirect('pref_insert_spec_form', ypref_pk=proforma.pk)
        else:
            print('form is not valid')
    else:
        pass
        # form = forms.ProfSpecForm(request.POST)

    context = {
        # 'form': form,
        'proforma': proforma,
        'req_obj': req,
        'reqspecs': reqspecs,
        'prefspecs': proforma.prefspec_set.all()
    }
    return render(request, 'requests/admin_jemco/ypref/proforma_specs.html', context)


@login_required
def proforma_pdf(request, ypref_pk, render_header):
    render_header = True if render_header == 'True' else False
    footer = False

    logo_img = static('request/admin_jemco/images/logo.jpg')
    prizes_img = static('request/admin_jemco/images/prizes.jpg')

    logo_full_url = request.build_absolute_uri(logo_img)
    prizes_full_url = request.build_absolute_uri(prizes_img)

    header = render_header
    footer = render_header

    if not Xpref.objects.filter(pk=ypref_pk):
        messages.error(request, 'Nothin found')
        return redirect('errorpage')

    pref = Xpref.objects.get(pk=ypref_pk)
    can_read = funcs.has_perm_or_is_owner(request.user, 'request.read_proforma', pref)

    if not can_read:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

    import os
    from django.conf import settings
    css = [
        os.path.join(settings.STATIC_ROOT, 'request', 'rtl', 'build', 'css', 'style.css'),
        os.path.join(settings.STATIC_ROOT, 'request', 'rtl', 'build', 'css', 'pdf_style.css'),
        # os.path.join(settings.STATIC_ROOT, 'request', 'rtl', 'build', 'css', 'pdf_style2.css'),
        os.path.join(settings.STATIC_ROOT, 'request', 'rtl', 'build', 'css', 'custom.min.css'),
        os.path.join(settings.STATIC_ROOT, 'request', 'rtl', 'vendors', 'bootstrap', 'dist', 'css',
                     'bootstrap.min.css'),
        os.path.join(settings.STATIC_ROOT, 'request', 'rtl', 'vendors', 'bootstrap-rtl', 'dist', 'css',
                     'bootstrap-rtl.css')
    ]

    options = {
        'page-size': 'A4',
        'margin-top': '1.2in',
        # 'margin-top': '0.77in',
        'margin-right': '0.1in',
        'margin-bottom': '1.37795in',
        'margin-left': '0.1in',
        'encoding': "UTF-8",
        # 'footer-html': 'http://google.com',
    }
    if header:
        # options['margin-top'] = '0in'
        options.update({
            'header-html': request.build_absolute_uri(reverse('pdf_header')),
        })
        # del(options['header-html'])
    if footer:
        # options['margin-bottom'] = '0.1in'
        options.update({
            'footer-html': request.build_absolute_uri(reverse('pdf_footer')),
        })

    nestes_dict = {}
    proforma_total = 0
    kw_total = 0

    prof_images = pref.proffiles_set.all()
    prefspecs = pref.prefspec_set.filter(qty__gt=0, price__gt=0)
    i = 0
    for prefspec in prefspecs:
        proforma_total += prefspec.qty * prefspec.price
        kw_total += prefspec.qty * prefspec.kw
        nestes_dict[i] = {
            'obj': prefspec,
            'spec_total': prefspec.qty * prefspec.price
        }
        i += 1

    if request.method == 'POST':
        comment = pref.comments.create(author=request.user, body=request.POST['body'])
        pref.comments.all().update(is_read=True)
        comment.is_read = False
        comment.save()

    data = {
        'pref': pref,
        'prefspecs': prefspecs,
        'nested': nestes_dict,
        'vat': proforma_total * 0.09,
        'no_total': proforma_total,
        'proforma_total': proforma_total * 1.09,
        'kw_total': kw_total,
        'prof_images': prof_images,
        'comment_form': CommentForm(),
        'header': header,
        'footer': footer,
        'logo_full_url': logo_full_url,
        'prizes_full_url': prizes_full_url,
        'today': jdatetime.date.today()
    }
    size = len(data['prefspecs'])
    critical_range = [19, 20]
    if size in critical_range:
        options.update({'margin-bottom': '2.15039in'})

    content = render_to_string(
        # 'requests/admin_jemco/ypref/details_pdf.html', {
        'requests/admin_jemco/ypref/details_pdf_with_header.html', {
            'contents': data
        }
    )

    pdf = pdfkit.PDFKit(content, "string", options=options, css=css).to_pdf()
    size = pdf.__sizeof__()
    response = HttpResponse(pdf)
    response['Content-Type'] = 'application/pdf'

    # response['Content-disposition'] = 'attachment;filename={}.pdf'.format(your_filename)
    # response['Content-disposition'] = 'inline;filename={}.pdf'.format('output')
    # response['Content-disposition'] = 'inline;filename={}{}.pdf'.format(
    response['Content-disposition'] = 'attachment;filename=PF_{}_Req{}_{}.pdf'.format(
        pref.number,
        pref.req_id.number,
        pref.owner.username,
    )

    pdf_render = True
    if pdf_render:
        return response
    else:
        context = {
            'contents': data,
            'size': size,
        }
        return render(request, 'requests/admin_jemco/ypref/details_pdf_with_header.html', context)


@login_required
def followup_delete(request, followup_pk):
    followup = ProformaFollowUP.objects.get(pk=followup_pk)
    pref_pk = followup.xpref.pk
    followup.delete()
    return redirect('pref_details', ypref_pk=pref_pk)


def pdf_header(request):
    # return render(request, 'requests/admin_jemco/ypref/header.html')
    context = {
        'today': jdatetime.date.today()
    }
    return render(request, 'requests/admin_jemco/ypref/header.html', context)


def pdf_footer(request):
    return render(request, 'requests/admin_jemco/ypref/footer.html')


def proforma_has_payment_no_perm(request):
    np = Xpref.objects.filter(is_active=True, payment__isnull=False, perm_prof__isnull=True).distinct()
    perm_no_payments = Perm.objects.filter(proforma__payment__isnull=True)
    ps = Xpref.objects.filter(is_active=True)

    if not request.user.is_superuser:
        np = np.filter(owner=request.user)
        perm_no_payments = perm_no_payments.filter(proforma__owner=request.user)

    all_proformas = [proforma.number_td for proforma in ps if proforma.number_td is not None]
    duplicates_proforma_tds = []
    for proforma in all_proformas:
        count = all_proformas.count(proforma)
        if count > 1 and duplicates_proforma_tds.count(proforma) == 0:
            duplicates_proforma_tds.append(proforma)

    context = {
        'prof_has_payment_no_perm': np,
        'perm_no_payments': perm_no_payments,
        'duplicates_proforma_tds': duplicates_proforma_tds,
    }
    return render(request, 'requests/admin_jemco/ypref/has_payment_not_perm.html', context)