import jdatetime
from request.helpers import helpers
from request.tests.factory import factories
from core.date import Date


class BaseProformaFactories:
    def base_proformas(self):
        prof1 = factories.ProformaFactory.create(number=150)
        date_str = '20201014'
        date = Date.get_date_from_date_str(date_str)
        date_fa = jdatetime.date.fromgregorian(date=date, locale='fa_IR')
        prof1.date_fa = date_fa
        prof1.save()
        factories.ProformaSpecFactory.create(xpref_id=prof1, price=160000000, kw=18.5, rpm=3000, qty=1)
        factories.ProformaSpecFactory.create(xpref_id=prof1, price=1000000000, kw=132, rpm=1500, qty=2)
        prof2 = factories.ProformaFactory.create(number=151)
        date_str = '20201014'
        date = Date.get_date_from_date_str(date_str)
        date_fa = jdatetime.date.fromgregorian(date=date, locale='fa_IR')
        prof2.date_fa = date_fa
        prof2.save()
        factories.ProformaSpecFactory.create(xpref_id=prof2, price=160000000, kw=18.5, rpm=3000, qty=1)
        factories.ProformaSpecFactory.create(xpref_id=prof2, price=520000000, kw=90, rpm=1500, qty=2)
        prof3 = factories.ProformaFactory.create(number=152)
        date_str = '20201014'
        date = Date.get_date_from_date_str(date_str)
        date_fa = jdatetime.date.fromgregorian(date=date, locale='fa_IR')
        prof3.date_fa = date_fa
        factories.ProformaSpecFactory.create(xpref_id=prof3, price=1000000000, kw=132, rpm=1500, qty=1)
        factories.ProformaSpecFactory.create(xpref_id=prof3, price=520000000, kw=90, rpm=1500, qty=2)

        prof3.save()
