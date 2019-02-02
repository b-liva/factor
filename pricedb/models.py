from django.db import models
from django.utils.timezone import now


# Create your models here.
class PriceDb(models.Model):
    title = models.CharField(max_length=40)
    summary = models.TextField(max_length=600)

    def __str__(self):
        return '%s' % (self.title)


class PrimeCost(models.Model):
    price_db = models.ForeignKey(PriceDb, on_delete=models.CASCADE)
    kw5_5 = models.FloatField()


class MotorDB(models.Model):
    price_set = models.ForeignKey(PriceDb, on_delete=models.CASCADE)
    kw = models.FloatField()
    speed = models.IntegerField()
    voltage = models.IntegerField(default=380)
    prime_cost = models.FloatField(null=True, blank=True)
    base_price = models.FloatField(null=True, blank=True)
    sale_price = models.FloatField(null=True, blank=True)
    pub_date = models.DateTimeField(default=now)

    def __str__(self):
        return 'prime cost: %s' % (self.prime_cost)

    class Meta:
        permissions = (
            ('view_pricedb', 'can view price database'),
            ('clean_pricedb', 'can view price database'),
        )


class SalesPrice(models.Model):
    price_set = models.ForeignKey(PriceDb, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    price = models.IntegerField()

    def __str__(self):
        return '%s - %s - %s' % (self.price_set, self.code, self.price)
