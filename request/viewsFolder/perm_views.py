from django.shortcuts import render

from request.models import Perm
from req_track.models import TadvinTotal


def form(request):
    pass


def perm_index(request):
    perms = Perm.objects.all()
    context = {
        'perms': perms,
    }
    return render(request, 'requests/admin_jemco/perms/index.html', context)


def perm_find(request):
    pass


def perm_details(request, perm_pk):
    perm = Perm.objects.get(pk=perm_pk)
    perm_specs = perm.permspec_perm.all()
    context = {
        'perm': perm,
        'perm_specs': perm_specs,
    }
    return render(request, 'requests/admin_jemco/perms/details.html', context)


def perm_delete(request):
    pass


def perm_edit(request):
    pass


def perm_not_entered(request):
    perms = TadvinTotal.objects.filter(doctype_code=62, entered=False, perm_number__gt=1000)\
        .values('perm_number').distinct().values('perm_number', 'prof_number', 'date')
    context = {
        'perms': perms,
    }
    return render(request, 'requests/admin_jemco/perms/index_not_entered.html', context)

