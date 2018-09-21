import json
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Requests
from .models import Prefactor
from .models import PrefactorVerification
from django.contrib.auth.decorators import login_required
# Create your views here.


def request_page(request):
    allRequests = Requests.objects
    return render(request, 'requests/requests.html', {'allRequests': allRequests})


def prefactors_page(request):
    allPrefactos = Prefactor.objects
    return render(request, 'requests/prefactors.html', {'allPrefactors': allPrefactos})


def prefactors_verification_page(request):
    allPrefVerifications = PrefactorVerification.objects
    return render(request, 'requests/prefVerificationsPage.html', {'allPrefVerifications': allPrefVerifications})


def request_details(request, request_id):
    req = get_object_or_404(Requests, pk=request_id)
    return render(request, 'requests/req_details.html', {'request': req})

def prefactor_details(request, pref_id):
    pref = get_object_or_404(Prefactor, pk=pref_id)
    return render(request, 'requests/pref_details.html', {'prefactor': pref})


def pref_ver_details(request, pref_ver_id):
    pref_ver = get_object_or_404(PrefactorVerification, pk=pref_ver_id)
    return render(request, 'requests/pref_ver_details.html', {'pref_ver': pref_ver})


def allTable(request):
    x = Requests.objects.get(pk=1)
    x2 = Requests.objects.all()
    y = x.prefactor_set.all()
    # z = Prefactor.objects.get(pk=1).prefactorverification_set

    return render(request, 'prefactors/homepage.html', {'reqs': x2, 'prefs': y})


def find_pref(request):
    pref_no = request.POST['pref_no']
    prefactor = Prefactor.objects.get(number=pref_no)
    related_request = prefactor.request_id
    pre_ver = prefactor.prefactorverification_set.all()

    return render(
        request,
        'requests/results.html',
        {'prefactor': prefactor, 'verification': pre_ver, 'related_request': related_request}
    )


@login_required
def create_req(request):
    if request.method == 'POST':
        if request.POST['req_no'] and request.POST['req_summary']:
            req = Requests()
            req.number = request.POST['req_no']
            req.summary = request.POST['req_summary']
            req.image = request.FILES['req_file']
            req.pub_date = timezone.datetime.now()
            req.save()
            return redirect('allTables')
        else:
            return render(request, 'requests/create.html', {'error': 'some field is empty'})
    return render(request, 'requests/create.html')

@login_required
def create_pref(request):
    if request.method == 'POST':
        if request.POST['number'] and request.POST['summary'] and request.FILES:

            if Requests.objects.get(number=request.POST['req_number']):
                try:
                    related_req = Requests.objects.get(number=request.POST['req_number'])
                    pref = Prefactor()
                    pref.number = request.POST['number']
                    pref.request_id = related_req
                    pref.summary = request.POST['summary']
                    pref.image = request.FILES['image']
                    pref.pub_date = timezone.datetime.now()
                    pref.save()
                    return redirect('allTables')
                except Requests.DoesNotExist:
                    return render(request, 'prefactors/create.html', {'error': 'no such request'})
        else:
            list = allRequests()
            return render(request, 'prefactors/create.html', {'list': list, 'error': 'some field is empty'})
    return render(request, 'requests/create.html')

@login_required
def createpage(request):
    return render(request, 'requests/create.html')

@login_required
def createprefpage(request):
    list = allRequests()
    print(list)
    return render(request, 'prefactors/create.html', {'list': list})

@login_required
def create_verf_page(request, error=''):
    list = allPref()
    return render(request, 'prefVerification/create.html', {'list': list, 'error': error})

def create_verf(request):
    print(request)
    if request.method == 'POST':
        if request.POST['number'] and request.POST['summary'] and request.FILES:
            if Prefactor.objects.get(number=request.POST['pref_number']):
                try:
                    related_pref = Prefactor.objects.get(number=request.POST['pref_number'])
                    verf = PrefactorVerification()
                    verf.number = request.POST['number']
                    verf.pref_id = related_pref
                    verf.summary = request.POST['summary']
                    verf.image = request.FILES['image']
                    verf.pub_date = timezone.datetime.now()
                    verf.save()
                    return redirect('allTables')
                except Prefactor.DoesNotExist:
                    return render(request, 'prefVerification/create.html', {'error': 'no such request'})
        else:
            allprefactors = allPref()
            return render(request, 'prefVerification/create.html', {'error': 'some field is empty', 'list': allprefactors})
    return render(request, 'prefVerification/create.html')

def allPref():
    allPref = Prefactor.objects.all()
    list = []
    for pref in allPref:
        list.append(pref.number)
    list.sort()
    return list

def allRequests():
    allreq = Requests.objects.all()
    list = []
    for req in allreq:
        list.append(req.number)
    list.sort()
    return list