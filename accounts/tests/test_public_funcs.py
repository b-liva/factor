from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

from customer.models import Type, Customer
import datetime

from request.models import Requests

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
    if owner is None:
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
    )
    ex_user.groups.add(sale_expert_group)
    ex_user.super_user = True
    ex_user.save()
    return ex_user
