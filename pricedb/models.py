from django.db import models
from django.utils.timezone import now
from django_jalali.db import models as jmodels

# Create your models here.
from motordb.models import MotorsCode


class PriceDb(models.Model):
    title = models.CharField(max_length=40)
    summary = models.TextField(max_length=600)
    date_published = models.DateTimeField(default=now)
    date_published_fa = jmodels.jDateField(default=now)

    def __str__(self):
        return '%s' % (self.title)

    class Meta:
        permissions = (
            ('index_pricedb', 'can list price dbs'),
        )


class MotorDB(models.Model):
    price_set = models.ForeignKey(PriceDb, on_delete=models.CASCADE)
    motor = models.ForeignKey(MotorsCode, on_delete=models.CASCADE)
    prime_cost = models.FloatField(null=True, blank=True)
    base_price = models.FloatField(null=True, blank=True)
    sale_price = models.FloatField(null=True, blank=True)
    pub_date = models.DateTimeField(default=now)

    def __str__(self):
        return 'prime cost: %s' % (self.prime_cost)

    class Meta:
        permissions = (
            ('index_motordb', 'can view price database'),
            ('view_motordb', 'can view price database'),
            ('clean_motordb', 'can view price database'),
        )

