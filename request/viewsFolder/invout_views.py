from django.shortcuts import render

from request.models import InventoryOut


def form(request):
    pass


def invout_index(request):
    invouts = InventoryOut.objects.all()
    context = {
        'invouts': invouts,
    }
    return render(request, 'requests/admin_jemco/invouts/index.html', context)


def invout_find(request):
    pass


def invout_details(request, invout_pk):
    invout = InventoryOut.objects.get(pk=invout_pk)
    invout_specs = invout.inventoryoutspec_set.all()
    context = {
        'invout': invout,
        'invout_specs': invout_specs,
    }
    return render(request, 'requests/admin_jemco/invouts/details.html', context)


def invout_delete(request):
    pass


def invout_edit(request):
    pass

