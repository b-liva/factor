from django.db.models import Sum, F, FloatField, Count
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    AbstractBaseUser,
    Permission,
    Group,
    BaseUserManager,
    PermissionsMixin,
)

# from customer.models import Customer
# Create your models here.
from request.models import Xpref, PrefSpec, Payment


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    sales_exp = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.last_name

    def get_absolute_url(self):
        return reverse('account-details', args=[self.pk])

    def perms(self, *args, **kwargs):
        perms = Xpref.objects.filter(is_active=True, req_id__is_active=True, perm=True, req_id__owner=self)
        ps = PrefSpec.objects.filter(is_active=True, xpref_id__is_active=True, xpref_id__req_id__is_active=True,
                                     xpref_id__perm=True, price__gt=0, qty__gt=0, xpref_id__req_id__owner=self)

        # if 'date_min' in kwargs:
        if 'date_min' in kwargs and kwargs['date_min'] != '':
            perms = perms.filter(perm_date__gte=kwargs['date_min'])
            ps = ps.filter(xpref_id__perm_date__gte=kwargs['date_min'])
        if 'date_max' in kwargs and kwargs['date_max'] != '':
            perms = perms.filter(perm_date__lte=kwargs['date_max'])
            ps = ps.filter(xpref_id__perm_date__lte=kwargs['date_max'])
        count = perms.count()
        ps_count = ps.values('xpref_id').distinct().aggregate(count=Count('xpref_id'))
        ps_qty = ps.aggregate(sum=Sum('qty'))
        print(self, ps_qty['sum'])
        print(self, ps_count)

        return {
            'perms': perms,
            'count': count,
            'ps_qty': ps_qty,
            'ps_count': ps_count,
        }

    def perms_price_total(self, *args, **kwargs):
        # prefs = PrefSpec.objects.filter(
        #     xpref_id__req_id__is_active=True,
        #     xpref_id__is_active=True,
        #     xpref_id__perm=True,
        #     xpref_id__req_id__owner=self
        # )
        prefs = PrefSpec.objects.filter(
            is_active=True, xpref_id__is_active=True, xpref_id__req_id__is_active=True,
            xpref_id__perm=True, price__gt=0, qty__gt=0, xpref_id__req_id__owner=self
        )
        if kwargs['date_min']:
            # prefs = prefs.filter(xpref_id__req_id__date_fa__gte=kwargs['date_min'])
            prefs = prefs.filter(xpref_id__perm_date__gte=kwargs['date_min'])
        if kwargs['date_max']:
            # prefs = prefs.filter(xpref_id__req_id__date_fa__lte=kwargs['date_max'])
            prefs = prefs.filter(xpref_id__perm_date__lte=kwargs['date_max'])
        price = prefs.aggregate(sum=Sum(1.09 * F('qty') * F('price'), output_field=FloatField()))
        kw = prefs.aggregate(sum=Sum(F('qty') * F('kw'), output_field=FloatField()))
        return {
            'price': price,
            'kw': kw,
        }

    def perms_total_received(self, *args, **kwargs):
        if 'date_min' not in kwargs:
            kwargs['date_min'] = ''
        if 'date_max' not in kwargs:
            kwargs['date_max'] = ''
        perms = self.perms(date_min=kwargs['date_min'], date_max=kwargs['date_max'])['perms']
        perm_numbers_list = [a.number for a in perms]
        pays = Payment.objects.filter(xpref_id__number__in=perm_numbers_list)
        total_received = pays.aggregate(sum=Sum('amount'))
        return total_received['sum']


class CustomerUser(User):
    is_active_customer = models.BooleanField(default=True)
    is_repr = models.BooleanField(default=True)
    # customer = models.OneToOneField(Customer, on_delete=models.DO_NOTHING)

    def __str__(self):
        return '%s' % self.last_name


class StaffPosition(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return "%s" % self.title


class StaffInfo(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.ManyToManyField('accounts.StaffPosition', null=True, blank=True)
    tel = models.CharField(max_length=4)

    def __str__(self):
        return "%s (%s) tel: %s" % (self.account.last_name, self.position.last().title, self.tel,)

# class EmailUserManager(BaseUserManager):
#
#     def create_user(self, email, password=None, **extra_fields):
#         """Create and saves a new user by email and password"""
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self.db)
#
#         return user


# class EmailUser(AbstractBaseUser, PermissionsMixin):
#     """Custom user model that supports email instead of username"""
#     email = models.EmailField(max_length=255, unique=True)
#     name = models.CharField(max_length=255)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#
#     objects = EmailUserManager()
#
#     USERNAME_FIELD = 'email'
