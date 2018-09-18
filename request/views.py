import json
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Requests
from .models import Prefactor
from .models import PrefactorVerification
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
    x = Requests.objects.all().values()
    return HttpResponse(x)


