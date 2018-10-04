from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Customer
from .models import Type
from request.models import Requests
from request.models import Xpref
from request.models import PrefSpec
from request.models import Payment


from django.views import View

class TestView(View):
    def get(self, request):
        pass
    def post(self, request):
        pass


from django.contrib.auth.decorators import login_required


def customer(request):
    customer_types = Type.objects.all()
    return render(request, 'customer/customer.html', {
        'customer_types': customer_types
    })


def customer_create(request):
    all_customers = Customer.objects.all()
    customer_types = Type.objects.all()
    customer_type = Type.objects.get(pk=request.POST['type'])
    customer = Customer()
    customer.name = request.POST['name']
    customer.code = request.POST['code']
    customer.type = customer_type
    customer.save()
    msg = 'Customer added successfully'
    return render(request, 'customer/customer.html', {
        'msg': msg,
        'customer_types': customer_types,
        'all_customers': all_customers
    })


def customer_read(request):
    customers = Customer.objects.all()
    print(customers)
    x = 0
    for customer in customers:
        reqs = Requests.objects.filter(customer=customer)
        print('customer name: ' + customer.name)
        for req in reqs:
            print('     req No. ' + str(req.number))
            xprefs = Xpref.objects.filter(req_id=req)

            for xpref in xprefs:
                print('         prefactor number ' + str(xpref.number))
                specs = PrefSpec.objects.filter(xpref_id=xpref)
                payments = Payment.objects.filter(xpref_id=xpref)
                for payment in payments:
                    print('             payment: ' + str(payment.amount))
                x += 1



    print('total orders ' + str(x))

    return render(request, 'customer/read.html')


def customer_update(request):
    pass


def customer_delete(request):
    pass


def type_create(request):
    pass


def type_read(request):
    pass


def type_update(request):
    pass


def type_delete(request):
    pass