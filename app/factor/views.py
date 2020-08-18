from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect


def comming_soon(request):
    return render(request, 'general/comming_soon.html')