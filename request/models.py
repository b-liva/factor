import os.path
from os.path import split

# from django.contrib.auth.models import User
from accounts.models import User
from django.db import models
import datetime
from django.utils.timezone import now
from customer.models import Customer
from django_jalali.db import models as jmodels


def upload_location(instance, filename):
    id = 'first'
    no = 'number'
    if instance._meta.model_name == 'requestfiles':
        id = instance.req_id
        no = instance.req.number
    if instance._meta.model_name == 'proffiles':
        id = instance.prof.id
        no = instance.prof.number
    if instance._meta.model_name == 'paymentfiles':
        id = instance.pay.id
        no = instance.pay.number
    print(f'model name: {instance._meta.model_name}')
    return '%s/id%s_No%s/%s' % (instance._meta.model_name, id, no, filename)


project_type = (
    (0, 'Routine'),
    (1, 'Project'),
    (2, 'Services'),
    (3, 'Ex'),
)


class ProjectType(models.Model):
    title = models.CharField(max_length=20)
    summary = models.TextField(max_length=600)

    def __str__(self):
        return '%s' % self.title


class Requests(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    # number = models.CharField(unique=True, max_length=10)
    number = models.IntegerField(unique=True)
    temp_number = models.IntegerField(unique=True, null=True, blank=True)
    parent_number = models.IntegerField(null=True, blank=True)
    pub_date = models.DateTimeField(default=now)
    date_fa = jmodels.jDateField(default=now)
    date_finished = jmodels.jDateField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='req_owner')
    colleagues = models.ManyToManyField(User, blank=True, null=True)
    summary = models.TextField(max_length=1000, null=True, blank=True)
    added_by_customer = models.BooleanField(default=False)
    edited_by_customer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.number

    class Meta:
        permissions = (
            ('index_requests', 'can see list of requests'),
            ('read_requests', 'can read requests'),
            ('public_requests', 'public in requests'),
            ('sale_expert', 'can edit own stuff'),
        )

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')


class RequestFiles(models.Model):
    image = models.FileField(upload_to=upload_location, null=True, blank=True)
    req = models.ForeignKey(Requests, on_delete=models.CASCADE)


class FrameSize(models.Model):
    size = models.CharField(max_length=10)

    def __str__(self):
        return '%s' % self.size


class ReqSpec(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    req_id = models.ForeignKey(Requests, on_delete=models.DO_NOTHING)
    qty = models.IntegerField(default=1)
    # type = models.IntegerField(choices=project_type, default=0)
    type = models.ForeignKey(ProjectType, on_delete=models.DO_NOTHING)
    # probably this price should be removed.
    # price = models.FloatField(null=True, blank=True)
    kw = models.FloatField()
    rpm = models.IntegerField()
    voltage = models.IntegerField(default=380)
    ip = models.IntegerField(null=True, blank=True)
    ic = models.IntegerField(null=True, blank=True)
    # frame_size = models.CharField(null=True, blank=True, max_length=10)
    frame_size = models.ForeignKey(FrameSize, on_delete=models.DO_NOTHING, blank=True, null=True)
    # images = models.FileField(upload_to='specs/', blank=True, null=True)
    summary = models.TextField(max_length=500, blank=True, null=True)
    tech = models.BooleanField(default=False)
    price = models.BooleanField(default=False)
    permission = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    cancelled = models.BooleanField(default=False)

    class Meta:
        permissions = (
            ('index_reqspecs', 'can see list of request Specs'),
            ('read_reqspecs', 'can read request Specs'),
        )

    def __str__(self):
        return '%s - %skw' % (self.qty, self.kw)


class Xpref(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    req_id = models.ForeignKey(Requests, on_delete=models.DO_NOTHING)
    number = models.IntegerField(unique=True)
    temp_number = models.IntegerField(unique=True, null=True, blank=True)
    pub_date = models.DateTimeField(default=now)
    date_fa = jmodels.jDateField(default=now)
    exp_date_fa = jmodels.jDateField(default=now)
    # image = models.ImageField(upload_to=upload_location, blank=True, null=True)
    summary = models.TextField(max_length=600, null=True, blank=True)
    verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')

    def __str__(self):
        return '%s' % self.number

    class Meta:
        permissions = (
            ('index_proforma', 'Can index Proforma'),
            ('read_proforma', 'Can read Proforma'),
        )


class ProfFiles(models.Model):
    image = models.FileField(upload_to=upload_location, null=True, blank=True)
    prof = models.ForeignKey(Xpref, on_delete=models.CASCADE)


class PrefSpec(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    xpref_id = models.ForeignKey(Xpref, on_delete=models.DO_NOTHING)
    qty = models.IntegerField(default=1)
    type = models.TextField(default=1)
    price = models.FloatField(null=True, blank=True)
    kw = models.FloatField()
    rpm = models.IntegerField()
    voltage = models.IntegerField(default=380)
    ip = models.IntegerField(null=True, blank=True)
    ic = models.IntegerField(null=True, blank=True)
    summary = models.TextField(max_length=500, blank=True, null=True)
    considerations = models.TextField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return 'pk:%s | %s | %sKW - %sRPM - %sV' % (self.pk, self.qty, self.kw, self.rpm, self.voltage)


class XprefVerf(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    xpref = models.ForeignKey(Xpref, on_delete=models.CASCADE)
    number = models.IntegerField(blank=True, null=True)
    pub_date = models.DateTimeField(default=now)
    image = models.ImageField(upload_to='verifications/')
    summary = models.TextField(max_length=1000)

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')


class Prefactor(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    request_id = models.ForeignKey(Requests, on_delete=models.CASCADE)
    number = models.IntegerField(unique=True)
    pub_date = models.DateTimeField(default=now)
    image = models.ImageField(upload_to='prefactors')
    summary = models.TextField(max_length=1000)

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')


class PrefactorVerification(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    pref_id = models.ForeignKey(Prefactor, on_delete=models.CASCADE)
    number = models.IntegerField()
    pub_date = models.DateTimeField(default=now)
    image = models.ImageField(upload_to='pref_verifications')
    summary = models.TextField(max_length=1000)

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')


class Permission(models.Model):
    proforma = models.ForeignKey(Xpref, on_delete=models.CASCADE)
    number = models.IntegerField()
    pub_date = models.DateTimeField(default=now)
    summary = models.TextField(max_length=1000)

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')


class Payment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    xpref_id = models.ForeignKey(Xpref, on_delete=models.DO_NOTHING)
    number = models.IntegerField(unique=True)
    temp_number = models.IntegerField(unique=True, null=True, blank=True)
    amount = models.FloatField()
    payment_date = models.DateTimeField(default=now)
    date_fa = jmodels.jDateField(default=now)
    summary = models.TextField(max_length=600, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def pub_date_pretty(self):
        return self.payment_date.strftime('%b %e %Y')

    def __str__(self):
        return '#%s and $%s ' % (self.number, self.amount)

    class Meta:
        permissions = (
            ('read_payment', 'Can read payment details'),
            ('index_payment', 'Can see list of payments'),
        )


class PaymentFiles(models.Model):
    image = models.FileField(upload_to=upload_location, null=True, blank=True)
    pay = models.ForeignKey(Payment, on_delete=models.CASCADE)

