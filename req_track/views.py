import math

import jdatetime
from django.db.models import Q
from django.shortcuts import render, redirect

from accounts.models import User
from request.models import Requests
from req_track.models import ReqEntered
from .forms import E_Req_Form
from django.db import models

# Create your views here.


def e_req_add(request):

    if request.method == 'POST':
        form = E_Req_Form(request.POST or None)
        if form.is_valid():
            ereq_item = form.save(commit=False)
            # if Requests.objects.get(number=request.POST['number']):
            #     ereq_item.started = True
            ereq_item.save()
            return redirect('e_req_index')
    if request.method == 'GET':
        form = E_Req_Form()

    context = {
        'form': form,
    }
    return render(request, 'req_track/add_form.html', context)


def e_req_index(request):
    reqs = ReqEntered.objects.all()
    context = {
        'reqs': reqs,
    }
    return render(request, 'req_track/ereq_notstarted.html', context)


def e_req_read(request):
    pass


def e_req_delete(request):
    pass


def e_req_delete_all(request):
    ereq_all = ReqEntered.objects.all()
    for e in ereq_all:
        e.delete()

    return redirect('e_req_index')


def e_req_report(request):
    reqs = ReqEntered.objects.filter(is_entered=False).filter(is_request=True)
        # .exclude(owner_text__contains='ظریف')\
        # .exclude(owner_text__contains='محمدی')\
        # .exclude(owner_text__contains='علوی')
    second = reqs
    if not request.user.is_superuser:
        reqs = reqs.filter(owner_text__contains=request.user.last_name)

    mohammadi_account = User.objects.get(pk=2)
    alavi_account = User.objects.get(pk=3)
    zarif_account = User.objects.get(pk=4)
    foroughi_account = User.objects.get(pk=5)
    date = '1397-11-01'

    zarif = users_summary('ظریف', zarif_account, date, reqs)
    mohammadi = users_summary('محمدی', mohammadi_account, date, reqs)
    alavi = users_summary('علوی', alavi_account, date, reqs)
    # print(zarif['avg_time']['avg_tm'])
    # mohammadi = reqs.filter(owner_text__contains='محمدی')
    # alavi = reqs.filter(owner_text__contains='علوی')
    context = {
        'reqs': reqs,
        'zarif': zarif,
        'mohammadi': mohammadi,
        'alavi': alavi,
        'show': True,
        'title_msg': 'درخواست های وارد نشده'
    }
    return render(request, 'req_track/ereq_notstarted.html', context)


def check_orders(request):
    ereqs = ReqEntered.objects.filter(is_entered=False)
    for e in ereqs:
        if Requests.objects.filter(is_active=True).filter(number=e.number_automation):
            print(f"order No: {e.number_automation}: is entered.")
            e.is_entered = True
            e.save()
        else:
            print(f"order No: {e.number_automation}: is not entered.")

    return redirect('e_req_report')


def users_summary(user_txt, user_account, date, not_entered_reqs):
    reqs = Requests.objects.filter(is_active=True).filter(date_fa__gte=date).filter(owner=user_account)
    result_list = []
    for req in reqs:
        delay_entered = jdatetime.date.fromgregorian(date=req.pub_date, locale='fa_IR') - req.date_fa
        result_list.append(delay_entered.days)
    if len(result_list):
        avg_time = sum(result_list)/len(result_list)
    else:
        avg_time = 0
    response = {
        'not_entered': not_entered_reqs.filter(owner_text__contains=user_txt),
        'avg_time': avg_time,
        'count': reqs.count(),
    }
    return response


def e_req_report_proformas(request):
    reqs = ReqEntered.objects.filter(is_entered=False).filter(is_request=False)

    if not request.user.is_superuser:
        reqs = reqs.filter(owner_text__contains=request.user.last_name)

    reqs = reqs.filter(
        Q(title__icontains='پیشفاکتور') |
        Q(title__icontains='پیش فاکتور')
    )
    context = {
        'reqs': reqs,
        'show': False,
        'title_msg': 'تایید پیش فاکتورها'

    }
    return render(request, 'req_track/ereq_notstarted.html', context)


def e_req_report_payments(request):
    reqs = ReqEntered.objects.filter(is_entered=False).filter(is_request=False)

    if not request.user.is_superuser:
        reqs = reqs.filter(owner_text__contains=request.user.last_name)

    reqs = reqs.filter(
        Q(title__icontains='واریز') |
        Q(title__icontains='مبلغ') |
        Q(title__icontains='ساتنا') |
        Q(title__icontains='تسویه') |
        Q(title__icontains='پیش پرداخت') |
        Q(title__icontains='پیشپرداخت') |
        Q(title__icontains='چک')
    )
    context = {
        'reqs': reqs,
        'show': False,
        'title_msg': 'اعلام واریزی'
    }
    return render(request, 'req_track/ereq_notstarted.html', context)
