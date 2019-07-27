from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import ReqEntered, Payments, TrackItemsCode, TrackXpref, ProformaFollowUp, Customer, CustomerResolver, Perm
from import_export import resources

# Register your models here.
# admin.site.register(ReqEntered)
@admin.register(ReqEntered)
@admin.register(TrackItemsCode)
@admin.register(TrackXpref)
@admin.register(Payments)
@admin.register(ProformaFollowUp)
@admin.register(Customer)
@admin.register(CustomerResolver)
@admin.register(Perm)

# class ReqResource(resources.ModelResource):
#
#     class Meta:
#         model = ReqEntered

class ReqAdmin(ImportExportModelAdmin):
    pass

