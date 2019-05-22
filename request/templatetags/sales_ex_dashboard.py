from django.db.models import Sum, F, FloatField, Avg, Count, Q
from django_jalali.db import models as jmodels
import base64

from django import template

from req_track.models import ReqEntered
from request.models import Requests, Xpref, ReqSpec, PrefSpec, Payment

register = template.Library()


@register.simple_tag()
def reqs_to_follow(request, on):
    req = Requests.objects.filter(is_active=True, to_follow=True, on=on).order_by('date_modified').reverse()
    return req
