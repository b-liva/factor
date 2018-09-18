from django.shortcuts import render

from .models import PreFactor


def prefactors(request):
    prefs = PreFactor.objects
    return render(request, 'prefactors/prefactors.html', {'prefs':prefs})

def home(request):
    return render(request, 'prefactors/homepage.html')