import jdatetime
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.timezone import now
from django_jalali.db import models as jmodels


# Create your models here.
# class ReceivedBy(models.Model):
#     title = models.CharField(max_length=15)
#
#     def __str__(self):
#         return '%s' % self.title
from request.models import ReqSpec, Xpref
from customer.models import Customer as CustomerUser


class ReqEntered(models.Model):
    number_entered = models.CharField(max_length=20, blank=True, null=True)
    number_automation = models.IntegerField(unique=True)
    # received_by = models.ForeignKey(ReceivedBy, on_delete=models.DO_NOTHING)
    is_entered = models.BooleanField(default=False)
    title = models.CharField(max_length=250, null=True, blank=True)
    # owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    owner_text = models.CharField(max_length=40, default='الوند')
    date_txt = models.CharField(max_length=12, null=True, blank=True)
    customer = models.CharField(max_length=200, null=True, blank=True)
    is_request = models.BooleanField(default=True)
    attachment = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=600, null=True, blank=True)
    date_fa = jmodels.jDateField(default=now, null=True, blank=True)
    # date_fa = jmodels.jDateField(default=now, null=True, blank=True)

    def __str__(self):
        return '%s' % self.number_automation

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.date_fa = self.jdate_form_text()
        super(ReqEntered, self).save(force_insert, force_update, using, update_fields)

    def jdate_form_text(self):
        year, month, day = self.date_txt.split('/')
        if len(year) == 2:
            year = f"13{year}"
        return jdatetime.date(int(year), int(month), int(day))


class TrackXpref(models.Model):
    number = models.BigIntegerField()
    customer_code = models.BigIntegerField(null=True, blank=True)
    customer_name = models.CharField(max_length=60, null=True, blank=True)
    date_fa = models.CharField(max_length=15)
    exp_date_fa = models.CharField(max_length=15, null=True, blank=True)
    code = models.CharField(max_length=40)
    details = models.CharField(max_length=100, null=True, blank=True)
    req_number = models.CharField(max_length=200, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    price_reduction = models.FloatField(null=True, blank=True)
    perm_number = models.CharField(max_length=10, null=True, blank=True)
    receivable = models.FloatField(null=True, blank=True)
    red_flag = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    is_entered = models.BooleanField(default=False)

    def __str__(self):
        return '%s - #items: %s' % (self.number, self.items())

    def items(self):
        count = TrackXpref.objects.filter(number=self.number).count()
        return count


class Payments(models.Model):
    number = models.CharField(max_length=20)
    prof_number = models.CharField(max_length=40)
    date_txt = models.CharField(max_length=12, null=True, blank=True)
    date = jmodels.jDateField(blank=True, null=True)
    amount = models.FloatField()
    type = models.CharField(max_length=10)
    is_entered = models.BooleanField(default=False)
    red_flag = models.BooleanField(default=False)

    def __str__(self):
        return '#%s - $%s' % (self.number, self.amount)


class TrackItemsCode(models.Model):
    code = models.BigIntegerField()
    kw = models.CharField(max_length=50, null=True, blank=True)
    frame_size = models.CharField(max_length=50, blank=True, null=True)
    speed = models.CharField(max_length=50, null=True, blank=True)
    voltage = models.CharField(max_length=50, null=True, blank=True)
    ip = models.CharField(max_length=50, null=True, blank=True)
    ic = models.CharField(max_length=50, null=True, blank=True)
    im = models.CharField(max_length=50, null=True, blank=True)
    yd = models.CharField(max_length=50, null=True, blank=True)
    # ex_type = models.IntegerField(choices=ex_types, default=0, null=True, blank=True)
    # images = models.FileField(upload_to='motordb/')
    efficiency = models.CharField(max_length=50, null=True, blank=True)
    pf = models.CharField(max_length=50, null=True, blank=True)
    current_ln = models.CharField(max_length=50, null=True, blank=True)
    current_ls_to_ln = models.CharField(max_length=50, null=True, blank=True)
    torque_tn = models.CharField(max_length=50, null=True, blank=True)
    torque_ts_to_tn = models.CharField(max_length=50, null=True, blank=True)
    torque_tmax_to_tn = models.CharField(max_length=50, null=True, blank=True)
    torque_rotor_inertia = models.CharField(max_length=50, null=True, blank=True)
    weight = models.CharField(max_length=50, null=True, blank=True)
    freq = models.IntegerField(default=50)
    details = models.TextField()
    red_flag = models.BooleanField(default=False)
    green_flag = models.BooleanField(default=False)
    is_entered = models.BooleanField(default=False)
    temp_str = models.TextField(max_length=1000, null=True, blank=True)


class ProformaFollowUp(models.Model):
    owner = models.CharField(max_length=15)
    date = models.CharField(max_length=15)
    number = models.CharField(max_length=15)
    details = models.TextField(blank=True, null=True)
    customer = models.CharField(max_length=50, blank=True, null=True)
    result = models.TextField()

    def __str__(self):
        return "%s - %s" % (self.number, self.owner)

    def has_proforma(self):
        try:
            p = Xpref.objects.get(number=self.number)
            return True
        except:
            return False


class Customer(models.Model):
    code = models.CharField(max_length=12)
    name = models.CharField(max_length=100)
    tel = models.CharField(max_length=60, null=True, blank=True)
    addr = models.TextField(null=True, blank=True)
    entered = models.BooleanField(default=False)
    exported = models.BooleanField(default=False)
    temp_code = models.CharField(max_length=12, default=None)

    def __str__(self):
        return '%s: %s' % (self.code, self.name)


class CustomerResolver(models.Model):
    code1 = models.CharField(max_length=12)
    code2 = models.CharField(max_length=12)
    similarity = models.FloatField()
    resolved = models.BooleanField(default=False)
    cleared = models.BooleanField(default=False)

    def __str__(self):
        customer = self.customer1()
        customer_temp = self.customer2()
        # return '%s: %s' % (self.code1, self.code2)
        return '%s: %s: %s' % (customer, customer_temp, self.similarity)

    def customer1(self):
        customer = CustomerUser.objects.get(code=self.code1)
        return customer

    def customer2(self):
        customer = Customer.objects.get(code=self.code2)
        return customer


class Perm(models.Model):
    prof_number = models.IntegerField()
    perm_number = models.IntegerField()
    perm_date = models.CharField(max_length=12)
    customer_code = models.IntegerField()
    customer_name = models.CharField(max_length=100)
    product_code = models.IntegerField()
    product_details = models.TextField(null=True)
    summary = models.TextField(null=True)
    qty = models.IntegerField()
    unit_price = models.FloatField()
    total_price = models.FloatField()
    extra = models.FloatField(null=True)
    payable = models.FloatField(null=True)
    kw = models.CharField(max_length=20, null=True)

    def __str__(self):
        return "perm: %s, Proforma: %s, qty: %s kw: %s" % (self.perm_number, self.prof_number, self.qty, self.kw)


class PriceList(models.Model):
    price_list_id = models.IntegerField()
    price_list_name = models.CharField(max_length=40)
    kw = models.FloatField()
    rpm = models.IntegerField()
    code = models.BigIntegerField()
    prime_cost = models.FloatField(null=True, blank=True)
    base_price = models.FloatField()
    sale_price = models.FloatField()
    pub_date = models.DateTimeField(default=now)
    entered = models.BooleanField(default=False)

    def __str__(self):
        return '%s kw - %s rpm: %s' % (self.kw, self.rpm, self.sale_price,)


class TadvinTotal(models.Model):
    year = models.IntegerField()
    doctype_code = models.IntegerField()
    doctype = models.CharField(max_length=20)
    doc_number = models.IntegerField()
    row_number = models.IntegerField()
    date = models.CharField(max_length=14)
    serial_number = models.CharField(null=True, blank=True, max_length=30)
    code = models.IntegerField(null=True, blank=True)
    details = models.CharField(max_length=150, null=True, blank=True)
    prof_number = models.IntegerField()
    prof_row = models.IntegerField()
    perm_number = models.PositiveIntegerField(null=True, blank=True)
    perm_row = models.PositiveIntegerField(null=True, blank=True)
    havale_number = models.PositiveIntegerField(null=True, blank=True)
    havale_row = models.PositiveIntegerField(null=True, blank=True)
    factor_number = models.PositiveIntegerField(null=True, blank=True)
    factor_row = models.PositiveIntegerField(null=True, blank=True)
    qty = models.IntegerField()
    discount_value = models.FloatField(null=True, blank=True)
    discount_percent = models.FloatField(null=True, blank=True)
    price_unit = models.FloatField()
    price = models.FloatField()
    entered = models.BooleanField(default=False)

    def __str__(self):
        return "%s - %s" % (self.doctype, self.doc_number,)
