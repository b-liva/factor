from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.shortcuts import get_object_or_404
from customer.models import Type, Customer
import datetime

from request.models import Requests, ReqSpec, ProjectType, RpmType, Xpref, PrefSpec, Payment

User = get_user_model()


def sample_user(username='testuser', password='testpass123'):
    """Create a sample user"""
    return User.objects.create_user(username, password)


def sample_superuser(username='superuser'):
    user = sample_user(username=username)
    user.is_superuser = True
    user.save()
    return user


def sample_customer_type(name='پتروشیمی'):
    """Create a sample customer type"""
    return Type.objects.create(name=name)


def sample_customer(owner=None, name='سازش', date2=datetime.datetime.now(), customer_type=None):
    if owner is None:
        owner = sample_user()
    if customer_type is None:
        customer_type = sample_customer_type()
    customer = Customer.objects.create(
        owner=owner,
        name=name,
        date2=date2,
        type=customer_type
    )
    return customer


def sample_request(owner=None, number=None, customer=None):
    if not owner:
        owner = sample_user()
    if customer is None:
        customer = sample_customer()
    req = Requests.objects.create(
        owner=owner,
        number=number,
        customer=customer
    )
    return req


def login_as_expert(username='expert_user'):
    ex_user = sample_user(username=username)
    sale_expert_group = Group.objects.create(name='sale_expert')
    sale_expert_group.permissions.add(
        Permission.objects.get(codename='add_customer', content_type__app_label='customer'),
        Permission.objects.get(codename='index_customer', content_type__app_label='customer'),
        Permission.objects.get(codename='read_customer', content_type__app_label='customer'),
        Permission.objects.get(codename='index_requests', content_type__app_label='request'),
        Permission.objects.get(codename='add_requests', content_type__app_label='request'),
        Permission.objects.get(codename='delete_requests', content_type__app_label='request'),
        Permission.objects.get(codename='change_requests', content_type__app_label='request'),
        Permission.objects.get(codename='add_reqspec', content_type__app_label='request'),
        Permission.objects.get(codename='index_reqspecs', content_type__app_label='request'),
        Permission.objects.get(codename='index_reqspec', content_type__app_label='request'),
        Permission.objects.get(codename='change_reqspec', content_type__app_label='request'),
        Permission.objects.get(codename='delete_reqspec', content_type__app_label='request'),
        Permission.objects.get(codename='read_reqspecs', content_type__app_label='request'),
        Permission.objects.get(codename='index_xpref', content_type__app_label='request'),
        Permission.objects.get(codename='add_xpref', content_type__app_label='request'),
        Permission.objects.get(codename='delete_xpref', content_type__app_label='request'),
        Permission.objects.get(codename='change_xpref', content_type__app_label='request'),
        Permission.objects.get(codename='index_prefspec', content_type__app_label='request'),
        Permission.objects.get(codename='add_prefspec', content_type__app_label='request'),
        Permission.objects.get(codename='delete_prefspec', content_type__app_label='request'),
        Permission.objects.get(codename='change_prefspec', content_type__app_label='request'),
        Permission.objects.get(codename='index_payment', content_type__app_label='request'),
        Permission.objects.get(codename='add_payment', content_type__app_label='request'),
        Permission.objects.get(codename='change_payment', content_type__app_label='request'),
        Permission.objects.get(codename='delete_payment', content_type__app_label='request'),
    )
    ex_user.groups.add(sale_expert_group)
    ex_user.super_user = True
    ex_user.save()
    return ex_user


def sample_reqspec(req, **params):
    defaults = {
        'type': ProjectType.objects.create(title='روتین'),
        'rpm_new': RpmType.objects.create(rpm=1500, pole=4),
        'qty': 2, 'kw': 132, 'rpm': 1500, 'voltage': 380,
    }
    defaults.update(params)

    return ReqSpec.objects.create(req_id=req, **defaults)


def sample_proforma(req, owner, number, **params):
    defaults = {}
    defaults.update(params)
    return Xpref.objects.create(req_id=req, owner=owner, number=number, **defaults)


def sample_prefspec(proforma, owner, reqspe, **params):

    defaults = {
        'kw': reqspe.kw,
        'rpm': reqspe.rpm,
    }
    defaults.update(params)
    return PrefSpec.objects.create(xpref_id=proforma, owner=owner, reqspec_eq=reqspe, **defaults)


def sample_income(proforma, owner, number, **params):
    defaults = {
        'amount': 1500000,
    }
    defaults.update(params)
    return Payment.objects.create(xpref_id=proforma, owner=owner, number=number, **defaults)
