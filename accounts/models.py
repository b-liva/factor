from django.db.models import Sum, F, FloatField
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
# from customer.models import Customer
# Create your models here.
from request.models import Xpref, PrefSpec


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    sales_exp = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.last_name

    def get_absolute_url(self):
        return reverse('account-details', args=[self.pk])

    def perms(self, *args, **kwargs):
        print(kwargs)
        perms = Xpref.objects.filter(is_active=True, req_id__is_active=True, perm=True, req_id__owner=self)
        if kwargs['date_min']:
            perms = perms.filter(req_id__date_fa__gte=kwargs['date_min'])
        if kwargs['date_max']:
            perms = perms.filter(req_id__date_fa__lte=kwargs['date_max'])
        count = perms.count()
        return {
            'perms': perms,
            'count': count,
        }

    def perms_price_total(self, *args, **kwargs):
        prefs = PrefSpec.objects.filter(
            xpref_id__req_id__is_active=True,
            xpref_id__is_active=True,
            xpref_id__perm=True,
            xpref_id__req_id__owner=self
        )
        if kwargs['date_min']:
            prefs = prefs.filter(xpref_id__req_id__date_fa__gte=kwargs['date_min'])
        if kwargs['date_max']:
            prefs = prefs.filter(xpref_id__req_id__date_fa__lte=kwargs['date_max'])
        price = prefs.aggregate(sum=Sum(1.09 * F('qty') * F('price'), output_field=FloatField()))
        kw = prefs.aggregate(sum=Sum(F('qty') * F('kw'), output_field=FloatField()))
        return {
            'price': price,
            'kw': kw,
        }


class CustomerUser(User):
    is_active_customer = models.BooleanField(default=True)
    is_repr = models.BooleanField(default=True)
    # customer = models.OneToOneField(Customer, on_delete=models.DO_NOTHING)

    def __str__(self):
        return '%s' % self.last_name



