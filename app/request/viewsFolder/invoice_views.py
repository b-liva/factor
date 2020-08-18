from django.shortcuts import render

from request.models import Invoice


def form(request):
    pass


def invoice_index(request):
    invoices = Invoice.objects.all()
    context = {
        'invoices': invoices,
    }
    return render(request, 'requests/admin_jemco/invoice/index.html', context)


def invoice_find(request):
    pass


def invoice_details(request, invoice_pk):
    invoice = Invoice.objects.get(pk=invoice_pk)
    invoice_specs = invoice.invoicespec_set.all()
    context = {
        'invoice': invoice,
        'invoice_specs': invoice_specs,
    }
    return render(request, 'requests/admin_jemco/invoice/details.html', context)


def invoice_delete(request):
    pass


def invoice_edit(request):
    pass

