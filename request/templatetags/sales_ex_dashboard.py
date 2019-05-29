from django.db.models import Sum, F, FloatField, Avg, Count, Q
from django_jalali.db import models as jmodels
import base64

from django import template

from accounts.models import User
from req_track.models import ReqEntered
from request.models import Requests, Xpref, ReqSpec, PrefSpec, Payment, Comment

register = template.Library()


@register.simple_tag()
def reqs_to_follow(request, on):
    req = Requests.objects.filter(is_active=True, to_follow=True, on=on).order_by('date_modified').reverse()
    return req


@register.simple_tag()
def reqs_to_entered(pk):
    user = User.objects.get(pk=pk)
    reqs = ReqEntered.objects.filter(is_entered=False, is_request=True, owner_text__contains=user)
    return reqs


@register.simple_tag()
def unread_comments(status, user):
    comments = Comment.objects.filter(is_read=status).exclude(author=user).order_by('pub_date').reverse()
    return comments
