from django.db.models import Sum, F, FloatField, Avg, Count, Q
from django_jalali.db import models as jmodels
import base64

from django import template

from django.contrib.auth import get_user_model
User = get_user_model()
from req_track.models import ReqEntered
from request.models import Requests, Xpref, ReqSpec, PrefSpec, Payment, Comment

register = template.Library()


@register.simple_tag()
def reqs_to_follow(user, on):
    # req = Requests.objects.filter(is_active=True, owner=user, to_follow=True, on=on).order_by('date_modified').reverse()
    req = Requests.objects.filter(is_active=True, owner=user, to_follow=True).order_by('date_modified').reverse()
    return req


@register.simple_tag()
def reqs_to_entered(user):
    reqs = ReqEntered.objects.filter(is_entered=False, is_request=True)
    if not user.is_superuser:
        reqs = reqs.filter(owner_text__contains=user)
    return reqs


@register.simple_tag()
def reqs_noxp(user):
    reqs = Requests.objects.filter(is_active=True, xpref__isnull=True).order_by('date_fa').reverse()
    if not user.is_superuser:
        reqs = reqs.filter(owner=user)
    return reqs


@register.simple_tag()
def reqs_no_xp(user):
    reqs = Requests.objects.filter(finished=False, xpref__isnull=True).order_by('date_fa').reverse()
    if not user.is_superuser:
        reqs = reqs.filter(owner=user)
    return reqs


@register.simple_tag()
def unread_comments(status, user):
    filter_query = Q(req_comment__owner=user, req_comment__is_active=True) | \
                   Q(req_comment__colleagues=user, req_comment__is_active=True) | \
                   Q(xpref_comment__owner=user, xpref_comment__is_active=True)

    comments = Comment.objects.filter(is_read=status).filter(filter_query).exclude(author=user).distinct().order_by('pub_date').reverse()
    return comments


@register.simple_tag()
def expert_remaining_reqs_not_entered(pk):
    account = User.objects.get(pk=pk)
    print(account)
    reqs = ReqEntered.objects.filter(owner_text__contains=account.last_name, is_request=True, is_entered=False)
    if account.last_name == 'فروغی':
        reqs = reqs.exclude(owner_text__contains='ظریف')
    return reqs.count()


@register.simple_tag()
def expert_remaining_reqs_no_xp(pk):
    account = User.objects.get(pk=pk)
    reqs = Requests.objects.filter(is_active=True, owner=account, xpref__isnull=True)
    return reqs.count()


@register.simple_tag()
def all_expert_reqs(pk):
    account = User.objects.get(pk=pk)
    reqs = Requests.objects.filter(is_active=True, owner=account)
    return reqs.count()


@register.simple_tag()
def expert_reqs_percent(account):
    reqs = Requests.objects.filter(is_active=True, owner=account)
    all_reqs = Requests.objects.filter(is_active=True)
    return 100 * reqs.count() / all_reqs.count()
