from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.utils.translation import gettext as _
from request.models import TimeStampedModel
from django_jalali.db import models as jmodels
User = get_user_model()


# Create your models here.
class BaseCostRow(models.Model):
    unit_choices = [
        ('kg', _('kg')),
        ('machine', _('machine')),
        ('item', _('item')),
    ]
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)
    qty = models.IntegerField()
    price = models.IntegerField()
    unit = models.CharField(max_length=10, choices=unit_choices)

    class Meta:
        abstract = True


class WageCost(BaseCostRow):

    class Meta:
        permissions = [
            ('read_wagecost', 'can retrieve wage cost')
        ]


class SteelRebar(BaseCostRow):
    pass


class OverheadCost(BaseCostRow):
    pass


class Steel(BaseCostRow):
    pass


class CuStator(BaseCostRow):
    pass


class AluIngot(BaseCostRow):
    pass


class SiliconSheet(BaseCostRow):
    pass


class CastIron(BaseCostRow):
    pass


class Bearing(BaseCostRow):
    name = models.CharField(max_length=12)


class Test(BaseCostRow):
    name = models.CharField(max_length=12)


class Certificate(BaseCostRow):
    name = models.CharField(max_length=12)


class ProjectCostBase(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    wage = models.ForeignKey(WageCost, on_delete=models.DO_NOTHING)
    steel_rebar = models.ForeignKey(SteelRebar, on_delete=models.DO_NOTHING)
    overhead = models.ForeignKey(OverheadCost, on_delete=models.DO_NOTHING)
    steel = models.ForeignKey(Steel, on_delete=models.DO_NOTHING)
    cu = models.ForeignKey(CuStator, on_delete=models.DO_NOTHING)
    alu = models.ForeignKey(AluIngot, on_delete=models.DO_NOTHING)
    silicon = models.ForeignKey(SiliconSheet, on_delete=models.DO_NOTHING)
    cast_iron = models.ForeignKey(CastIron, on_delete=models.DO_NOTHING)

    class Meta:
        abstract = True


class ProjectCost(ProjectCostBase):
    ch_number = models.CharField(max_length=16)
    motor_type = models.CharField(max_length=6)
    date_fa = jmodels.jDateField(default=now)
    bearing = models.ManyToManyField(Bearing)
    test = models.ManyToManyField(Test)
    certificate = models.ManyToManyField(Certificate)
    standard_parts = models.IntegerField()
    cost_production = models.IntegerField()
    general_cost = models.IntegerField()
    cost_practical = models.IntegerField()

    class Meta:
        permissions = [
            ('read_projectcost', 'can read projectcost'),
        ]
