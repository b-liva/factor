from django.shortcuts import render
from .models import PrefactorVerification


def pref_verification(request):
    pref_ver = PrefactorVerification.objects
    return render(request, 'prefVerification/prefVerification.html', {'pref_ver': pref_ver})
