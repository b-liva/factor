from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum, F, FloatField, Count
from django.urls import reverse
from django.utils.timezone import now
from django_jalali.db import models as jmodels
from django.contrib.auth import get_user_model
from request.models import Payment, Requests, ReqSpec, PrefSpec
User = get_user_model()


def default_customer_code():
    last_customer = Customer.objects.all().order_by('pk').last()
    last_id = 0
    if last_id:
        last_id = last_customer.pk
    customer = Customer.objects.filter(pk=last_id)
    while customer is not None:
        last_id += 1
        customer = Customer.objects.filter(code=last_id)
        if not customer:
            break
    return last_id


class Type(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return '%s' % self.name
# types = Type.objects.all()


class Customer(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='owner')
    code = models.IntegerField(unique=True, default=default_customer_code, blank=True)
    code_temp = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100)
    type = models.ForeignKey(Type, on_delete=models.DO_NOTHING)
    # type = models.(choices=types)
    pub_date = models.DateTimeField(default=now)
    # date2 = jmodels.jDateTimeField(default=now)
    date2 = jmodels.jDateField(default=now)
    phone = models.CharField(max_length=100, blank=True, null=True)
    fax = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(max_length=250, blank=True, null=True)
    postal_code = models.CharField(max_length=15, blank=True, null=True)
    addr = models.TextField(max_length=600, blank=True, null=True)
    agent = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    imported = models.BooleanField(default=False)

    class Meta:
        permissions = (
            ('read_customer', 'Can read a customer details'),
            ('index_customer', 'Can see list of customers'),
            ('index_requests', 'customer can see list of requests'),
        )

    def __str__(self):
        return '%s' % self.name

    def get_absolute_url(self):
        return reverse('customer_read', args=[self.pk])

    def total_receivable(self):
        items = self.spec_perms()['items']
        receivable = items.aggregate(sum=Sum(F('qty') * F('price'), output_field=FloatField()))
        receivable = 1.09 * receivable['sum'] if receivable['sum'] else 0
        return receivable

    def total_received(self):
        payments = Payment.objects.filter(xpref_id__req_id__customer=self.id, is_active=True)
        amount = payments.aggregate(sum=Sum('amount'))
        amount = amount['sum'] if amount['sum'] else 0
        context = {
            'payments': payments,
            'amount': amount
        }
        return context

    def permits(self):
        permits = PrefSpec.objects.filter(
            xpref_id__perm=True,
            price__gt=0,
            xpref_id__req_id__customer=self
        )
        return permits

    def sales_qty(self):
        permits = self.permits()
        qty = permits.aggregate(Sum('qty'))['qty__sum']
        return qty

    def sales_kw(self):
        permits = self.permits()
        kw = permits.aggregate(sum=Sum(F('qty') * F('kw'), output_field=FloatField()))['sum']
        return kw

    def sales_amount(self):
        permits = self.permits()
        amount = permits.aggregate(Sum('price'))['price__sum']
        return amount

    def perm_qty_delivered(self):
        sent = PrefSpec.objects.filter(xpref_id__req_id__customer=self, qty_sent__gt=0)
        sent_value = sent.aggregate(sum=Sum(F('price') * F('qty'), output_field=FloatField()))
        sent_value = 1.09 * sent_value['sum'] if sent_value['sum'] else 0
        sent_count = sent.aggregate(count=Sum('qty_sent'))
        sent_count = sent_count['count'] if sent_count['count'] else 0

        context = {
            'sent_count': sent_count,
            'sent_value': sent_value,

        }
        return context

    def perm_qty_not_delivered(self):
        pass

    def ballance(self):
        ballance_sent = self.total_received()['amount'] - self.perm_qty_delivered()['sent_value']
        ballance_total = self.total_received()['amount'] - self.total_receivable()
        ballance_sent = ballance_sent if ballance_sent else 0
        ballance_total = ballance_total if ballance_total else 0
        context = {
            'ballance_sent': ballance_sent,
            'ballance_total': ballance_total,
        }
        return context

    def total_kw(self):
        reqs = Requests.actives.filter(customer=self.id)
        count = reqs.count()
        amount = ReqSpec.objects.filter(req_id__is_active=True, req_id__customer=self).aggregate(sum=Sum(F('qty') * F('kw'), output_field=FloatField()))
        context = {
            'count': count,
            'amount': amount['sum'],
        }
        return context

    def spec_perms(self):
        items = PrefSpec.objects.filter(xpref_id__req_id__customer=self, xpref_id__perm=True)
        qty = items.aggregate(sum=Sum('qty'))
        qty = qty['sum'] if qty['sum'] else 0
        context = {
            'items': items,
            'qty': qty
        }
        return context


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    fax = models.IntegerField(blank=True, null=True)
    postal_code = models.IntegerField(blank=True, null=True)
    address = models.TextField(max_length=600, blank=True, null=True)


class Phone(models.Model):
    add = models.ForeignKey(Address, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)

