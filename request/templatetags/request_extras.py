from django_jalali.db import models as jmodels
import base64

from django import template
from request.models import Requests, Xpref, ReqSpec, PrefSpec

register = template.Library()


@register.filter(name='is_sent')
def is_sent(reqspec):
    sent = False
    pref_set = reqspec.prefspec_set.filter(xpref_id__is_active=True)
    # print(f"pref specs: {pref_set}")
    for p in pref_set:
        print(f"pref: {p}")
        if p.sent:
            sent = True
    return sent


@register.filter(name='has_price')
def has_price(reqspec):
    price = False
    pref_set = reqspec.prefspec_set.filter(xpref_id__is_active=True).order_by('xpref_id__date_fa', 'pk').reverse()

    if len(pref_set):
        for p in pref_set:
            if p.price > 0:
                price = True


    # if len(pref_set):
    #     if len(pref_set) > 1:
    #         """
    #             here we should find the valid price
    #             """
    #         for p in pref_set:
    #             if p.price > 0:
    #                 price = True
    #     else:
    #         if pref_set[0].price > 0:
    #             price = True

    # if len(pref_set) > 1:
    #     pass
    # elif len(pref_set) == 0:
    #     if pref_set[0].price > 0:
    #         price = True
    # else:
    #     pass
    return price


@register.filter(name='is_cancelled')
def is_cancelled(reqspec):
    cancelled = False
    pref_set = reqspec.prefspec_set.all()
    return cancelled


@register.filter(name='has_permission')
def has_permission(reqspec):
    perm = False
    pref_set = reqspec.prefspec_set.filter(xpref_id__is_active=True).order_by('xpref_id__date_fa', 'pk').reverse()
    if len(pref_set):
        for p in pref_set:
            if p.xpref_id.perm:
                perm = True
    return perm


@register.filter(name='enc')
def enc(reqspec_pk):
    v = str(reqspec_pk)
    value = base64.b64encode(v.encode("utf-8"))
    return value


@register.filter(name='perm_warning_class')
def perm_warning_class(perm):
    today_fa = jmodels.jdatetime.date.today()
    diff = perm['perm'].due_date - today_fa
    warning_class = ""

    if diff.days <= 0:
        warning_class = 'btn-danger'

    if diff.days > 0:
        warning_class = 'btn-warning'

    if diff.days > 31:
        warning_class = 'btn-success'

    return warning_class


@register.filter(name='days')
def days(perm):
    today_fa = jmodels.jdatetime.date.today()
    diff = perm['perm'].due_date - today_fa

    return diff.days
