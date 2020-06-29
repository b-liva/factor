import os.path
from os.path import split

# from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum, F, FloatField
from django.utils import timezone


from django.db import models
import datetime
import jdatetime
from django.utils.timezone import now
from django_jalali.db import models as jmodels


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides selfupdating ``created`` and ``modified`` fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


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


class Comment(models.Model):
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    date_fa = jmodels.jDateField(default=now)
    pub_date = models.DateTimeField(default=now)
    body = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return "%s: %s" % (self.author, self.body,)


class ProjectType(models.Model):
    title = models.CharField(max_length=20)
    summary = models.TextField(max_length=600)

    def __str__(self):
        return '%s' % self.title


class RpmType(models.Model):
    rpm = models.IntegerField()
    pole = models.IntegerField()

    def __str__(self):
        return '%s قطب %s دور' % (self.pole, self.rpm)


class IPType(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return '%s' % self.title


class ICType(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return '%s' % self.title


class IMType(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return '%s' % self.title


class IEType(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return '%s' % self.title


class ActiveRequestManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Requests(models.Model):
    customer = models.ForeignKey('customer.Customer', on_delete=models.DO_NOTHING)
    # owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='req_owner')
    owner = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING, related_name='req_owner')

    number = models.IntegerField(unique=True)
    temp_number = models.IntegerField(unique=True, null=True, blank=True)
    parent_number = models.IntegerField(null=True, blank=True)
    pub_date = models.DateTimeField(default=now)
    date_fa = jmodels.jDateField(default=now)
    date_fa_text = models.CharField(null=True, blank=True, max_length=20)
    date_finished = jmodels.jDateField(blank=True, null=True)
    colleagues = models.ManyToManyField('accounts.User', blank=True, null=True)
    summary = models.TextField(max_length=1000, null=True, blank=True)
    added_by_customer = models.BooleanField(default=False)
    edited_by_customer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    finished = models.BooleanField(default=False)

    date_modified = models.DateTimeField(null=True, blank=True)
    follow_up = models.TextField(blank=True, null=True)
    to_follow = models.BooleanField(default=False)
    on = models.BooleanField(default=False)
    comments = GenericRelation('Comment', related_query_name='req_comment')

    objects = models.Manager()
    actives = ActiveRequestManager()

    lookup_fields = ['customer_name__icontains', 'owner_last_name__icontains', 'number']

    def __str__(self):
        return '%s' % self.number

    def request_details(self):
        total_qty = self.reqspec_set.aggregate(Sum('qty'))
        kws = self.reqspec_set.values('kw')
        x = ''
        for i in list(kws):
            x += f"{i['kw']}, "

        return "%s دستگاه  %s کیلووات" % (total_qty['qty__sum'], x)

    class Meta:
        permissions = (
            ('index_requests', 'can see list of requests'),
            ('read_requests', 'can read requests'),
            ('public_requests', 'public in requests'),
            ('sale_expert', 'can edit own stuff'),
        )

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.date_modified = timezone.now()
        super(Requests, self).save()

    def total_kw(self):
        kw = self.reqspec_set.aggregate(sum=Sum(F('qty') * F('kw'), output_field=FloatField()))
        kw = kw['sum'] if kw['sum'] else 0
        return kw

    def proformas(self):
        all_proformas = self.xpref_set.filter(is_active=True)
        return all_proformas

    def total_received(self):
        amount = Payment.objects.filter(is_active=True, xpref_id__req_id=self).aggregate(sum=Sum('amount'))
        sum = amount['sum'] if amount['sum'] else 0
        return sum

    def total_receivable(self):
        amount = PrefSpec.objects.filter(xpref_id__is_active=True, xpref_id__req_id=self) \
            .aggregate(sum=Sum(F('qty') * F('price'), output_field=FloatField()))
        sum = amount['sum'] if amount['sum'] else 0
        return 1.09 * sum - self.total_received()

    def files(self):
        files = self.requestfiles_set.all()
        return files

    def files_by_type(self):
        files = self.files()
        images_suffix = ['jpg', 'jpeg', 'png', 'tiff']
        pdfs_suffix = ['pdf']
        docs_suffix = ['doc', 'docx', 'xls']
        images = []
        pdfs = []
        docs = []
        other = []
        for f in files:
            filename = str(f.image)
            filename = filename.split('.')[-1]
            # if str(f.image).lower().endswith('.jpg') or str(f.image).lower().endswith('.jpeg') or str(
            if filename in images_suffix:
                images.append(f)
            # elif str(f.image).lower().endswith('.pdf'):
            elif filename in pdfs_suffix:
                pdfs.append(f)

            # elif str(f.image).lower().endswith('.doc'):
            elif filename in docs_suffix:
                docs.append(f)
            else:
                other.append(f)
        context = {
            'images': images,
            'pdfs': pdfs,
            'docs': docs,
            'other': other
        }

        return context


class RequestFiles(models.Model):
    req = models.ForeignKey(Requests, on_delete=models.CASCADE)
    image = models.FileField(upload_to=upload_location, null=True, blank=True)

    def pretty_name(self):
        name = self.image.name.split('/')[-1]
        return name


class FrameSize(models.Model):
    size = models.CharField(max_length=10)

    def __str__(self):
        return '%s' % self.size


class ReqSpec(models.Model):
    code = models.BigIntegerField(default=99009900)
    req_id = models.ForeignKey(Requests, on_delete=models.CASCADE)
    owner = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING)
    type = models.ForeignKey(ProjectType, on_delete=models.DO_NOTHING)

    qty = models.IntegerField(default=1)
    kw = models.FloatField()
    rpm = models.IntegerField(null=True, blank=True)
    rpm_new = models.ForeignKey(RpmType, on_delete=models.DO_NOTHING)
    voltage = models.IntegerField(default=380)
    ip_type = models.IntegerField(null=True, blank=True)
    ic_type = models.IntegerField(null=True, blank=True)
    im = models.ForeignKey(IMType, on_delete=models.DO_NOTHING, blank=True, null=True)
    ip = models.ForeignKey(IPType, on_delete=models.DO_NOTHING, blank=True, null=True)
    ic = models.ForeignKey(ICType, on_delete=models.DO_NOTHING, blank=True, null=True)
    ie = models.ForeignKey(IEType, on_delete=models.DO_NOTHING, blank=True, null=True)
    frame_size = models.ForeignKey(FrameSize, on_delete=models.DO_NOTHING, blank=True, null=True)
    summary = models.TextField(max_length=500, blank=True, null=True)
    tech = models.BooleanField(default=False)
    price = models.BooleanField(default=False)
    permission = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    cancelled = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)

    class Meta:
        permissions = (
            ('index_reqspecs', 'can see list of request Specs'),
            ('index_reqspec', 'can see list of request Spec!'),
            ('read_reqspecs', 'can read request Specs'),
        )

    def __str__(self):
        return '%s - %skw' % (self.qty, self.kw)


class ReqRows(TimeStampedModel):
    req = models.ForeignKey(Requests, on_delete=models.CASCADE)
    owner = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING)
    code = models.BigIntegerField(default=55005500)
    title = models.CharField(max_length=150)
    qty = models.IntegerField(default=1)

    class Meta:
        abstract = True

    def __str__(self):
        return "%s عدد %s(%s)" % (self.qty, self.title, self.code)


class ReqPart(ReqRows):
    pass


class Wastage(ReqRows):
    pass


class Services(ReqRows):
    qty = models.FloatField(default=1)

    def __str__(self):
        return "%s نفر ساعت %s(%s)" % (self.qty, self.title, self.code)


class IssueType(models.Model):
    title = models.CharField(max_length=60)
    summary = models.TextField(max_length=600, null=True, blank=True)

    def __str__(self):
        return '%s' % self.title


class Xpref(models.Model):
    owner = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING)
    req_id = models.ForeignKey(Requests, on_delete=models.DO_NOTHING)
    number = models.IntegerField(unique=True)
    # number_auto = models.IntegerField(unique=True)
    number_td = models.IntegerField(null=True, blank=True)
    # temp_number = models.IntegerField(null=True, blank=True)
    pub_date = models.DateTimeField(default=now)
    date_fa = jmodels.jDateField(default=now)
    date_fa_text = models.CharField(null=True, blank=True, max_length=20)
    date_modified = models.DateTimeField(null=True, blank=True)
    exp_date_fa = jmodels.jDateField(default=now)
    perm_number = models.IntegerField(null=True, blank=True)
    perm_date = jmodels.jDateField(null=True, blank=True)
    due_date = jmodels.jDateField(null=True, blank=True)
    due_date_days = models.CharField(max_length=50, blank=True, null=True)
    summary = models.TextField(max_length=600, null=True, blank=True)
    verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    perm = models.BooleanField(default=False)
    follow_up = models.TextField(blank=True, null=True)
    to_follow = models.BooleanField(default=False)
    on = models.BooleanField(default=False)
    comments = GenericRelation('Comment', related_query_name='xpref_comment')
    issue_type = models.ForeignKey(IssueType, blank=True, null=True, on_delete=models.DO_NOTHING)
    signed = models.BooleanField(default=False)

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')

    def __str__(self):
        return '%s' % self.number

    def proforma_details(self):
        total_qty = self.prefspec_set.aggregate(Sum('qty'))
        kws = self.prefspec_set.values('kw')
        x = ''
        for i in list(kws):
            x += f"{i['kw']}, "

        return "%s دستگاه  %s کیلووات" % (total_qty['qty__sum'], x)

    def pretty_follow_up(self):
        return self.follow_up if self.follow_up is not None else ""

    def pretty_date_modified(self):
        return self.date_modified if self.date_modified is not None else ""

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.date_modified = timezone.now()
        super(Xpref, self).save()

    def total_proforma_price_vat(self):
        no_vat = self.prefspec_set.aggregate(sum=Sum(F('qty') * F('price'), output_field=FloatField()))
        no_vat = no_vat['sum']
        if no_vat is None:
            no_vat = 0
        vat = .09 * no_vat
        price_vat = no_vat + vat
        # return float(format(value, '.12g'))
        return {
            'no_vat': no_vat,
            'vat': vat,
            'price_vat': price_vat
        }

    def total_proforma_received(self):
        value = self.payment_set.filter(is_active=True).aggregate(sum=Sum('amount'))
        received = 0 if value['sum'] is None else value['sum']
        remaining = self.total_proforma_price_vat()['price_vat'] - received
        # Todo: Debug division by zero if total_proforma_price_vat()['price_vat'] == 0
        received_percent = 0
        remaining_percent = 0
        if self.total_proforma_price_vat()['price_vat']:
            received_percent = 100 * received / self.total_proforma_price_vat()['price_vat']
            remaining_percent = 100 * remaining / self.total_proforma_price_vat()['price_vat']
        status = True if remaining == 0 else False
        return {
            'received': received,
            'received_percent': received_percent,
            'remaining': remaining,
            'remaining_percent': remaining_percent,
            'status': status
        }

    def total_proforma_qty(self):
        return PrefSpec.objects.filter(xpref_id=self, price__gt=0).aggregate(sum=Sum('qty'))['sum']

    def total_proforma_qty_sent(self):
        return PrefSpec.objects.filter(xpref_id=self, price__gt=0).aggregate(sum=Sum('qty_sent'))['sum']

    def total_proforma_qty_remain(self):
        return self.total_proforma_qty() - self.total_proforma_qty_sent()

    class Meta:
        permissions = (
            ('index_proforma', 'Can index Proforma'),
            ('index_xpref', 'Can index Proformas'),
            ('read_proforma', 'Can read Proforma'),
        )


class ProformaFollowUP(models.Model):
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    xpref = models.ForeignKey(Xpref, on_delete=models.CASCADE)
    summary = models.CharField(max_length=100)
    description = models.TextField(null=True)
    pub_date = models.DateTimeField(default=now)
    date_fa = jmodels.jDateField(default=now)
    next_followup = jmodels.jDateField(null=True, blank=True)

    def __str__(self):
        return "%s(%s)" % (self.summary, self.date_fa,)


class ProfFiles(models.Model):
    prof = models.ForeignKey(Xpref, on_delete=models.CASCADE)
    image = models.FileField(upload_to=upload_location, null=True, blank=True)


class PrefSpec(models.Model):
    code = models.BigIntegerField(default=99009900)
    owner = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING)
    xpref_id = models.ForeignKey(Xpref, on_delete=models.CASCADE)
    reqspec_eq = models.ForeignKey(ReqSpec, on_delete=models.DO_NOTHING)

    qty = models.IntegerField(default=1)
    type = models.TextField(default=1)
    price = models.FloatField(null=True, blank=True)
    kw = models.FloatField()
    rpm = models.IntegerField()
    voltage = models.IntegerField(default=380)
    ip_type = models.IntegerField(null=True, blank=True)
    ic_type = models.IntegerField(null=True, blank=True)
    im = models.ForeignKey(IMType, on_delete=models.DO_NOTHING, blank=True, null=True)
    ip = models.ForeignKey(IPType, on_delete=models.DO_NOTHING, blank=True, null=True)
    ic = models.ForeignKey(ICType, on_delete=models.DO_NOTHING, blank=True, null=True)
    summary = models.TextField(max_length=500, blank=True, null=True)
    considerations = models.TextField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    sent = models.BooleanField(default=False)
    qty_sent = models.IntegerField(default=0, null=True, blank=True)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return 'pk:%s | %s | %sKW - %sRPM - %sV' % (self.pk, self.qty, self.kw, self.rpm, self.voltage)

    class Meta:
        permissions = (
            ('index_prefspec', 'can see list of prefsepcs'),
        )


class ProfChangeRequest(models.Model):
    owner = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING)
    proforma = models.ForeignKey(Xpref, on_delete=models.CASCADE)
    description = models.TextField(max_length=600)
    pub_date = models.DateTimeField(default=now)
    change_needed = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.description[:100]


class PaymentType(models.Model):
    title = models.CharField(max_length=25)

    def __str__(self):
        return '%s' % self.title


class Payment(models.Model):
    owner = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING)
    # xpref_id = models.ForeignKey(Xpref, on_delete=models.DO_NOTHING, related_name='payments')
    xpref_id = models.ForeignKey(Xpref, on_delete=models.DO_NOTHING)

    number = models.IntegerField(unique=True)
    type = models.ForeignKey(PaymentType, on_delete=models.DO_NOTHING, blank=True, null=True)
    temp_number = models.IntegerField(unique=True, null=True, blank=True)
    amount = models.FloatField()
    payment_date = models.DateTimeField(default=now)
    date_fa = jmodels.jDateField(default=now)
    date_fa_text = models.CharField(null=True, blank=True, max_length=20)
    due_date = jmodels.jDateField(blank=True, null=True)
    due_date_text = models.CharField(null=True, blank=True, max_length=20)
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
    pay = models.ForeignKey(Payment, on_delete=models.CASCADE)
    image = models.FileField(upload_to=upload_location, null=True, blank=True)


def change_date_format(date, separator='/'):
    date_splitted = date.split(separator)
    year = int(date_splitted[0])
    month = int(date_splitted[1])
    day = int(date_splitted[2])
    date = jdatetime.date(year=year, month=month, day=day)
    return date


class Perm(TimeStampedModel):
    proforma = models.ForeignKey(Xpref, on_delete=models.CASCADE, related_name='perm_prof')
    number = models.IntegerField()
    date = models.CharField(max_length=10)
    year = models.CharField(max_length=4)
    due_date = jmodels.jDateField(null=True, blank=True)
    date_complete = jmodels.jDateField(null=True, blank=True)

    def __str__(self):
        return "Perm: %s - Prof: %s: " % (self.number, self.proforma,)

    def qty_total(self):
        count = self.permspec_perm.aggregate(Sum('qty'))
        return count['qty__sum']

    def qty_sent(self):
        count = self.inv_out_perm.aggregate(sum=Sum('inventoryoutspec__qty'))
        if not count['sum']:
            return 0
        return count['sum']

    def qty_remained(self):
        return self.qty_total() - self.qty_sent()

    def update_delays(self):
        remaining = self.qty_total() - self.qty_sent()
        print('remaingin: ', remaining)
        if remaining == 0:
            date = change_date_format(self.date, '/')
            self.date_complete = date
            self.save()


class PermSpec(TimeStampedModel):
    perm = models.ForeignKey(Perm, on_delete=models.CASCADE, related_name='permspec_perm')
    row = models.IntegerField()
    code = models.IntegerField()
    details = models.CharField(max_length=100)
    qty = models.IntegerField()
    price_unit = models.FloatField()
    price = models.FloatField()

    def __str__(self):
        return "%s دستگاه %s با مجوز %s" % (
            self.qty,
            self.code,
            self.perm.number,
        )

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(PermSpec, self).save()

        self.perm.update_delays()


class InventoryOut(TimeStampedModel):
    perm = models.ForeignKey(Perm, on_delete=models.CASCADE, related_name='inv_out_perm')
    number = models.IntegerField()
    date = models.CharField(max_length=10)
    year = models.CharField(max_length=4)

    def __str__(self):
        return "InvOut: %s - Perm: %s: " % (
            self.number,
            self.perm.number,
        )

    def qty(self):
        return self.inventoryoutspec_set.aggregate(sum=Sum('qty'))['sum']


class InventoryOutSpec(TimeStampedModel):
    invout = models.ForeignKey(InventoryOut, on_delete=models.CASCADE)
    row = models.IntegerField()
    code = models.IntegerField()
    details = models.CharField(max_length=100)
    qty = models.IntegerField(default=1)
    serial_number = models.CharField(max_length=20, null=True, blank=True)
    price_unit = models.FloatField()
    price = models.FloatField()

    def __str__(self):
        return "InvOut: %s - qty: %s - serial:%s - date out: %s " % (
            self.invout.number,
            self.qty,
            self.serial_number,
            self.invout.date
        )


class Invoice(TimeStampedModel):
    invout = models.ForeignKey(InventoryOut, on_delete=models.CASCADE, related_name='invoice_invout')
    number = models.IntegerField()
    date = models.CharField(max_length=10)
    year = models.CharField(max_length=4)

    def __str__(self):
        return "Invoice: %s - Invout: %s: " % (
            self.number,
            self.invout.number,
        )


class InvoiceSpec(TimeStampedModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    row = models.IntegerField()
    code = models.IntegerField()
    details = models.CharField(max_length=100)
    qty = models.IntegerField(default=1)
    serial_number = models.CharField(max_length=20,null=True, blank=True)
    price_unit = models.FloatField()
    price = models.FloatField()

    def __str__(self):
        return "invoce: %s - qty: %s: - price: %s - invout: %s - perm:%s - proforma: %s - req: %s" % (
            self.invoice.number,
            self.qty,
            self.price_unit,
            self.invoice.invout.number,
            self.invoice.invout.perm.number,
            self.invoice.invout.perm.proforma.number,
            self.invoice.invout.perm.proforma.req_id.number,
        )
