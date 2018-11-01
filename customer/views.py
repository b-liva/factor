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
from request import views2
from django.contrib import messages
from customer import forms


import request.functions as funcs
from django.views import View

class TestView(View):
    def get(self, request):
        pass
    def post(self, request):
        pass


from django.contrib.auth.decorators import login_required

@login_required
def customer(request):
    customer_types = Type.objects.all()
    return render(request, 'customer/customer.html', {
        'customer_types': customer_types
    })

@login_required
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

@login_required
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


@login_required
def customer_form(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'customer.add_customer')
    if not can_add:
        messages.error(request, 'Sorry, No access for you')
        return redirect('errorpage')
    customer_types = Type.objects.all()
    customer_form = forms.CustomerForm()
    return render(request, 'customer/customer.html', {
        'customer_types': customer_types,
        'c_form': customer_form
    })


@login_required
def customer_insert(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'customer.add_customer')
    if not can_add:
        messages.error(request, 'Sorry, No access for you')
        return redirect('errorpage')
    all_customers = Customer.objects.all()
    customer_types = Type.objects.all()
    customer_type = Type.objects.get(pk=request.POST['type'])
    customer_to_insert = Customer()
    customer_to_insert.name = request.POST['name']
    customer_to_insert.code = request.POST['code']
    customer_to_insert.pub_date = request.POST['pub_date']
    customer_to_insert.date2 = request.POST['date2']
    customer_to_insert.type = customer_type
    customer_to_insert.save()
    msg = 'Customer added successfully'
    return render(request, 'customer/index.html', {
        'msg': msg,
        'customer_types': customer_types,
        'customers': all_customers
    })


@login_required
def customer_index(request):
    can_index = funcs.has_perm_or_is_owner(request.user, 'customer.index_customer')
    if not can_index:
        messages.error(request, 'No access to see list of customers')
        return redirect('errorpage')
    customers = Customer.objects.all()
    return render(request, 'customer/index.html', {'customers': customers})

@login_required
def customer_find(request):
    customer = Customer.objects.get(code=request.POST['customer_no'])
    return redirect('customer_read', customer_pk=customer.pk)

@login_required
def customer_read2(request, customer_pk):
    if not Customer.objects.filter(pk=customer_pk):
        messages.error(request, 'No such customer')
        return redirect('errorpage')
    customer = Customer.objects.get(pk=customer_pk)
    can_read = funcs.has_perm_or_is_owner(request.user, 'customer.read_customer', customer)
    if not can_read:
        messages.error(request, 'Sorry, no way for you to do that')
        return redirect('errorpage')
    # customer = Customer.objects.get(pk=customer_pk)
    customer_reqs = customer.requests_set.all()
    kw = {}
    some = {}
    for customer_req in customer_reqs:
        # specs = customer_req.reqspec_set.all()
        kw[customer_req.pk] = views2.total_kw(customer_req.pk)
        t_kw = views2.total_kw(customer_req.pk)
        some[t_kw] = customer_req
    print(type(kw))
    print(some)
    return render(request, 'customer/details.html', {
        'customer': customer,
        'customer_reqs': customer_reqs,
        'kw': kw,
        'some': some,
    })

@login_required
def customer_edit(request, customer_pk):
    if not Customer.objects.filter(pk=customer_pk):
        messages.error(request, 'No such Customer')
        return redirect('errorpage')

    customer_instance = Customer.objects.get(pk=customer_pk)
    can_edit = funcs.has_perm_or_is_owner(request.user, 'customer.edit_customer', customer_instance)
    if not can_edit:
        messages.error(request, 'Sorry, No access for you')
        return redirect('errorpage')
    pass


def customer_delete(request, customer_pk):
    if not Customer.objects.filter(pk=customer_pk):
        messages.error(request, 'No such Customer')
        return redirect('errorpage')
    customer_instance = Customer.objects.get(pk=customer_pk)
    can_delete = funcs.has_perm_or_is_owner(request.user, 'customer.delete_customer', customer_instance)
    if not can_delete:
        messages.error(request, 'Sorry, No access for you')
        return redirect('errorpage')
    customer = Customer.objects.get(pk=customer_pk)
    customer_name = customer.name
    customer.delete()
    msg = customer_name + ' removed successfully!'
    return redirect('customer_index')


# Type functions:
@login_required
def type_form(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'customer.add_type')
    if not can_add:
        messages.error(request, 'No access')
        return redirect('errorpage')
    return HttpResponse('customer type form goes here.')


@login_required
def type_insert(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'customer.add_type')
    if not can_add:
        messages.error(request, 'No access')
        return redirect('errorpage')
    return HttpResponse('customer type insertion goes here.')



@login_required
def type_index(request):
    pass


@login_required
def type_read(request, type_pk):
    pass


@login_required
def type_edit(request, type_pk):
    can_edit = funcs.has_perm_or_is_owner(request.user, 'customer.edit_type')
    if not can_edit:
        messages.error(request, 'No access')
        return redirect('errorpage')

    pass


@login_required
def type_delete(request, type_pk):
    if not Type.objects.filter(pk=type_pk):
        messages.error(request, 'type not found')
        return redirect('errorpage')
    type = Type.objects.get(pk=type_pk)
    can_delete = funcs.has_perm_or_is_owner(request.user, 'customer.delete_type', type)
    if not can_delete:
        messages.error(request, 'No access')
        return redirect('errorpage')
    type.delete()
    return redirect('type_index')

