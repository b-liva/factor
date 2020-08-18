from django.contrib import messages
import request.templatetags.functions as funcs
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import json
from .models import PriceDb
from .models import MotorDB
# Create your views here.


@login_required
def pricedb_form(request):

    can_index = funcs.has_perm_or_is_owner(request.user, 'pricedb.add_pricedb')
    if not can_index:
        messages.error(request, 'عدم دسترسی کافی!')
        return redirect('errorpage')
    price_set = PriceDb()
    price_set.title = request.POST['title']
    price_set.summary = request.POST['summary']
    price_set.save()
    db_kw = [
        5.5,
        7.5,
        11,
        15,
        18.5,
        22,
        30,
        37,
        45,
        55,
        75,
        90,
        110,
        132,
        160,
        200,
        220,
        250,
        315,
        355,
        400,
        450,
        ]
    db_speed = [1000, 1500, 3000]
    motor_pks = {}
    for kw in db_kw:
        pk_list = []
        for speed in db_speed:
            motor = MotorDB()
            motor.kw = kw
            motor.speed = speed
            motor.price_set = price_set
            motor.save()
            pk_list.append(motor.pk)
        motor_pks[kw] = pk_list
    print(motor_pks)
    # for kw, pks in motor_pks.items():
    #     print(kw)
    #     print(pks)
    # print(motor_pks)
    return render(request, 'pricedb/form.html', {
        'motor_pks': motor_pks,
        'db_kw': db_kw,
        'db_speed': db_speed,
    })


@login_required
def pricedb_insert(request):

    can_index = funcs.has_perm_or_is_owner(request.user, 'pricedb.add_pricedb')
    if not can_index:
        messages.error(request, 'عدم دسترسی کافی!')
        return redirect('errorpage')
    kv = {}
    for key in request.POST.keys():
        if key.startswith('pk_'):
            a = key.split('_')
            kv[a[1]] = request.POST[key]
    # print(kv)
    for pk in kv:
        motor = MotorDB.objects.get(pk=pk)
        if not kv[pk]:
            kv[pk] = 0
        motor.prime_cost = kv[pk]
        motor.save()
    return redirect('pricedb_index')


@login_required
def pricedb_index(request):
    can_index = funcs.has_perm_or_is_owner(request.user, 'pricedb.index_pricedb')
    if not can_index:
        messages.error(request, 'عدم دسترسی کافی!')
        return redirect('errorpage')

    price_set = PriceDb.objects.all()
    return render(request, 'pricedb/index.html', {'price_set': price_set})


@login_required
def pricedb_find(request):
    pass


@login_required
def pricedb_details(request, pricedb_pk):

    can_index = funcs.has_perm_or_is_owner(request.user, 'pricedb.index_pricedb')
    if not can_index:
        messages.error(request, 'عدم دسترسی کافی!')
        return redirect('errorpage')
    db_kw = [
        5.5,
        7.5,
        11,
        15,
        18.5,
        22,
        30,
        37,
        45,
        55,
        75,
        90,
        110,
        132,
        160,
        200,
        220,
        250,
        315,
        355,
        400,
        450,
    ]
    db_speed = [1000, 1500, 3000]
    priceset = PriceDb.objects.get(pk=pricedb_pk)
    prices = priceset.motordb_set.all().order_by('pk')
    # print(prices)
    list = []
    for pr in prices:
        list.append(pr.prime_cost)
    final = {}
    count = 0
    for kw in db_kw:
        price_list = []
        for speed in db_speed:
            price_list.append(list[count])
            count += 1
        final[kw] = price_list
    print(final)
    return render(request, 'pricedb/details.html', {
        'price_list': final,
        'price_set': priceset,
    })


@login_required
def pricedb_delete(request, pricedb_pk):

    can_index = funcs.has_perm_or_is_owner(request.user, 'pricedb.delete_pricedb')
    if not can_index:
        messages.error(request, 'عدم دسترسی کافی!')
        return redirect('errorpage')
    price_set = PriceDb.objects.get(pk=pricedb_pk)
    price_set.delete()
    return redirect('pricedb_index')


@login_required
def pricedb_edit(request, pricedb_pk):

    can_index = funcs.has_perm_or_is_owner(request.user, 'pricedb.edit_pricedb')
    if not can_index:
        messages.error(request, 'عدم دسترسی کافی!')
        return redirect('errorpage')
    price_set = PriceDb.objects.get(pk=pricedb_pk)
    pass


@login_required
def pricedb_clean(request):

    can_index = funcs.has_perm_or_is_owner(request.user, 'pricedb.delete_pricedb')
    if not can_index:
        messages.error(request, 'عدم دسترسی کافی!')
        return redirect('errorpage')

    motors = MotorDB.objects.all()
    for motor in motors:
        tf = motor.prime_cost or motor.base_price or motor.sale_price
        if not tf:
            motor.delete()
    return redirect('pricedb_index')

