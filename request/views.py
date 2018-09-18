from django.shortcuts import render
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