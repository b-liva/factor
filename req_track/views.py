import datetime
import math

import jdatetime
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, F, FloatField
from django.shortcuts import render, redirect

from accounts.models import User
from request.forms.forms import ReqFollowUpForm
from request.forms.proforma_forms import ProfFollowUpForm
from request.models import Requests, Xpref, PrefSpec, ReqSpec
from request.models import Payment as Request_payment
from req_track.models import ReqEntered, Payments, TrackItemsCode, TrackXpref, ProformaFollowUp
from .forms import E_Req_Form
from django.db import models


# Create your views here.


@login_required
def e_req_add(request):
    if request.method == 'POST':
        form = E_Req_Form(request.POST or None)
        if form.is_valid():
            ereq_item = form.save(commit=False)
            # if Requests.objects.get(number=request.POST['number']):
            #     ereq_item.started = True
            ereq_item.save()
            return redirect('req_track:e_req_index')
    if request.method == 'GET':
        form = E_Req_Form()

    context = {
        'form': form,
    }
    return render(request, 'req_track/add_form.html', context)


@login_required
def e_req_index(request):
    reqs = ReqEntered.objects.all()
    context = {
        'reqs': reqs,
    }
    return render(request, 'req_track/ereq_notstarted.html', context)


@login_required
def e_req_read(request):
    pass


@login_required
def e_req_delete(request):
    pass


@login_required
def e_req_delete_all(request):
    ereq_all = ReqEntered.objects.all()
    for e in ereq_all:
        e.delete()

    return redirect('req_track:e_req_index')


def e_req_report(request):
    reqs = ReqEntered.objects.filter(is_entered=False, is_request=True)
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
        'expert': {
            'zarif': zarif_account,
            'mohammadi': mohammadi_account,
            'alavi': alavi_account,
            'foroughi': foroughi_account,
        },
        'reqs': reqs,
        'zarif': zarif,
        'mohammadi': mohammadi,
        'alavi': alavi,
        'show': True,
        'title_msg': 'درخواست های وارد نشده'
    }
    return render(request, 'req_track/ereq_notstarted.html', context)


@login_required
def check_orders(request):
    ereqs = ReqEntered.objects.filter(is_entered=False)
    for e in ereqs:
        if Requests.objects.filter(is_active=True).filter(number=e.number_automation):
            print(f"order No: {e.number_automation}: is entered.")
            e.is_entered = True
            e.save()
        else:
            print(f"order No: {e.number_automation}: is not entered.")

    return redirect('req_track:e_req_report')


def users_summary(user_txt, user_account, date, not_entered_reqs):
    reqs = Requests.objects.filter(is_active=True, date_fa__gte=date, owner=user_account)
    all_reqs = Requests.objects.filter(is_active=True, owner=user_account)
    result_list = []
    for req in reqs:
        delay_entered = jdatetime.date.fromgregorian(date=req.pub_date, locale='fa_IR') - req.date_fa
        result_list.append(delay_entered.days)
    if len(result_list):
        avg_time = sum(result_list) / len(result_list)
    else:
        avg_time = 0
    response = {
        'not_entered': not_entered_reqs.filter(owner_text__contains=user_txt),
        'avg_time': avg_time,
        'count': all_reqs.count(),
    }
    return response


@login_required
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


@login_required
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


@login_required
def payment_check(request):
    payments_not_flaged = Payments.objects.filter(red_flag=False)

    for p in payments_not_flaged:
        if Request_payment.objects.filter(number=p.number):
            p.is_entered = True
        try:
            Xpref.objects.get(number=p.prof_number)
        except:
            p.red_flag = True

        p.date_txt = p.date_txt.replace('/', '-')
        date = p.date_txt.split('-')
        for key, value in enumerate(date):
            if len(value) == 2 and int(value) > 40:
                date[key] = str(int(value) + 1300)
            else:
                date[key] = value
        s = '-'
        p.date = s.join(date)
        p.save()
    return redirect('req_track:payment_index')


@login_required
def payment_index(request):
    payments = Payments.objects.all()
    context = {
        'payments': payments,
    }
    return render(request, 'payments/paymets_index.html', context)


@login_required
def payment_assign(request):
    payments = Payments.objects.filter(red_flag=False, is_entered=False)

    for payment in payments:
        # if not Request_payment.objects.filter(number=payment.number):
        proforma = Xpref.objects.get(number=payment.prof_number)
        pay = Request_payment()
        pay.number = payment.number
        pay.date_fa = payment.date
        pay.xpref_id = proforma
        pay.amount = payment.amount
        pay.customer = proforma.req_id.customer
        pay.owner = request.user
        pay.save()
        payment.is_entered = True
        payment.save()

    return redirect('payment_index')


def motor_codes_index(request):
    all_codes = TrackItemsCode.objects.filter(green_flag=True, code__gt=1000000)
    print(all_codes.count())
    context = {
        'all_codes': all_codes,
    }

    return render(request, 'codes/codes.html', context)


def motor_codes_check(request):
    all_codes = TrackItemsCode.objects.all()
    print(all_codes.count())
    keywords = ['وات', 'موتور', 'kw', 'rpm']
    for code in all_codes:
        if any(keyword in code.details for keyword in keywords):
            code.green_flag = True
            code.save()

    return redirect('req_track:motor_codes_index')


def motor_codes_process(request):
    green_codes = TrackItemsCode.objects.filter(green_flag=True)[0:150]
    for code in green_codes:
        a = code.details.split('.')
        for key, x in enumerate(a):
            print(x)
            y = x.split(' ')
            if len(y) > 1:
                print(y)
                del (a[key])
                for i in y:
                    a.append(i)
            y = x.split('-')
            if len(y) > 1:
                print(y)
                del (a[key])
                for i in y:
                    a.append(i)
        separator = "*%&"
        code.temp_str = separator.join(a)
        for value in a:
            if value.find('kw') >= 0:
                kw = value.replace('kw', '')
                code.kw = kw
            if value.find('کیلووات') >= 0:
                kw = value.replace('کیلووات', '')
                code.kw = kw
            if value.find('rpm') >= 0:
                rpm = value.replace('rpm', '')
                code.speed = rpm
            if value.find('دور') >= 0:
                rpm = value.replace('دور', '')
                code.speed = rpm
            if value.find('ip') >= 0:
                ip = value.replace('ip', '')
                code.ip = ip
            if value.find('ic') >= 0:
                ic = value.replace('ic', '')
                code.ic = ic
        code.save()

    return redirect('req_track:motor_codes_index')


def proformas(request):
    all_proformas = TrackXpref.objects.filter(red_flag=False, is_entered=False).order_by('date_fa')
    count = all_proformas.values('number').distinct().count()

    context = {
        'all_proformas': all_proformas,
        'count': count,
        'title': 'وارد نشده',
    }

    return render(request, 'proformas/proformas.html', context)


def proformas_complete(request):
    all_proformas = TrackXpref.objects.filter(is_entered=True, red_flag=False)
    count = all_proformas.values('number').distinct().count()

    context = {
        'all_proformas': all_proformas,
        'count': count,
        'title': 'وارد شده',
    }

    return render(request, 'proformas/proformas.html', context)


def proformas_uncomplete(request):
    all_proformas = TrackXpref.objects.filter(red_flag=True, is_entered=True)
    count = all_proformas.values('number').distinct().count()

    context = {
        'all_proformas': all_proformas,
        'title': 'خطا',
        'count': count,
    }

    return render(request, 'proformas/proformas.html', context)


def track_prof_count(track_prof):
    count = TrackXpref.objects.filter(number=track_prof.number).aggregate(Sum('qty'))
    return count


def prof_count(prof):
    count = prof.prefspec_set.filter(price__gt=0).aggregate(Sum('qty'))
    return count


def check_proforma(request):
    allproformas = TrackXpref.objects.all()
    for track_prof in allproformas:
        try:
            prof = Xpref.objects.get(number=track_prof.number)
            if prof.prefspec_set.filter(price__gt=0).count() == TrackXpref.objects.filter(
                    number=track_prof.number).count() and \
                    prof_count(prof) == track_prof_count(track_prof):
                # entered with no error -> Complete
                track_prof.is_entered = True
                track_prof.red_flag = False
            else:
                # there is some error with this item
                track_prof.is_entered = True
                track_prof.red_flag = True
        except:
            # it is not entered.
            track_prof.is_entered = False
            track_prof.red_flag = False

        track_prof.save()
    return redirect('req_track:proformas')


def create_proforma(request):
    """
    Creates Proformas from imported proformas. Works with proformas that are not entered before.
    :param request:
    :return: None
    """
    proformas = TrackXpref.objects.exclude(is_entered=True, req_number__isnull=True)
    for proforma in proformas:
        try:
            req = Requests.objects.get(number=proforma.req_number)
            if Xpref.objects.filter(number=proforma.number):
                prof = Xpref.objects.get(number=proforma.number)
            else:
                prof = Xpref()
                prof.number = proforma.number
                prof.owner = req.owner
                prof.req_id = req
                prof.date_fa = proforma.date_fa.replace('/', '-')
                prof.summary = 'added automatically'
                prof.save()
                for r in req.reqspec_set.filter(is_active=True):
                    ps = PrefSpec()
                    ps.code = r.code
                    ps.type = r.type
                    ps.code = r.code
                    ps.price = 0
                    ps.kw = r.kw
                    ps.qty = r.qty
                    ps.rpm = r.rpm
                    ps.voltage = r.voltage
                    ps.ip = r.ip
                    ps.ic = r.ic
                    ps.summary = r.summary
                    ps.owner = request.user
                    ps.xpref_id = prof
                    ps.reqspec_eq = r
                    ps.summary = 'added automatically'
                    ps.save()
            if req.reqspec_set.filter(code=proforma.code):
                ps = prof.prefspec_set.get(code=proforma.code)
                ps.price = proforma.price
                ps.save()
            else:
                prof.delete()
        except:
            pass

    return redirect('req_track:check_proforma')


def clear_flags(request):
    profs = TrackXpref.objects.all()
    profs.update(is_entered=False, red_flag=False)
    return redirect('req_track:proformas_uncomplete')


def prof_followup_list(request):
    profs = ProformaFollowUp.objects.all()

    context = {
        'profs': profs,
        'title': 'پیگیری پیش فاکتور',
    }

    return render(request, 'proformas/followup/index.html', context)


def prof_followup_list2(request):
    # profs = Xpref.objects.filter(is_active=True)
    profs = Xpref.objects.all()

    context = {
        'profs': profs,
        'title': 'پیگیری پیش فاکتور',
    }

    return render(request, 'proformas/followup/index2.html', context)


def prof_followup_find(request):
    if request.method == 'POST':
        number = request.POST['prof_number']
        print(number)
        if Xpref.objects.get(number=int(number)):
            prof = Xpref.objects.get(number=int(number))
            print('Ok')
            return redirect('req_track:prof_followup_form', prof_pk=prof.pk)
        else:
            print('Not Ok')
    context = {
        'title': 'پیش فاکتور'
    }
    return render(request, 'proformas/followup/find.html', context)


def prof_followup_form(request, prof_pk):
    prof = Xpref.objects.get(pk=prof_pk)
    form = ProfFollowUpForm(instance=prof)
    if request.method == 'POST':
        form = ProfFollowUpForm(request.POST or None, instance=prof)
        if form.is_valid():
            proforma = form.save(commit=False)
            proforma.on = False
            proforma.save()
            return redirect('req_track:prof_followup_find')

    context = {
        'prof': prof,
        'form': form
    }

    return render(request, 'proformas/followup/form.html', context)


def req_followup_form(request, req_pk):
    req = Requests.objects.get(pk=req_pk)
    form = ReqFollowUpForm(instance=req)
    if request.method == 'POST':
        form = ReqFollowUpForm(request.POST or None, instance=req)
        if form.is_valid():
            req = form.save(commit=False)
            req.on = False
            req.save()
            return redirect('req_track:prof_followup_find')

    context = {
        'item': req,
        'form': form
    }

    return render(request, 'proformas/followup/form.html', context)
