import json

from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

# from request.views import allRequests, find_all_obj
# from request.models import Requests
# from request.models import ReqSpec
# from request.models import permissionSpec
# from request.models import Xpermission
# from request.models import Payment
# from request.models import XpermissionVerf
# from customer.models import Customer
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def permission_form(request):
    pass

@login_required
def permission_insert(request):
    pass

@login_required
def permission_index(request):
    pass

@login_required
def permission_find(request):
    pass

@login_required
def permission_details(request, ypermission_pk):
    pass

@login_required
def permission_delete(request, ypermission_pk):
    pass

@login_required
def permission_edit_form(request, ypermission_pk):
    pass

@login_required
def permission_edit(request, ypermission_pk):
    pass

@login_required
def xpermission_link(request, xpermission_id):
    pass


