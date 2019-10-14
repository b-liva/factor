from django.shortcuts import render

from request.models import Perm


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
    print('hello from perm details')
    perm = Perm.objects.get(pk=perm_pk)
    context = {
        'perm': perm,
    }
    return render(request, 'requests/admin_jemco/perms/details.html', context)


def perm_delete(request):
    pass


def perm_edit(request):
    pass

