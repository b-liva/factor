import requests
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import (Customer,
                     Address,
                     )
from .models import Type
from request.models import Requests
from request.models import Xpref
from request.models import PrefSpec
from request.models import Payment
from request import views2
from django.contrib import messages
from customer import forms
# import reportlab
import jdatetime


import request.templatetags.functions as funcs
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
        reqs = Requests.objects.filter(is_active=True).filter(customer=customer)
        print('customer name: ' + customer.name)
        for req in reqs:
            print('     req No. ' + str(req.number))
            xprefs = Xpref.objects.filter(is_active=True).filter(req_id=req)

            for xpref in xprefs:
                print('         prefactor number ' + str(xpref.number))
                specs = PrefSpec.objects.filter(xpref_id=xpref)
                payments = Payment.objects.filter(is_active=True).filter(xpref_id=xpref)
                for payment in payments:
                    print('             payment: ' + str(payment.amount))
                x += 1
    print('total orders ' + str(x))

    return render(request, 'customer/read.html')


@login_required
def customer_form(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'customer.add_customer')
    if not can_add:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

    customer_types = Type.objects.all()
    customer_form = forms.CustomerForm()
    return render(request, 'customer/customer.html', {
        'customer_types': customer_types,
        'c_form': customer_form
    })


@login_required
def cform(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'customer.add_customer')
    if not can_add:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')

    if request.method == 'POST':
        customer_form = forms.CustomerForm(request.POST)

        if customer_form.is_valid():
            customer_item = customer_form.save(commit=False)
            customer_item.owner = request.user
            customer_item.save()
            return redirect('customer_index')
    else:
        customer_form = forms.CustomerForm()
        # customer_form.owner = request.user
    return render(request, 'customer2/customer_form.html', {'form': customer_form})


@login_required
def customer_insert(request):
    can_add = funcs.has_perm_or_is_owner(request.user, 'customer.add_customer')
    if not can_add:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')
    # print('001')
    # form = forms.CustomerForm(request.POST)
    # if form.is_valid():
    #     print('form is valid')
    #     form.save(commit=True)
    #     return customer_index(request)
    # print('002')

    name = request.POST['name']
    code = request.POST['code']
    # if not name or not code:
    #     messages.error(request, 'required field')
    #     return redirect('customer_form')
    #
    customer = Customer.objects.filter(code=code)
    if customer:
        messages.error(request, 'customer code already existing')
        return redirect('customer_form')
    all_customers = Customer.objects.all()
    customer_types = Type.objects.all()
    # customer_type = Type.objects.get(pk=request.POST['type'])
    customer_to_insert = Customer()
    # customer_to_insert.name = name
    # customer_to_insert.code = code
    # if request.POST['pub_date']:
    #     customer_to_insert.pub_date = request.POST['pub_date']
    # customer_to_insert.date2 = request.POST['date2']
    # customer_to_insert.type = customer_type
    customer_to_insert.owner = request.user
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

    customers = Customer.objects.filter(agent=False)
    context = {
        'customers': customers,
        'title': 'مشتریان',
    }
    return render(request, 'customer/index.html', context)


@login_required
def repr_index(request):
    can_index = funcs.has_perm_or_is_owner(request.user, 'customer.index_customer')
    if not can_index:
        messages.error(request, 'No access to see list of customers')
        return redirect('errorpage')

    customers = Customer.objects.filter(agent=True)
    context = {
        'customers': customers,
        'title': 'نمایندگان',
    }
    return render(request, 'customer/index.html', context)


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
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')
    customer_reqs = customer.requests_set.all().order_by('date_fa').reverse()
    kwList = []
    pList = []
    totalRes = {}
    tempDict = {}
    proformaDict = {}
    for customer_req in customer_reqs:
        tempDict = {}
        tempDict['kw'] = views2.total_kw(customer_req.pk)
        kwList.append(tempDict['kw'])
        req_profs = customer_req.xpref_set.filter(is_active=True)
        paymentList = []
        for p in req_profs:
            proformaDict = {}
            pList.append(p)
            payments = p.payment_set.filter(is_active=True)
            print(f'payments is: {payments}')
            for pmnt in payments:
                paymentList.append(pmnt)
            proformaDict['payments'] = paymentList

        print(f'***payment list is: {paymentList}')

        proformaDict['proformas'] = req_profs
        reqspec = customer_req.reqspec_set.all()
        tempDict['profs'] = req_profs
        tempDict['profs2'] = proformaDict
        tempDict['specs'] = reqspec
        tempDict['req'] = customer_req
        totalRes[customer_req.pk] = tempDict

        # reqId->
        #         profs->
        #                 payments->
        #         specs->
        #         kw->
        #         req->
    totalpaymenst = customer.payment_set.all()
    print(f'total result: {totalRes}')
    payList = []
    for pay in totalpaymenst:
        payList.append(pay.amount)

    paySum = sum(payList)
    payment_list, payment_sum = customers_payment(customer.pk)
    request_count = customer.requests_set.count()
    context = {
        'customer': customer,
        'customer_reqs': customer_reqs,
        # 'kw': kw,
        # 'some': some,
        'customer_kw_total': sum(kwList),
        'payment_list': payment_list,
        'payment_sum': payment_sum,
        'totalRes': totalRes,
        'pay_sum': paySum,
        'req_count': request_count
    }
    return render(request, 'customer/details.html', context)


@login_required
def customer_edit(request, customer_pk):
    if not Customer.objects.filter(pk=customer_pk):
        messages.error(request, 'No such Customer')
        return redirect('errorpage')

    customer_instance = Customer.objects.get(pk=customer_pk)
    can_edit = funcs.has_perm_or_is_owner(request.user, 'customer.edit_customer', customer_instance)
    if not can_edit:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')
    pass


@login_required
def customer_delete(request, customer_pk):
    if not Customer.objects.filter(pk=customer_pk):
        messages.error(request, 'No such Customer')
        return redirect('errorpage')
    customer_instance = Customer.objects.get(pk=customer_pk)
    c_name = customer_instance.name
    can_delete = funcs.has_perm_or_is_owner(request.user, 'customer.delete_customer', customer_instance)
    if not can_delete:
        messages.error(request, 'عدم دسترسی کافی')
        return redirect('errorpage')
    if request.method == 'GET':
        context = {
            'id': customer_instance.pk,
            'fn': 'customer_del',
        }
        return render(request, 'general/confirmation_page.html', context)
    elif request.method == 'POST':
        customer_instance.delete()
    msg = c_name + ' removed successfully!'
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


@login_required
def customer_edit_form(request, customer_pk):
    if not Customer.objects.filter(pk=customer_pk):
        messages.error(request, 'No such Customer')
        return redirect('errorpage')

    customer_instance = Customer.objects.get(pk=customer_pk)
    if customer_instance.date2:
        customer_instance.date2 = customer_instance.date2.togregorian()
    can_edit = funcs.has_perm_or_is_owner(request.user, 'customer.change_customer', customer_instance)
    if not can_edit:
        messages.error(request, 'No access')
        return redirect('errorpage')

    form = forms.CustomerForm(request.POST or None, instance=customer_instance)

    if form.is_valid():
        form.save()
        return redirect('customer_index')
    return render(request, 'customer2/customer_form.html', {
        'form': form,
    })


def customers_payment(customer_pk):
    customer = Customer.objects.get(pk=customer_pk)
    payments = customer.payment_set.all()
    priceList = []
    for p in payments:
        priceList.append(p.amount)
    total_payments = sum(priceList)
    return (priceList, total_payments)


def add_address(request, customer_pk):
    c = Customer.objects.get(pk=customer_pk)
    if request.method == 'POST':
        addr_form = forms.AddressForm(request.POST)

        if addr_form.is_valid():
            addr_item = addr_form.save(commit=False)
            addr_item.customer = c
            addr_item.save()
            return redirect('customer_index')
    else:
        addr_form = forms.AddressForm()
        # customer_form.owner = request.user
    context = {
        'form': addr_form,
        'customer': c,
    }
    return render(request, 'customer2/addAddress.html', context)


def addr_list(request, customer_pk):
    c = Customer.objects.get(pk=customer_pk)
    addrs = c.address_set.all()
    addrs_dict = {}
    for a in addrs:
        phoneList = []
        phones = a.phone_set.all()
        for p in phones:
            phoneList.append(p.phone_number)
        addrs_dict[a.pk] = phoneList
    print(addrs_dict)

    context = {
        'customer': c,
        'addresses': addrs
    }

    return render(request, 'customer2/addrList.html', context)


def add_phone(request, customer_pk, addr_pk):
    c = Customer.objects.get(pk=customer_pk)
    address = Address.objects.get(pk=addr_pk)
    if request.method == "POST":
        form = forms.PhoneForm(request.POST or None)
        if form.is_valid():
            phone_item = form.save(commit=False)
            phone_item.add = address
            phone_item.save()
            return redirect('addr-list', customer_pk=c.pk)
    else:
        form = forms.PhoneForm()
    context = {
        'form': form,
        address: address,
    }
    return render(request, 'customer2/addPhone.html', context)


def autocomplete(request):
    # lookup = lookup.encode('utf-8')
    # lookup = requests.utils.quote(request.GET['query'])
    lookup = str(request.GET['query'])
    list = {}
    print(f'request: {lookup}')
    customers = Customer.objects.filter(name__contains=lookup)
    print(customers)
    list2 = []
    list3 = {}
    for c in customers:
        list = {
            'data': c.pk,
            'value': c.name
        }
        list2.append(list)
    list3['suggestions'] = list2
    print(list2)
    print(f'list3: {list3}')
    return JsonResponse(list3, safe=False)
    # return HttpResponse(list2)
