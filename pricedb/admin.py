from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import PriceDb, SalesPrice
from import_export import resources

admin.site.register(PriceDb)
# admin.site.register(SalesPrice)


@admin.register(SalesPrice)
class SalesPriceAdmin(ImportExportModelAdmin):
    pass

