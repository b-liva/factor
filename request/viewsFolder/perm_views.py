from django.shortcuts import render

from request.models import Perm, Xpref
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
    no_proforma = []

    perms = TadvinTotal.objects.filter(doctype_code=62, entered=False, perm_number__gt=1000)\
        .values('perm_number').distinct().values('perm_number', 'prof_number', 'date')

    perms_sales = TadvinTotal.objects.filter(doctype_code=62, entered=False, perm_number__gte=1000, perm_number__lt=2000)\
        .values('perm_number').distinct().values('perm_number', 'prof_number', 'date')
    perms_parts = TadvinTotal.objects.filter(doctype_code=62, entered=False, perm_number__gte=2000, perm_number__lt=3000)\
        .values('perm_number').distinct().values('perm_number', 'prof_number', 'date')
    perms_services = TadvinTotal.objects.filter(doctype_code=62, entered=False, perm_number__gte=3000, perm_number__lt=4000)\
        .values('perm_number').distinct().values('perm_number', 'prof_number', 'date')
    perms_wastages = TadvinTotal.objects.filter(doctype_code=62, entered=False, perm_number__gte=4000, perm_number__lt=5000)\
        .values('perm_number').distinct().values('perm_number', 'prof_number', 'date')

    for a in perms:
        if not Xpref.objects.filter(number_td=a['prof_number']).exists():
            no_proforma.append({'perm_number': a['perm_number'], 'prof_number': a['prof_number']})

    context = {
        'perms_sales': perms_sales,
        'perms_parts': perms_parts,
        'perms_services': perms_services,
        'perms_wastages': perms_wastages,
        'perms': perms,
        'no_proforma': no_proforma,
    }
    return render(request, 'requests/admin_jemco/perms/index_not_entered.html', context)

